from django.conf import settings
import datetime
import requests

def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60 
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

class CheckGrammar(object):

    text_to_check = ''
    corrected_text = ''

    def __init__(self, text_to_check=''):

        self.text_to_check = text_to_check
        if len(text_to_check) > 0:
            self.check_text()

    def check_text(self):

        r = requests.get(
            'https://speller.yandex.net/services/spellservice.json/checkText?text={text}'.format(text=self.text_to_check))
        json_data = r.json()
        if len(json_data):
            self.corrected_text = r.json()[0]['s'][0]


