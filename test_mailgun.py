import requests


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox0237bc27a4f749b2a45dce1acdd6c9a6.mailgun.org/messages",
        auth=("api", "key-e0c35afc43262b7de6d17a9655b56a8e"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox0237bc27a4f749b2a45dce1acdd6c9a6.mailgun.org>",
              "to": "Ratul Minhaz <minhaz.ratul@gmail.com>",
              "subject": "Hello Ratul Minhaz",
              "text": "Congratulations Ratul Minhaz, you just sent an email with Mailgun!  You are truly awesome!  You can see a record of this email in your logs: https://mailgun.com/cp/log .  You can send up to 300 emails/day from this sandbox server.  Next, you should add your own domain so you can send 10,000 emails/month for free."})

# print(send_simple_message().content)


def get_lists():
    return requests.get(
        "https://api.mailgun.net/v3/sandbox0237bc27a4f749b2a45dce1acdd6c9a6.mailgun.org/lists",
        auth=("api", "key-e0c35afc43262b7de6d17a9655b56a8e"))

print(get_lists().content)
