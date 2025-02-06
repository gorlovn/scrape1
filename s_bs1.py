#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

# Настройка заголовков для имитации браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# URL страницы с пиццей
url = 'https://chicago-pizza.ru/catalog/picca'

# Отправка GET-запроса
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Создание объекта BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Поиск всех карточек товаров
    pizza_cards = soup.find_all('div', class_='flex min-h-0 grow flex-col gap-1 p-2 lg:gap-2.5 lg:p-3')
    
    # Список для хранения результатов
    pizza_list = []
    
    for card in pizza_cards:
        try:
            # Извлечение названия
            name = card.find('div', class_='line-clamp-3 break-words pb-0.5 !leading-none lg:text-lg').text.strip()
            
            # Извлечение цены
            price = card.find('div', class_='whitespace-nowrap !leading-none text-lg lg:text-xl').find('div').text.strip()
            
            pizza_list.append({'Название': name, 'Цена': price})
            
        except AttributeError as e:
            print(f'Ошибка при парсинге карточки: {e}')
    
    # Вывод результатов
    for idx, pizza in enumerate(pizza_list, 1):
        print(f"{idx}. {pizza['Название']} - {pizza['Цена']}")

else:
    print(f'Ошибка при загрузке страницы. Код статуса: {response.status_code}')