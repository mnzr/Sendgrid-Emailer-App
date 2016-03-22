# Views are where the routes are defined
import pprint
import json
import rethinkdb as r
import sendgrid
# import csv
from flask import render_template, url_for, request, g, redirect
# from werkzeug import secure_filename
from .forms import EmailForm, AddContactForm, NewCampaignForm, TestForm
from config import *
from app import app


sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)


@app.before_request
def before_request():
    g.db = r.connect(host=HOST, port=PORT, db=DB)


@app.teardown_request
def teardown_request(exception):
    g.db.close()


# Root for the test site
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EmailForm()

    if form.validate_on_submit():
        return redirect(url_for('emails'))

    return render_template('index.html',
                           title='Home',
                           form=form)


@app.route('/emails')
def emails():
    messages = list(r.table(TABLE).run(g.db))
    return render_template('emails.html', messages=messages)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    current_lists = json.loads(sg.client.contactdb.lists.get().response_body)['lists']
    form = AddContactForm()
    form.list_items.choices = [(lst['id'], lst['name']) for lst in current_lists]

    if form.validate_on_submit():
        print(form.list_items.data)
        data = {'sample': 'data'}

        return redirect(url_for('contacts'))
    # This is really handy during debugging
    # print(form.errors)

    ##################################################
    # Add Multiple Recipients to a List #
    # POST /contactdb/lists/{list_id}/recipients #
    """
    data = {'sample': 'data'}
    params = {'list_id': 0}
    list_id = "test_url_param"
    response = sg.client.contactdb.lists._(list_id).recipients.post(request_body=data, query_params=params)
    """
    return render_template('contacts.html',
                           # current_lists=current_lists,
                           form=form)


@app.route('/campaigns')
def campaigns():
    list_ids = [x['id'] for x in json.loads(sg.client.contactdb.lists.get().response_body)['lists']]
    form = NewCampaignForm(list_ids)
    return form.list_ids

"""
@app.route('/campaigns/<campaign_id>'):
def campaigns():
"""


@app.route('/test', methods=['GET', 'POST'])
def test():
    form = TestForm()
    if form.validate_on_submit():
        print("Ha")
        return redirect(url_for('index'))
    return render_template('test.html',
                           form=form)
