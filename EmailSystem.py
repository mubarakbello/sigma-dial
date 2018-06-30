import smtplib
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print('Welcome to Email Sending System, kindly follow all instructions as go on')


def mail_sender(sender, password, recipient, subject, message):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.starttls() not used because of the port, if .smtp with port 587 were used it'll be relevant
    try:
        server.login(sender, password)
    except Exception:
        print('END Error validating your details.\nTry again later')
    try:
        response_text = MIMEMultipart()
        response_text['To'] = recipient
        response_text['From'] = sender
        response_text['Subject'] = subject
        response_text.attach(MIMEText(message, 'plain'))
        server.sendmail(sender, recipient, message)
        print('END Mail sent successfully!')
    except SMTPAuthenticationError:
        print('END Response not accepted by Google.')
    except Exception:
        print('END Error sendding mail. Please try agin later.')
    server.quit()


def mail_receiver():
    pass