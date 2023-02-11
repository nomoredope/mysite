import smtplib
import json
from time import sleep
config = json.load(open('configs/email_config.json'))


def check_mail(mail):
    message = 's' # генерация символов
    server_ssl = smtplib.SMTP_SSL(config['smtp'], config['smtp_port']) # "smtp.rambler.ru:465"
    server_ssl.ehlo()  # optional, called by login()
    server_ssl.login(config['mail_ad'], config['mail_pass']) # "anton_slashhev@rambler.ru", "Denis102"
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(config['mail_ad'], mail, message)
    # sleep(15)
    server_ssl.close()
    return message

