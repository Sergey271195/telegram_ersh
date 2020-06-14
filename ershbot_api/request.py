import requests
from bs4 import BeautifulSoup
import re
import json

from .views import Section, Dish

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
        print('Title:', section_title)
        if len(all_keys) == 3:
            additional_info = all_keys[2]
            print('Info:', additional_info)
        print('Img src:', img_src)

        for dish_title in menu_dict[key]:
            print('DISH_TITLE', dish_title)
            prop, price = 0, 0
            info_dict = {'type_1': '', 'price_1': '', 'type_2': '', 'price_2': '', 'type_3': '', 'price_3': '', 'type_4': '', 'price_4': ''}
            for dish_info in menu_dict[key][dish_title]:
                if ' руб.' in dish_info:
                    price+= 1
                    info_dict[f'price_{price}'] = int(re.sub(r' руб.', '', dish_info))
                else:
                    prop+= 1
                    info_dict[f'type_{prop}'] = dish_info

            print(info_dict)
    
