import smtplib
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
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
recipient_mail = input('receipient_mail: ')

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


def attach_file(filename, path):
    for recipient in recipient_mail:
        message = MIMEMultipart()
        message['To'] = recipient
        message['From'] = your_mail
        message['Subject'] = message_subject
        body = message_
        message.attach(MIMEText(body, 'plain'))

    # attachment
    filename = file_name
    path = open(file_path, 'rb')
    part = MIMEBase('application', 'octet stream')
    part.set_payload(path.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    message.attach(part)
    text = message.as_string()
    send_attach_req = input('Send? Yes(y) or No(n)')
    if send_attach_req == 'y':
        for receiver in recipient_mail:
            send_mail(your_mail, your_mail_password, receiver, text)
    else:
        pass


attach_request = input('Do you want to attach a file? Yes(y) or No(n)')
if attach_request == 'y':
    file_name = input('filename: ')
    print('Use the format below')
    print(r"C:/Users/USER/Pictures/titanicpic.jpg")
    file_path = input('File Location: ')
    attach_file(file_name, file_path)

if attach_request != 'y':

    send_request = input('Send? Yes (y) or No(n)')
    if send_request == 'y':
        try:
            send_mail(your_mail, your_mail_password, recipient_mail, message_)
        except SMTPAuthenticationError:
            print('Email not sent.')
    else:
        pass

#smtplib.SMTPAuthenticationError