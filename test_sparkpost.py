from sparkpost import SparkPost
from config import *


sp = SparkPost(SPARKPOST_KEY)


response = sp.transmissions.send(
    recipients=['minhaz.ratul@gmail.com'],
    html='<p>Hello world</p>',
    from_email='m@ratul.xyz',
    subject="It's working"
)

print(response)
