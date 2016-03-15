# Views are where the routes are defined
import pprint
import json
import rethinkdb as r
import sendgrid
# import csv
from flask import render_template, url_for, request, g, redirect
# from werkzeug import secure_filename
from .forms import EmailForm, AddContactForm
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
        to = []
        """
        if form.email_upload.data.filename != '':
            filename = secure_filename(form.email_upload.data.filename)
            form.email_upload.data.save('uploads/' + filename)
            print("Uploaded file is: %s" % form.email_upload.data.filename)
            with open('uploads/' + filename) as csvfile:
                reader = csv.reader(csvfile)
                emails = list(reader)
                for email in emails:
                    to.append({
                                'email': email[0],
                                'type': 'to'
                              })
        """
        emails = form.email_addresses.data.split(',')
        if form.email_addresses.data != '':
            for email in emails:
                print(email)
                to.append({
                            'email': email,
                            'type': 'to'
                          })
        print("Filename: %s" % form.email_upload.data.filename)

        message = {
            'from_email': FROM_MAIL,
            'from_name': FROM_NAME,
            'to': to,
            'subject': form.subject.data,
            'html': form.body.data
        }
        pprint.pprint(message, indent=4, depth=1)
        try:
            result = mandrill_client.messages.send(message=message, async=False)
            print(result)
        except mandrill.Error, e:
            # Mandrill errors are thrown as exceptions
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
            raise


        r.db(DB).table(TABLE).insert(message).run(g.db)

        return redirect(url_for('messages'))

    """


    if form.validate_on_submit():
        message = {
            'from_email': 'message.from_email@example.com',
            'from_name': 'Example Name',
            'to': to,
            'subject': form.subject.data,
            'html': form.body.data
        }
        pprint.pprint(message, indent=4, depth=1)

        r.db(DB).table(TABLE).insert(message).run(g.db)

        return redirect(url_for('emails'))
    """
    return render_template('index.html',
                           title='Home',
                           form=form)


@app.route('/emails')
def emails():
    messages = list(r.table(TABLE).run(g.db))
    return render_template('emails.html', messages=messages)


@app.route('/contacts')
def contacts():
    current_lists = json.loads(sg.client.contactdb.lists.get().response_body)['lists']
    pprint.pprint(current_lists, indent=4, depth=4)

    form = AddContactForm()

    if form.validate_on_submit():

    return render_template('contacts.html', current_lists=current_lists)
