import telebot
from telebot import types
import sqlite3
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных
conn = sqlite3.connect('support_requests.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы для запросов
cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    question TEXT,
    department TEXT,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()

# FAQ (полный список)
faq = {
    "Как оформить заказ?": "Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку \"Добавить в корзину\", затем перейдите в корзину и следуйте инструкциям для завершения покупки.",
    "Как узнать статус моего заказа?": "Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел \"Мои заказы\". Там будет указан текущий статус вашего заказа.",
    "Как отменить заказ?": "Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.",
    "Что делать, если товар пришел поврежденным?": "При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.",
    "Как связаться с вашей технической поддержкой?": "Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.",
    "Как узнать информацию о доставке?": "Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки."
}

# Словарь для отслеживания состояния пользователя
user_state = {}


def send_faq_list(chat_id):
    """Отправляет список вопросов с номерами."""
    faq_text = "Выберите номер вопроса:\n"
    for i, question in enumerate(faq.keys(), start=1):
        faq_text += f"{i}. {question}\n"

    bot.send_message(chat_id, faq_text)

    # Клавиатура с номерами
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Назад")
    for i in range(1, len(faq) + 1):
        markup.add(str(i))
    bot.send_message(chat_id, "Введите номер вопроса:", reply_markup=markup)


def send_main_menu(chat_id):
    """Отправляет главное меню."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Часто задаваемые вопросы', 'Задать вопрос специалисту')
    bot.send_message(chat_id, "Чем я могу вам помочь?", reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_state[message.chat.id] = 'main_menu'  # Начальный шаг - главное меню
    send_main_menu(message.chat.id)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Обработка команды «Назад»
    if message.text == 'Назад':
        handle_back(message.chat.id)
        return  # Возвращаемся, чтобы не продолжать обработку текста как вопроса

    if message.text == 'Часто задаваемые вопросы':
        user_state[message.chat.id] = 'faq_list'  # Пользователь выбрал FAQ
        send_faq_list(message.chat.id)
    elif message.text == 'Задать вопрос специалисту':
        user_state[message.chat.id] = 'department_choice'  # Пользователь выбирает отдел
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('Программисты', 'Отдел продаж', 'Назад')  # Добавляем кнопку Назад
        bot.send_message(message.chat.id, "Кому вы хотите задать вопрос?", reply_markup=markup)
    elif message.text in ['Программисты', 'Отдел продаж']:
        department = 'Программисты' if message.text == 'Программисты' else 'Отдел продаж'
        user_state[message.chat.id] = f'question_{department}'  # Пользователь задает вопрос
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Назад")
        bot.send_message(message.chat.id, f"Введите ваш вопрос для отдела {department}:", reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: save_request(msg, department))
    elif message.text.isdigit() and int(message.text) in range(1, len(faq) + 1):
        question = list(faq.keys())[int(message.text) - 1]
        bot.send_message(message.chat.id, faq[question])


def handle_back(chat_id):
    """Возвращает пользователя на предыдущий этап диалога."""
    state = user_state.get(chat_id)
    if state is None:
        send_main_menu(chat_id)  # Если состояния нет, отправляем на главное меню
        return

    if state == 'faq_list':
        send_main_menu(chat_id)  # Возвращаем в главное меню
    elif state == 'department_choice':
        send_main_menu(chat_id)  # Возвращаем в главное меню
    elif state.startswith('question_'):
        # Возвращаем на выбор отдела, если пользователь в процессе ввода вопроса
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('Программисты', 'Отдел продаж', 'Назад')
        bot.send_message(chat_id, "Кому вы хотите задать вопрос?", reply_markup=markup)
        user_state[chat_id] = 'department_choice'  # Сохраняем новый шаг

    else:
        send_main_menu(chat_id)  # В случае ошибок возвращаем в главное меню


def save_request(message, department):
    """Сохраняет запрос в базу данных."""
    # Проверяем, не является ли сообщение "Назад"
    if message.text == 'Назад':
        handle_back(message.chat.id)
        return  # Не сохраняем запрос, а просто возвращаем на предыдущий этап

    user_id = message.from_user.id
    username = message.from_user.username
    question = message.text

    cursor.execute(
        'INSERT INTO requests (user_id, username, question, department) VALUES (?, ?, ?, ?)',
        (user_id, username, question, department)
    )
    conn.commit()

    bot.send_message(message.chat.id, f"Ваш запрос отправлен в отдел {department}. Спасибо!")
    send_main_menu(message.chat.id)  # Возвращаем в главное меню после отправки запроса


bot.polling(none_stop=True)
