import requests


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


