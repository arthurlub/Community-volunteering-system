# -*- coding: utf-8 -*-
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

fromaddr = 'community1volunteering1system@gmail.com'
username = fromaddr
password = 'community1vo'


def send_email(client_email, subject, body, attachment=None):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    recipients = [client_email]
    client_msg = MIMEMultipart()
    client_msg['From'] = fromaddr
    client_msg['To'] = client_email
    client_msg['Date'] = formatdate(localtime=True)
    client_msg['Subject'] = subject
    client_msg.attach(MIMEText(body))

    server.sendmail(fromaddr, recipients, client_msg.as_string())
    server.close()



