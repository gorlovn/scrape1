# Проект scrape1
Парсинг страниц сайта с ценами с использованием ИИ посредством библиотеки [scrapegraphai](https://github.com/ScrapeGraphAI/Scrapegraph-ai)

## Управление проектом
Управление проектом (установка зависимостей) осуществляется с использованием менеджера зависимостей [UV](https://github.com/astral-sh/uv)

### Установка UV

```shell
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```shell
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Установка в Windows зависимостей с использованием pip

Установка rust: https://www.rust-lang.org/tools/install

В командной строке (`cmd`) в папке с проектом

```shell
python -m venv .venv
.venv\Scripts\activate.bat
pip install scrapegraphai
pip install requests
pip install pandas
pip install openpyxl
playwright install
```

## Использование LLM 
Для запуска больших языковых моделей (LLM) используется фреймворк [Ollama](https://ollama.ai/).
Парсинг веб страниц выполняется с использованием модели `llama3.2`.

Необходимо установить фреймворк загрузив его для соответствующей операционной системы с официального сайта.
После установки фреймворка необходимо скачать языковую модель:
```shell
ollama pull llama3.2
```

## Запуск в Windows
В командной строке (`cmd`) в папке с проектом

```shell
.venv\Scripts\activate.bat
python s2.py seti
```

Вторым аргументом можно задать название модели.
Предварительно модель нужно загрузить на компьютер:
```shell
ollama pull model
```
По умолчанию используется модель `llama3.2`.

Список доступных моделей смотреть здесь: https://ollama.com/library

Список локально загруженных моделей:
```shell
ollama list
```
Удалить загруженную модель:
```shell
ollama rm model
```
