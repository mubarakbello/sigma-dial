import smtplib
from smtplib import SMTPAuthenticationError
from email import encoders

print('Welcome to Email Sending System, kindly follow all instructions as go on')


def send_mail(email, password, recipient, message):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# server.starttls() not used because of the port, if .smtp with port 587 were used it'll be relevant
    server.login(email, password)
    server.sendmail(your_mail, recipient, message)
    server.quit()



your_mail = input('email: ')
your_mail_password = input('password: ')
print("If you're inputing multiple emails use a single space to separate them.")
recipient_mail = input('recipient_mail: ')

if ' ' in recipient_mail:
    try:
        recipient_mail = recipient_mail.split(' ')
    except EOFError:
        print('Error Occurred')
    finally:
        pass
else:
    pass
message_subject = input('Subject: ')
message_ = input('Message: ')


