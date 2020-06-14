import requests
import os

class Webhook():
    
    def __init__(self):
        self.token = os.environ.get('ERSH_TOKEN')
        self.url = f'https://api.telegram.org/bot{self.token}'


    def setWebhook(self):
        
        if os.environ.get('PRODUCTION') == 'True':
            url_path = 'https://ersh-telegram-bot.herokuapp.com/'
        else:
            url_path = 'https://aabe5eb3f80d.ngrok.io'
        
        print(f'Connecting to: {url_path}')
        set_url = os.path.join(self.url, 'setWebhook')
        webhook = requests.post(set_url, data = {'url': url_path})
        r = webhook.json()
        print(r)

    def deleteWebhook(self):

        delete_url = os.path.join(self.url, 'deleteWebhook')
        webhook = requests.post(delete_url)
        r = webhook.json()
        print(r)


if __name__ == '__main__':
    Webhook().deleteWebhook()