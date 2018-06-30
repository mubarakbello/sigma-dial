import africastalking as afs
from flask import Flask, request

from EmailSystem import mail_sender

USERNAME = 'sandbox'
API_KEY = '5e09c729236f9fd4bb0cd92e4ede25576f366734b442a0bd5297eda12385698d'
afs.initialize(USERNAME, API_KEY)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    response = request.form['text']
    responses = response.strip('*')
    if response == '':
        text_mes = 'CON DialMail\nRead and send quick mails!\n1. Read mails\n2. Send a quick maail'
    elif response == '1':
        text_mes = 'CON '
    elif response == '2':
        text_mes = 'CON DialMail\nEnter your gmail login details\n\nE-mail:'
    elif len(responses) == 2:
        if responses[0] == 2: text_mes = 'CON DialMail\n\nPassword:'
    elif len(responses) == 3:
        if responses[0] == 2: text_mes = "CON DialMail\n\nRecipient's mail address:"
    elif len(responses) == 4:
        if responses[0] == 2: text_mes = 'CON DialMail\n\nSubject:'
    elif len(responses) == 5:
        if responses[0] == 2: text_mes = 'CON DialMail\n\nMessage body:'
    elif len(responses) == 6:
        if responses[0] == 2: mail_sender(*responses[1:])
    # text_mes = 'END An error occurred. Try again later'
    return text_mes


if __name__ == '__main__':
    app.run()