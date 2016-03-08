import sendgrid
import os
from config import *


"""
sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)


response = sg.client.api_keys.get()
print(response.status_code)
print(response.response_body)
print(response.response_headers)
"""


sg = sendgrid.SendGridClient(SENDGRID_API_KEY)


message = sendgrid.Mail()
message.add_to('John Doe <ratul@webable.com.bd>')
message.set_subject('Example')
message.set_html('Body')
message.set_text('Body')
message.set_from('Doe John <m@ratul.xyz>')
status, msg = sg.send(message)
print(status, msg)
