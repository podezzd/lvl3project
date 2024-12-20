
# Телеграм-бот для поддержки

Этот бот помогает пользователям задавать вопросы в службу поддержки. Он отвечает на часто задаваемые вопросы (FAQ) и передает запросы в нужный отдел.

## Возможности

- Просмотр FAQ
- Задать вопрос в отдел (например, программисты или отдел продаж)
- Сохранение запросов в базе данных

## Установка

1. Клонируй репозиторий:

   ```bash
   git clone https://github.com/podezzd/lvl3project
   ```

2. В файле `config.py` вставь свой токен от бота:

   ```python
   TOKEN = 'ТВОЙ_ТОКЕН_ОТ_БОТА'
   ```

3. Запусти бота:

   ```bash
   python bot.py
   ```

## Как работает

1. Пользователь запускает бота и выбирает, что ему нужно: FAQ или задать вопрос.
![image](https://github.com/user-attachments/assets/415c6e09-7359-4ff1-919f-989436b70622)
3. В FAQ бот показывает список вопросов и отвечает на них.
![image](https://github.com/user-attachments/assets/8c572ccd-abdd-4dfa-8c51-1e051105c26c)
![image](https://github.com/user-attachments/assets/0f7bef68-66a7-4d2a-87c3-d59a916129dd)
5. В разделе «Задать вопрос» пользователь выбирает отдел (например, программисты или отдел продаж) и пишет свой вопрос.
![image](https://github.com/user-attachments/assets/be7420d0-283f-4f6e-8052-a76b3b6257e9)
7. Все запросы сохраняются в базе данных.
![image](https://github.com/user-attachments/assets/1f8c9937-7029-4a96-bb23-135585fe4045)

## Структура базы данных

Таблица `requests` хранит информацию о запросах:

- `id`: номер запроса
- `user_id`: ID пользователя
- `username`: имя пользователя
- `question`: текст запроса
- `department`: выбранный отдел
- `date`: время запроса

## Лицензия

авторы:
- ilovemarshmallow https://t.me/ilovemarshmallow
- pawpaw4ik https://t.me/pawpaw4ik
