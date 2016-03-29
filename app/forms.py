from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, TextField
from flask_wysiwyg.wysiwyg import WysiwygField
from flask_wtf.file import FileField


class EmailForm(Form):
    email_addresses = StringField('Email addresses')
    email_upload = FileField('Email address list upload')
    subject = StringField('Subject')
    body = WysiwygField('Body')


class AddRecipientsForm(Form):
    list_items = SelectField('List items', coerce=int, choices=[])
    csv = FileField('Email address list upload')


class AddListForm(Form):
    list_name = TextField('List name') # , choices=[], coerce=unicode, option_widget=None)


class NewCampaignForm(Form):
    title = StringField('Title')
    subject = StringField('Subject')
    sender_id = StringField('Sender ID')
    list_ids = SelectField('List IDs', choices=[])
    suppression_group_id = 692,
    html_content = WysiwygField('HTML Content')
    plain_content = TextAreaField('Plain Content')
    custom_unsubscribe_url = "http://ratul.xyz"
