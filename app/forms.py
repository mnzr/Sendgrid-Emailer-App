from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, TextField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms_components import DateRange
from flask_wysiwyg.wysiwyg import WysiwygField
from flask_wtf.file import FileField


class AddRecipientsForm(Form):
    list_items = SelectField('List items', coerce=int, choices=[])
    csv = FileField('Email address list upload')


class AddListForm(Form):
    list_name = StringField('List name')  # , choices=[], coerce=unicode, option_widget=None)


class NewCampaignForm(Form):
    title = StringField('Title')
    subject = StringField('Subject')
    sender_id = 23117  # StringField('Sender ID')
    list_ids = SelectField('List IDs', coerce=int, choices=[])
    suppression_group_id = 629,
    html_content = WysiwygField('HTML Content',
                                default="""<a href="[unsubscribe]">Unsubscribe</a>""")
    plain_content = TextAreaField('Plain Content',
                                  default="""<a href="[unsubscribe]">Unsubscribe</a>""")
    # custom_unsubscribe_url = "http://ratul.xyz"


class CampaignPageForm(Form):
    # date = DateTimeField(label='Date', format='%Y-%m-%d %H:%M')
    date = DateTimeField('Date-time Picker')
