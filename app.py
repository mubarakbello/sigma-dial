import africastalking as afs
from flask import Flask, request
import myapp
from EmailSystem import mail_sender

USERNAME = 'sandbox'
API_KEY = '5e09c729236f9fd4bb0cd92e4ede25576f366734b442a0bd5297eda12385698d'
afs.initialize(USERNAME, API_KEY)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    text_mes = 'END Mail sent successfully!'
    response = request.form['text']
    responses = response.split('*')
    print(responses)
    if response == '':
        text_mes = 'CON SigmaDial\n\nRead and send quick mails!\n1. Read mails\n2. Send a quick mail'
    elif response == '1':
        text_mes = 'CON '
    elif response == '2':
        text_mes = 'CON SigmaDial\n\nEnter your gmail login details\nE-mail:'
    elif len(responses) == 2:
        if responses[0] == '2': text_mes = 'CON SigmaDial\n\nPassword:'
    elif len(responses) == 3:
        if responses[0] == '2': text_mes = "CON SigmaDial\n\nRecipient's mail address:"
    elif len(responses) == 4:
        if responses[0] == '2': text_mes = 'CON SigmaDial\n\nSubject:'
    elif len(responses) == 5:
        if responses[0] == '2': text_mes = 'CON SigmaDial\n\nMessage body:'
    elif len(responses) == 6:
        # if responses[0] == '2': text_mes = mail_sender(*responses[1:])
        if responses[0] == '2': text_mes = myapp.send_mail(responses[1], *responses[3:])
    return text_mes


if __name__ == '__main__':
    app.run()