# Views are where the routes are defined
import pprint
import rethinkdb as r
import mandrill
from flask import render_template, url_for, request, g, redirect
from .forms import EmailForm
from config import *
from app import app


mandrill_client = mandrill.Mandrill('2HY5VR2aZMP5FAE06lYYig')


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
        emails = form.email_addresses.data.split(',')
        pprint.pprint(emails, indent=4, depth=1)
        to = []
        for email in emails:
            to.append({
                        'email': email,
                        'type': 'to'
                      })
        message = {
            'from_email': 'm@ratul.xyz',
            'from_name': 'Example Name',
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
def messages():
    messages = list(r.table(TABLE).run(g.db))
    return render_template('emails.html', messages=messages)
