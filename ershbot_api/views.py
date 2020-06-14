from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests
from bs4 import BeautifulSoup
import re
import json

from .models import Section, Dish
from .customTg import TelegramBot, createRowKeyboard, createLineKeyboard

def create_db(Section, Dish):

    ersh_url = 'http://restoranersh.ru/menu.html'
    request = requests.get(ersh_url)

    text = request.text
    new_text = re.sub(r'<dt><small>', r'<dd><small>', text)

    soup = BeautifulSoup(new_text, 'html.parser')

    sections = soup.find_all('section')

    menu_dict = {}

    for section in sections[1:]:
        img = section.find('img')
        img_src = 'http://restoranersh.ru' + re.search(r'src="(?P<src>.*?)"', str(img)).group('src')
        header = section.find('h3')
        small_header = header.find('small')
        if small_header and small_header.text != '':
            header_text = img_src + '#' + re.sub(small_header.text, '#'+small_header.text, header.text)
        else:
            header_text = img_src + '#' + header.text

        menu_dict[header_text] = {}
        content = section.find_all(['dt', 'dd'])
        current_title = None
        for index, dish in enumerate(content):

            title = re.search(r'<dt>(?P<title>.+?)</dt>', str(dish))
            additional_info = re.search(r'<small>(?P<small>.+?)</small>', str(dish))
            price_1 = re.search(r'<strong>(\s)?(?P<price>.+?)</strong>', str(dish))
            price_2 = re.search(r'<span style="font-weight: 600;">(?P<price>.+?)</span>', str(dish))
            if title:
                current_title = title.group('title')
                menu_dict[header_text][current_title] = []

            if additional_info:
                menu_dict[header_text][current_title].append(additional_info.group('small'))

            if price_1:
                menu_dict[header_text][current_title].append(price_1.group('price'))     

            if price_2:
                menu_dict[header_text][current_title].append(price_2.group('price'))       


    for key in menu_dict.keys():
        all_keys = key.split('#')
        img_src = all_keys[0]
        section_title = all_keys[1]
        additional_info = ''
        if len(all_keys) == 3:
            additional_info = all_keys[2]
        section = Section(section_title = section_title, additional_info = additional_info, img_url = img_src)
        section.save()
        for dish_title in menu_dict[key]:
            prop, price = 0, 0
            info_dict = {'type_1': '', 'price_1': None, 'type_2': '', 'price_2': None, 'type_3': '', 'price_3': None, 'type_4': '', 'price_4': None}
            for dish_info in menu_dict[key][dish_title]:
                if ' руб.' in dish_info:
                    price+= 1
                    info_dict[f'price_{price}'] = int(re.sub(r' руб.', '', dish_info))
                else:
                    prop+= 1
                    info_dict[f'type_{prop}'] = dish_info
            dish = Dish(section = section, dish_title = dish_title, **info_dict)
            dish.save()


class ErshApiView():

    def __init__(self):
        self.tgBot = TelegramBot()


    def check_db_if_created(self):
        if len(Section.objects.all()) == 0:
            create_db(Section, Dish)

    def callback_handler(self, callback_query):
        user_id = callback_query['from'].get('id')
        message_id = callback_query['message'].get('message_id')
        data = callback_query.get('data')

        splited_data = data.split('_')
        section = Section.objects.all().get(section_title = splited_data[0])
        dishes = list(Dish.objects.all().filter(section__section_title = splited_data[0]))
        
        callback_type = len(splited_data)
        if callback_type == 1:
            current_dish = 0

        else:
            current_dish = int(splited_data[1]) % len(dishes)

        LAYOUT = [
            (splited_data[0]+'_'+str(current_dish-1), 'Назад'),
            ('Info', f'{current_dish + 1}/{len(dishes)}'),
            (splited_data[0]+'_'+str(current_dish+1), 'Вперед')
        ]
        
        message_head = f'{section.section_title}\n<a href="{section.img_url}">&#8203;</a>\n'
        message_body = dishes[current_dish].prepare_message()
        if callback_type == 1:
            self.tgBot.sendMessage(user_id, text = message_head+message_body, parse_mode="HTML", reply_markup=createLineKeyboard(LAYOUT))
        
        else:
            self.tgBot.editMessageText(user_id, message_id = message_id, text = message_head+message_body, parse_mode="HTML", reply_markup=createLineKeyboard(LAYOUT))
    

    @csrf_exempt
    def dispatch(self, request):
        if request.method == 'GET':
            response = self.get(request)
            return response

        if request.method == 'POST':
            response = self.post(request)
            return response

    def get(self, request):
        return(HttpResponse('<h1>Ersh Api View</h1>'))
    
    def post(self, request):
        self.check_db_if_created()
        request_body = json.loads(request.body)
        print(request_body)

        sections = Section.objects.all()
        sections_name = [(section.section_title, section.section_title) for section in sections]

        callback_query = request_body.get('callback_query')
        message = request_body.get('message')
        if callback_query:
            self.callback_handler(callback_query)
        
        if message:
            user_id = message['from'].get('id')
            self.tgBot.sendMessage(user_id, text = 'Категории блюд', reply_markup = createRowKeyboard(sections_name))
            
        return(HttpResponse(200))