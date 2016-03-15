from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from flask_wysiwyg.wysiwyg import WysiwygField
from flask_wtf.file import FileField


class EmailForm(Form):
    email_addresses = StringField('Email addresses')
    email_upload = FileField('Email address list upload')
    subject = StringField('Subject')
    body = WysiwygField('Body')


class AddContactForm(Form):
    csv = FileField('CSV')
