# Views are where the routes are defined
from pprint import pprint
import json
import rethinkdb as r
import sendgrid
import csv
from flask import render_template, url_for, request, g, redirect, flash
from werkzeug import secure_filename
from .forms import EmailForm, AddRecipientsForm, NewCampaignForm, AddListForm
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
    form_add_recipients = AddRecipientsForm()
    form_add_list = AddListForm()
    fetched_lists = [(lst['id'], lst['name']) for lst in current_lists]
    if fetched_lists:
        form_add_recipients.list_items.choices = [(lst['id'], lst['name']) for lst in current_lists]
    else:
        form_add_recipients.list_items.choices = [(0, "No item")]

    if form_add_recipients.validate_on_submit():
        if form_add_recipients.csv.data.filename != '':
            filename = secure_filename(form_add_recipients.csv.data.filename)
            form_add_recipients.csv.data.save('uploads/' + filename)
            print("Uploaded file is: %s" % form_add_recipients.csv.data.filename)

            # The email contacts that will be uploaded
            request_body = []
            # [{'email': 'test@email.com'}, {'email': 'nottest@teemail.com'}]
            # Make the response_body
            with open('uploads/' + filename) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if 'email' in row:
                        continue
                    request_body.append({
                        'email': row[0],
                        'first_name': row[1],
                        'last_name': row[2]
                    })


            response = sg.client.contactdb.recipients.post(request_body=request_body)
            pprint(json.loads(response.response_body), indent=4, depth=4)
            recipient_ids = json.loads(response.response_body)['persisted_recipients']
            # Adding recipients to the list selected
            list_id = form_add_recipients.list_items.data
            response = sg.client.contactdb.lists._(list_id).recipients.post(request_body=recipient_ids)
            flash("Success! New email addresses will be added shortly.")
        else:
            flash("No file selected")
        return redirect(url_for('contacts'))

    if form_add_list.validate_on_submit():
        print("Trying to add " + form_add_list.list_name.data)
        pprint(current_lists, indent=4, depth=4)
        if [list_details for list_details in current_lists if form_add_list.list_name.data in list_details['name']]:
            flash("List exists")
            print("List exists")
        else:
            try:
                response = sg.client.contactdb.lists.post(request_body={"name": form_add_list.list_name.data})
                flash("Created new list:" + form_add_list.list_name.data)
                print("Created new list:" + form_add_list.list_name.data)
                print('Response:')
                pprint(json.loads(response.response_body), indent=4, depth=4)
                flash("List will be added shortly.")
            except sendgrid.exceptions.SendGridClientError, e:
                print("Error: Can't add new list. Exception: " + e.message)

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
                           form_add_recipients=form_add_recipients,
                           form_add_list=form_add_list,
                           current_lists=current_lists)


@app.route('/campaigns')
def campaigns():
    list_ids = [x['id'] for x in json.loads(sg.client.contactdb.lists.get().response_body)['lists']]
    form = NewCampaignForm(list_ids)
    return form.list_ids


"""
@app.route('/campaigns/<campaign_id>'):
def campaigns():
"""
