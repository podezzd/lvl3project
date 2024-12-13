
# Телеграм-бот для поддержки

Этот бот помогает пользователям задавать вопросы в службу поддержки. Он отвечает на часто задаваемые вопросы (FAQ) и передает запросы в нужный отдел.

## Возможности

- Просмотр FAQ
- Задать вопрос в отдел (например, программисты или отдел продаж)
- Сохранение запросов в базе данных

## Установка

1. Клонируй репозиторий:

   ```bash
   git clone https://github.com/yourusername/telegram-support-bot.git
   cd telegram-support-bot
   ```

2. Установи зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. В файле `config.py` вставь свой токен от бота:

   ```python
   TOKEN = 'ТВОЙ_ТОКЕН_ОТ_БОТА'
   ```

4. Запусти бота:

   ```bash
   python bot.py
   ```

## Как работает

1. Пользователь запускает бота и выбирает, что ему нужно: FAQ или задать вопрос.
2. В FAQ бот показывает список вопросов и отвечает на них.
3. В разделе «Задать вопрос» пользователь выбирает отдел (например, программисты или отдел продаж) и пишет свой вопрос.
4. Все запросы сохраняются в базе данных.

## Структура базы данных

Таблица `requests` хранит информацию о запросах:

- `id`: номер запроса
- `user_id`: ID пользователя
- `username`: имя пользователя
- `question`: текст запроса
- `department`: выбранный отдел
- `date`: время запроса

## Лицензия

Проект с лицензией MIT. Смотри файл [LICENSE](LICENSE).
