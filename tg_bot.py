import requests
import configparser
import time 

config = configparser.ConfigParser()
config.read('config.ini')

class TG_Bot:
    def __init__(self):
        self.token = config["telegram"]["token"]
        self.webhook_url = config["telegram"]["webhook-url"]
        self.init_time = time.time()
        
    def send_message(self, chat_id, text):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        payload = {'chat_id': chat_id, 'text': text}
        return requests.post(url,json=payload)
    
    def parse_massage(self, message):
        date = message["message"]["date"]
        chat_id = message["message"]["chat"]["id"]
        username = message["message"]["from"]["username"]
        text = message["message"]["text"]
        return date, chat_id, username, text
    
    def set_webhook(self):
        url = f'https://api.telegram.org/bot{self.token}/setWebhook?url={self.webhook_url}'
        res = requests.post(url)
        return res.status_code, res.text