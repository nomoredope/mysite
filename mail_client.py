import smtplib
import json
import secrets
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
m_config = json.load(open('configs/email_config.json'))


def gen_code(n: int):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(n))
    return password


def check_mail(mail):
    a = gen_code(8)
    message = f'Your code: {a}' # генерация символов
    server_ssl = smtplib.SMTP_SSL(m_config['smtp'], m_config['smtp_port']) # "smtp.rambler.ru:465"
    server_ssl.ehlo()  # optional, called by login()
    server_ssl.login(m_config['mail_ad'], m_config['mail_pass']) # "anton_slashhev@rambler.ru", "Denis102"
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(m_config['mail_ad'], mail, message)
    # sleep(15)
    server_ssl.close()
    return a


def send_me_message(name, from_mail, message1):
    message = MIMEMultipart('alternative')
    message['From'] = m_config['mail_ad']
    message['To'] = m_config['contact_email']
    message['Subject'] = 'New contact'
    message.attach(MIMEText(f'From: {name}\n Email: {from_mail}\n {message1}'))

    server_ssl = smtplib.SMTP_SSL(m_config['smtp'], m_config['smtp_port'])
    server_ssl.login(m_config['mail_ad'], m_config['mail_pass'])
    server_ssl.sendmail(m_config['mail_ad'], m_config['contact_email'], message.as_string())
    server_ssl.quit()
