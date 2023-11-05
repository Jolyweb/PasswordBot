import telebot

from telebot import types

#BOT 
bot = telebot.TeleBot('6795326742:AAEvAwxNlhNWGzwd6uhzJhI7PEoazkhyEUM')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Меня зовут <b>{1.first_name}</b>, я был создан для того, чтобы тебе было проще хранить и искать пароли".format(message.from_user, bot.get_me()), parse_mode='html')
    bot.send_message(message.chat.id, "Ты можешь написать /help, чтобы ознакомиться с моим функционалом ближе!".format(message.from_user, bot.get_me()))
    
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/help - Все команды\n/create - Создание файла\n/redact - Редактирование файла\n/delete - Удаление файла\n/find - Поиск файла\n/showall - Отобразить все файлы")

@bot.message_handler(commands=['create'])
def create(message):
    bot.send_message(message.chat.id, "После ввода всех данных ты получишь файл следующего формата: ")
    test_f = open('test.txt', 'rb')
    bot.send_document(message.chat.id, document=test_f, caption="Это пример!")
    
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton("Введи название")
    # item2 = types.KeyboardButton("Создание логина")
    # item3 = types.KeyboardButton("Создание пароля")
    # item4 = types.KeyboardButton("Дополнительная информация")
    # markup.add(item1, item2, item3)
    
    bot.send_message(message.chat.id, "Для прекращения процесса создания просто выбери другой пункт из меню")

@bot.message_handler(content_types=['text'])
def creating(message):
    if message.chat.type == 'private':
        file_name = ""
        if message.text == "Введи название":
            sent = bot.send_message(message.chat.id, "Введите название файла: ")
            bot.register_next_step_handler(sent, create_file_name)
            
    def create_file_name(message):
        message_to_save = message.text
        message_to_save = message_to_save + '.txt' 
        

    # def create_login(message):
    #     massage_to_save = message.text
    #     pass
    

    # def create_password(message):
    #     pass

    # def create_description(message):
    #     pass 
    

#RUN
bot.polling(none_stop=True)    