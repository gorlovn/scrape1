import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import logging
from typing import Dict, List

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_bs4.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Настройка заголовков для имитации браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# URL страницы с пиццей
base_url = 'https://chicago-pizza.ru/catalog/'
endpoint = 'picca'

def save_results(_data: List[Dict], 
                 _filename: str = "pizza_prices.json") -> None:
    """Сохраняет результаты в JSON и XLSX файлы"""
    try:
        with open(_filename, 'w', encoding='utf-8') as f:
            json.dump(_data, f, ensure_ascii=False, indent=4)
        logger.info(f"Результаты сохранены в {_filename}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении файла: {str(e)}")
        return None
    
    try:
        _xlsx_filename = _filename.replace('.json', '.xlsx')
        _df = pd.DataFrame(_data)
        _df.to_excel(_xlsx_filename, index=False)
        logger.info(f"Результаты сохранены в {_xlsx_filename}")
        return _df
    except Exception as e:
        logger.error(f"Ошибка при формировании и сохранении dataframe: {str(e)}")
        return None

url = base_url + endpoint
# Отправка GET-запроса
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Создание объекта BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Поиск всех карточек товаров
    _cards = soup.find_all('div', class_='flex min-h-0 grow flex-col gap-1 p-2 lg:gap-2.5 lg:p-3')
    
    # Список для хранения результатов
    _list = []
    
    for card in _cards:
        try:
            # Извлечение названия
            _class_name = 'line-clamp-3 pb-0.5 leading-none! break-words lg:text-lg'
            name_element = card.find('div', class_=_class_name)
            if name_element:
                name = name_element.text.strip()
            else:
                logger.warning(f'Не найден элемент с названием: {_class_name}')
                continue  # Пропускаем эту карточку, если название не найдено            
            
            # Извлечение цены
            _class_name = 'leading-none! whitespace-nowrap text-lg lg:text-xl'
            price_container = card.find('div', class_=_class_name)
            if price_container:
                price_element = price_container.find('div')
                if price_element:
                    price = price_element.text.strip()
                else:
                    logger.warning(f'Не найден дочерний элемент с ценой: {_class_name}')
                    continue  # Пропускаем эту карточку, если цена не найдена
            else:
                logger.warning(f'Не найден контейнер с ценой')
                continue  # Пропускаем эту карточку, если цена не найдена            
            
            _list.append({'Название': name, 'Цена': price})
            
        except AttributeError as e:
            logger.error(f'Ошибка при парсинге карточки: {e}')
            
    # Сохранение результатов
    df = save_results(_list, f"{endpoint}_prices.json")
    
    # Вывод результатов
    for idx, card in enumerate(_list, 1):
        print(f"{idx}. {card['Название']} - {card['Цена']}")

else:
    logger.error(f'Ошибка при загрузке страницы. Код статуса: {response.status_code}')