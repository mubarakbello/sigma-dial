import africastalking as afs
from flask import Flask, request, render_template
import sqlite3 as sql
import myapp
from EmailSystem import mail_sender

USERNAME = 'sandbox'
API_KEY = '5e09c729236f9fd4bb0cd92e4ede25576f366734b442a0bd5297eda12385698d'
afs.initialize(USERNAME, API_KEY)

app = Flask(__name__)

GOOGLE_CLIENT_ID = '691506785044-m79l433jote690ut6hkqktu3dr32oha7.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '9qeJEKp5rYmptg-rjOObnOb8'
GOOGLE_REFRESH_TOKEN = '1/w1r4JnpN9ZUkyI1jkBNkMsWzDRtf3-3ZhYd29Ik8WuA'

"""
SigmaDial

Please enter your mail address to get started
    -mail-registered
        Enter your nPassword
            -password-correct
                Send a quick mail
                    Recipient address
                        Subject
                            Message
                                -sent-successfully
                                    Mail sent successfully
                                -send-not-complete
                                    An error occurred while sendind. Try again later
                Read your mails
                    This feature isnt implemented yet. Thanks
            -password-incorrect
                Password incorrect. Please try again
    -mail-not-registered
        You need to authorize SigmaDial in your gmail. Visit blahblahblah.com to get started
"""


# @app.route('/webhook', methods=['POST'])
def webhook():
    text_mes = 'END Mail sent successfully!'
    response = request.form['text']
    responses = response.split('*')
    print(responses)
    if response == '':
        text_mes = 'CON SigmaDial\n\nRead and send quick mails!\n1. Read mails\n2. Send a quick mail'
    elif response == '1':
        text_mes = 'END This feature isnt implemented yet. Try again later.'
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
        if responses[0] == '2': text_mes = myapp.send_mail(GOOGLE_REFRESH_TOKEN, responses[1], *responses[3:])
    return text_mes


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        usermail = request.form['mail']
        user_sigmadial_pass = request.form['password']
        print('Mail, pword from request:', usermail, user_sigmadial_pass)
        boolea = retrieveUserInfo('gmail_and_pword', usermail, user_sigmadial_pass)
        print(boolea)
        if boolea:
            return render_template('panel.html', logged_in='Logged in successfully.')
        else:
            condi = insertUser(usermail, user_sigmadial_pass)
            print(condi)
            if condi:
                return render_template('panel.html', acc_created='Account created successfully.')
            else:
                return render_template('index.html', error='Error creating your account.')
    print('GET request')
    return render_template('index.html')

@app.route('/authen', methods=['POST'])
def add_ref_token():
    user = request.form['usermail']
    token = request.form['ref_token']
    print('User, ref_token from request:', user, token)
    token_obtained = myapp.get_token_after_permission(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, token)
    print('Refresh Token obtained from gg:', token_obtained)
    boolea = updateUserKey(user, token_obtained[0])
    print(boolea)
    if boolea:
        return render_template('landing.html', auth_success='Authentication complete. You can exit now.')
    else:
        return render_template('landing.html', auth_error='Error completing authentication. Try again later.')


@app.route('/authenticate', methods=['POST'])
def authe():
    auth_get = myapp.get_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    print('Auth to be returned', auth_get)
    mailing = request.form['emailfield']
    print('Email field:', mailing)
    return render_template('landing.html', auth_gen=auth_get, email=mailing)


def insertUser(mail_address, sigmadial_password):
    print('About to insert user info to db')
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        try:
            userKey = ''
            cur.execute('CREATE TABLE IF NOT EXISTS users (Id INT PRIMARY KEY, Email VARCHAR(255), Password VARCHAR(20), UserKey VARCHAR(255));')
            cur.execute('INSERT INTO users (Email, Password, UserKey) VALUES (?,?,?);', (mail_address, sigmadial_password, userKey))
            print('Insert ops done')
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False

def updateUserKey(mail_address, user_key):
    print('About to update user key')
    with sql.connect('database.db') as conn:
        cur = conn.cursor()
        try:
            cur.execute('UPDATE users SET UserKey = ? WHERE Email = ?;', (user_key, mail_address))
            print('Most liikely update is complete')
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False


def retrieveRefToken(usermail, password):
    print('About to retrieve ref token')
    with sql.connect('database.db') as conn:
            cur = conn.cursor()
            try:
                cur.execute('SELECT UserKey FROM users WHERE Email = ? AND Password = ?', (usermail, password))
                userKey = cur.fetchall()
                print('Type of userkeys returned', type(userKey))
                print('Userkeys:', userKey)
                conn.commit()
                return userKey
            except Exception:
                conn.rollback()
                return False


def retrieveUserInfo(option, mail_address, password='not-some_nice.value'):
    if password != 'not-some_nice.value' and password != None:
        # means the password is entered and auth is needed
        print('Gmail and password entered, auth needed')
        with sql.connect('database.db') as conn:
            cur = conn.cursor()
            try:
                cur.execute('CREATE TABLE IF NOT EXISTS users (Id INT PRIMARY KEY, Email VARCHAR(255), Password VARCHAR(20), UserKey VARCHAR(255));')
                cur.execute('SELECT Email, Password FROM users')
                emails = cur.fetchall()
                print('Type of returned emails', type(emails))
                print('Email, Password', emails)
                conn.commit()
            except Exception:
                emails = []
                conn.rollback()
            if option == 'gmail':
                return True if mail_address in emails else False
            elif option== 'gmail_and_pword':
                if len(emails) == 0: return False
                for row in emails:
                    print('Row i:', row)
                    if (row[0].lower(), row[1].lower()) == (mail_address.lower(), password.lower()):
                        print('Password correct!')
                        return True
                return False
    else:
        # means pword is not entered and mail lookup is needed
        print('Gmail entered, mail lookup needed')
        with sql.connect('database.db') as conn:
            cur = conn.cursor()
            try:
                cur.execute('CREATE TABLE IF NOT EXISTS users (Id INT PRIMARY KEY, Email VARCHAR(255), Password VARCHAR(20));')
                cur.execute('SELECT Email FROM users')
                emails = cur.fetchall()
                print('Type of returned emails', type(emails))
                print('Email', emails)
                conn.commit()
            except Exception:
                emails = []
                conn.rollback()
            for i in emails:
                print('Row i:', i)
                if mail_address.lower() == i[0].lower(): return True
            return False


@app.route('/webhook', methods=['POST'])
def det_response():
    text_mes = "END Mail couldn't send for some reason!"
    response = request.form['text']
    responses = response.split('*')
    print('Webhook response:',responses)
    if response == '':
        text_mes = 'CON SigmaDial\n\nPlease enter your mail address to get started\nGmail:'
    elif len(responses) == 1:
        text_mes = check_if_registered('gmail', responses[0])
    elif len(responses) == 2:
        text_mes = check_if_registered('gmail_and_pword', responses[0], pword=responses[1])
    elif len(responses) == 3:
        if responses[2] == '2':
            text_mes = 'END SigmaDial\n\nThis feature isnt implemented yet. Thanks'
        elif responses[2] == '1':
            text_mes = "CON SigmaDial\n\nRecipient's mail address:"
    elif len(responses) == 4:
        text_mes = 'CON SigmaDial\n\nSubject:'
    elif len(responses) == 5:
        text_mes = 'CON SigmaDial\n\nMessage body:'
    elif len(responses) == 6:
        print('About to send mail')
        reference_token = retrieveRefToken(*responses[:2])
        if reference_token:
            print('Token retrieved:', reference_token)
            text_mes = myapp.send_mail(reference_token, responses[0], *responses[3:])
        else:
            text_mes = 'END Error retrieving your token'
    if response is not None:
        return text_mes
    else:
        return 'END Nothing was returned by SigmaDial'


def check_if_registered(option, mail_address, pword=None):
    answer = retrieveUserInfo(option, mail_address, pword)
    if option == 'gmail':
        if answer:
            return 'CON SigmaDial\n\nEnter your SigmaDial Password:'
        else:
            return 'END SigmaDial\n\nYou need to authorize SigmaDial in your gmail. Visit http://82.196.10.181 to get started'
    elif option == 'gmail_and_password':
        if answer == True:
            print('Yay!')
            return 'CON SigmaDial\n\nWelcome!\n1. Send a quick mail\n2. Read your mails'
        else:
            print('Nay...')
            return 'END SigmaDial\n\nPassword incorrect. Try again later'


# with app.test_request_context() as src:
#     url_sigma = url_for('static', filename='')
if __name__ == '__main__':
    app.run()
