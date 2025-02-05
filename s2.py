
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import json
import logging
from typing import Dict, List
import requests
from scrapegraphai.graphs import SmartScraperGraph

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_ollama_connection(model_name: str = "llama3") -> bool:
    """Проверяет доступность Ollama сервера и наличие модели"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        models = [model["name"] for model in response.json()["models"]]
        return any(model_name in name for name in models)
    except Exception as e:
        logger.error(f"Ошибка подключения к Ollama: {str(e)}")
        return False

def save_results(_data: List[Dict], 
                 _filename: str = "pizza_prices.json",
                 _fieldname: str = "пиццы") -> None:
    """Сохраняет результаты в JSON файл"""
    try:
        with open(_filename, 'w', encoding='utf-8') as f:
            json.dump(_data, f, ensure_ascii=False, indent=4)
        logger.info(f"Результаты сохранены в {_filename}")
    except Exception as e:
        logger.error(f"Ошибка при сохранении файла: {str(e)}")
        return False
    
    try:
        _csv_filename = _filename.replace('.json', '.csv')
        _df = pd.json_normalize(_data[0][_fieldname])
        _df.to_csv(_csv_filename, index=False)
        logger.info(f"Результаты сохранены в {_csv_filename}")
    except Exception as e:
        logger.error(f"Ошибка при формировании и сохранении datafame: {str(e)}")
        return False
    

def main(_endpoint="picca", 
         _key_word="пиццы", 
         _field_name = "пиццы",
         _base_uri="https://chicago-pizza.ru/catalog/"):
    # Проверка подключения к Ollama
    if not check_ollama_connection("llama3.2"):
        logger.error("Ollama сервер недоступен или модель не найдена")
        return

    _src_uri = _base_uri + _endpoint
    # Конфигурация скрейпера
    graph_config = {
        "llm": {
            "model": "ollama/llama3.2",
            "temperature": 0.1,
            "model_tokens": 8192
        },
        "verbose": True,
        "headless": True,  # Включить headless режим для продакшена
        "browser_args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
    }

    # Оптимизированный промпт для парсинга
    prompt = f"""Извлеки все {_key_word} в формате JSON с полями:
    - название: строка
    - цена: число (только цифры)
    Отфильтруй пустые значения и элементы без цены."""

    try:
        # Инициализация скрейпера
        logger.info("Запуск процесса скрейпинга...")
        smart_scraper = SmartScraperGraph(
            prompt=prompt,
            source=_src_uri,
            config=graph_config
        )

        # Выполнение скрейпинга
        result = smart_scraper.run()
        
        if not result:
            logger.warning("Не удалось извлечь данные")
            return

        # Сохранение результатов
        save_results(result if isinstance(result, list) else [result],
                     _fieldname=_field_name,
                     _filename = f"{_endpoint}_prices.json")
        
        # Вывод результатов
        logger.info("Успешно извлечено записей: %d", len(result))
        print(json.dumps(result, ensure_ascii=False, indent=4))

    except Exception as e:
        logger.error(f"Ошибка при выполнении скрейпинга: {str(e)}", exc_info=True)

if __name__ == "__main__":
    import sys
    
    endpoint = 'picca'
    key_word = 'пиццы'
    fieldname = 'пиццы'
    nn = len(sys.argv)
    if nn > 1:
        endpoint = sys.argv[1]
        if nn > 2:
            key_word = sys.argv[2]
            if nn > 3:
                fieldname = sys.argv[3]
    
    main(endpoint, key_word, fieldname)
