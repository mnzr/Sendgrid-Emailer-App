from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from flask_wysiwyg.wysiwyg import WysiwygField


class EmailForm(Form):
    email_addresses = StringField('Email Addresses')
    subject = StringField('Subject')
    body = WysiwygField('body')

    #TextAreaField('Message')
