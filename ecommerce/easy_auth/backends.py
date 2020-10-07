from email.mime.text import MIMEText
from email.header import Header
import smtplib
import random


def create_pass(q_letters=12):

    LETTERS = 'QWERTYUIOPLMNBVCXZASDFGHJKqwertyuioplkjhgfdsazxcvbnm12345678901234567890'
    password = ''
    while q_letters:
        password += LETTERS[random.randint(0, len(LETTERS)-1)]
        q_letters -= 1
    return password


class Email(object):

    text = None
    mail_host = None
    mail_port = None
    mail_login = None
    mail_pass = None

    def __init__(self, text):

        self.text = text

    def _get_messageMIME(self, reciever):

        msg = MIMEText(self.text, 'plain', 'utf-8')
        msg['Subject'] = Header('Кек лол', 'utf-8')
        msg['From'] = self.mail_login
        msg['To'] = reciever

        return msg.as_string()

    def _get_host_with_port(self):

        return '{}:{}'.format(self.mail_host, str(self.mail_port))

    def send_message(self, reciever):
        
        smtp_obj = smtplib.SMTP(self._get_host_with_port())
        smtp_obj.starttls()
        smtp_obj.login(self.mail_login, self.mail_pass)
        smtp_obj.sendmail(self.mail_login, reciever, self._get_messageMIME(reciever))
        smtp_obj.quit()

    
class VdkDefaultEmail(Email):

    mail_host = 'smtp.mail.ru'
    mail_port = 587
    mail_login = 'info@vdkonline.ru'
    mail_pass = 'cytvin-sIsryr'
