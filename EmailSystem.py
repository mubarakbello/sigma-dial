import smtplib
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def mail_sender(sender, password, recipient, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 25)
    server.connect("smtp.gmail.com", 465)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # server.starttls()
    # server.starttls() not used because of the port, if .smtp with port 587 were used it'll be relevant
    # try:
    #     server.login(sender, password)
    # except Exception:
    #     return 'END Error validating your details.\nTry again later'
    server.login(sender,password)
    try:
        response_text = MIMEMultipart()
        response_text['To'] = recipient
        response_text['From'] = sender
        response_text['Subject'] = subject
        response_text.attach(MIMEText(message, 'plain'))
        server.sendmail(sender, recipient, response_text.as_string())
        server.quit()
        return 'END Mail sent successfully!'
    except SMTPAuthenticationError:
        server.quit()
        return 'END Response not accepted by Google.'
    except Exception:
        server.quit()
        return 'END Error sending mail. Please try agin later.'


def mail_receiver():
    pass