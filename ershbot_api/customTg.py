import json
import os
import requests


def bot_command_decorator(command):
    def method_decorator(method_to_decorate):
        def wrapper(self, request_body, user_id):
            message = request_body.get('message')
            if message:
                if message.get('text') == command:
                    user_id = message['from'].get('id')
                    return method_to_decorate(self, request_body, user_id)
        return wrapper
    return method_decorator
        
class TelegramBot():

    def __init__(self):

        self.token = os.environ.get('ERSH_TOKEN')
        self.url = f'https://api.telegram.org/bot{self.token}'

    def getMe(self):
        
        get_me_url = os.path.join(self.url, 'getMe')
        telegram_response = requests.get(get_me_url)
        tracker_bot = telegram_response.json()
        return tracker_bot

    def sendPhoto(self, user_id, file_location, caption = ''):
        
        try:
            send_message_url = os.path.join(self.url, 'sendPhoto')
            files = {'photo':(open(file_location, 'rb'))}
            telegram_request = requests.post(send_message_url, data = {'chat_id': user_id, 'caption': caption}, files = files )
            tracker_message= telegram_request.json()
            print(json.dumps(tracker_message, indexnt = 4))
            return tracker_message
        except Exception as e:
            print(e)

    def sendMessage(self, user_id, text, parse_mode = '', reply_markup = ''):

        send_message_url = os.path.join(self.url, 'sendMessage')
        telegram_request = requests.post(send_message_url, data = {'chat_id': user_id, 'text': text, 'parse_mode': parse_mode, 'reply_markup': reply_markup})
        tracker_message= telegram_request.json()
        #print(tracker_message)
        return tracker_message

    def getFile(self, file_id):
        
        get_file_url = os.path.join(self.url, 'getFile')
        telegram_response = requests.post(get_file_url, data = {'file_id': file_id})
        file_instance = telegram_response.json()
        #print(file_instance)
        return file_instance

    def editMessageText(self, user_id, message_id, text, parse_mode = '', reply_markup = ''):
        edit_message_url = os.path.join(self.url, 'editMessageText')
        telegram_request = requests.post(edit_message_url, data = {'chat_id': user_id, 'message_id': message_id, 'text': text, 'parse_mode': parse_mode, 'reply_markup': reply_markup})
        tracker_message= telegram_request.json()
        #print(tracker_message)
        return tracker_message

class InlineKeyobardButton():

    def __init__(self, text, callback_data):

        self.text = text
        self.callback_data = callback_data
    
    def getButton(self):

        return ({'text': self.text, 'callback_data': self.callback_data})



class InlineKeyobardMarkup():

    def __init__(self):
        self.allrows = []

    def getKeyboard(self):

        return(json.dumps({'inline_keyboard': self.allrows}, indent=4))

    def addRow(self, row):
        self.allrows.append(row)


def createRowKeyboard(keyboard_layout):

    keyboard = InlineKeyobardMarkup()

    for category in keyboard_layout:
        button = InlineKeyobardButton(text = category[1], callback_data= category[0]).getButton()
        keyboard.addRow([button])
        
    return keyboard.getKeyboard()

def createLineKeyboard(keyboard_layout):

    keyboard = InlineKeyobardMarkup()
    buttons = []
    for category in keyboard_layout:
        button = InlineKeyobardButton(text = category[1], callback_data= category[0]).getButton()
        buttons.append(button)
        
    keyboard.addRow(buttons)
        
    return keyboard.getKeyboard()

if __name__ == '__main__':
    createCategoryKeyboard()

    



