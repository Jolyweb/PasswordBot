import telebot
import os

from telebot import types

#BOT 
bot = telebot.TeleBot('YOUR TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Меня зовут <b>{1.first_name}</b>, я был создан для того, чтобы тебе было проще хранить и искать пароли".format(message.from_user, bot.get_me()), parse_mode='html')
    # bot.send_message(message.chat.id, "Ты можешь написать /help, чтобы ознакомиться с моим функционалом ближе!".format(message.from_user, bot.get_me()))
    help(message)
    
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/help - Все команды\n/create - Создание файла\n/redact - Редактирование файла\n/delete - Удаление файла\n/find - Поиск файла\n/showall - Отобразить все файлы")




#  -----------------------------------CREATE-----------------------------------------------

@bot.message_handler(commands=['create'])
def create(message):
    bot.send_message(message.chat.id, "После ввода всех данных ты получишь файл следующего формата: ")
    test_f = open('test.txt', 'rb')
    bot.send_document(message.chat.id, document=test_f, caption="Это пример!")
    bot.register_next_step_handler(message, creating_file_name)
    bot.send_message(message.chat.id, "Введите имя файла: ")

def creating_file_name(message):
    # FILE NAME IS READY
    file_name = message.text + '.txt'
    file_name = file_name.replace(' ', '').lower()
    
    # Используем "raw" строку для пути
    file_path = r"C:\vs\python\TelegramBots\qwisex_password_bot\users_data\{}.txt".format(file_name)

    # Выводим путь к файлу перед созданием
    print("Попытка создания файла по пути:", file_path)
    
    # Указываем путь к файлу в папке users_data
    file_path = os.path.join('users_data', file_name)
    
    # CREATING FILE
    new_file = open(file_path, 'w', encoding='utf-8')
    new_file.close()

    # Теперь передаем file_path обратно в функцию create
    create(message, file_path)

def create(message, file_path):
    # Получаем только название файла из полного пути
    file_name = os.path.basename(file_path)
    
    # Теперь вы можете использовать file_name в функции create
    bot.send_message(message.chat.id, f"Файл <b>{file_name}</b> успешно создан!", parse_mode='html')
    # Дальнейшее взаимодействие с файлом
    
    # CREATING LOGIN
    bot.register_next_step_handler(message, creating_login, file_path, file_name)
    bot.send_message(message.chat.id, "Введите логин:")
    
def creating_login(message, file_path, file_name):
    # Открываем файл в режиме добавления (a) для сохранения предыдущего содержимого
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"login: {message.text}\n")

    # Продолжаем с запросом пароля
    bot.register_next_step_handler(message, creating_password, file_path, file_name)
    bot.send_message(message.chat.id, "Введите пароль: ")

def creating_password(message, file_path, file_name):
    # Открываем файл в режиме добавления (a) для сохранения предыдущего содержимого
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"password: {message.text}\n")

    # Опять же, получаем только название файла из полного пути
    file_name = os.path.basename(file_path)
    
    # Лог о создании файла
    print("Файл создан по пути", file_path)
    
    bot.send_message(message.chat.id, f"Файл <b>{file_name}</b> успешно заполнен", parse_mode='html')
    bot.send_document(message.chat.id, document=open(file_path, 'rb'), caption="Ваш файл!")
    
    help(message)




# -------------------------------------------------DELETE------------------------------------------------

@bot.message_handler(commands=['delete'])
def delete(message):
    bot.send_message(message.chat.id, "Вы выбрали опцию УДАЛЕНИЯ.")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("✅")
    item2 = types.KeyboardButton("❌")
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, "Желаете продолжить?", reply_markup=markup)
    
    # Вы должны использовать проверку внутри функции обработчика, чтобы понять, что пользователь выбрал
    @bot.message_handler(func=lambda m: m.text == "✅", content_types=['text'])
    def continue_removal(message):
        bot.register_next_step_handler(message, removal_process)
        bot.send_message(message.chat.id, "Введите название файла: ")
        
    @bot.message_handler(func=lambda m: m.text == "❌", content_types=['text'])
    def back_to_menu(message):
        # Вызываем функцию меню
        help(message)

def removal_process(message):
    file_name = message.text
    file_name = file_name.replace(' ', '').lower()

    # Используем "raw" строку для пути
    file_path = r"C:\vs\python\TelegramBots\qwisex_password_bot\users_data\{}.txt".format(file_name)

    # Выводим путь к файлу перед удалением
    print("Попытка удаления файла по пути:", file_path)

    # Проверяем, существует ли файл перед удалением
    if os.path.exists(file_path):
        os.remove(file_path)
        bot.send_message(message.chat.id, f"Файл {file_name} успешно удален.")
        print("Файл удален по пути:", file_path)
        help(message)
    else:
        bot.send_message(message.chat.id, f"Файл {file_name} не найден.")
        



#----------------------------------------------REDACT-----------------------------------------------------

@bot.message_handler(commands=['redact'])
def redact(message):
    bot.send_message(message.chat.id, "Вы выбрали опцию РЕДАКТИРОВАНИЯ")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Yes")
    item2 = types.KeyboardButton("No")
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, "Желаете продолжить?", reply_markup=markup)
    
    # Вы должны использовать проверку внутри функции обработчика, чтобы понять, что пользователь выбрал
    @bot.message_handler(func=lambda m: m.text == "Yes", content_types=['text'])
    def continue_redact(message):
        bot.register_next_step_handler(message, redact_process)
        bot.send_message(message.chat.id, "Введите название файла: ")
        
    @bot.message_handler(func=lambda m: m.text == "No", content_types=['text'])
    def back_to_menu(message):
        # Вызываем функцию меню
        help(message)

def redact_process(message):
    file_name = message.text
    file_name = file_name.replace(' ', '').lower()

    # Используем "raw" строку для пути
    file_path = r"C:\vs\python\TelegramBots\qwisex_password_bot\users_data\{}.txt".format(file_name)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        print("Файл удален по пути: (REDACT)", file_path)
    else:
        bot.send_message(message.chat.id, f"Файл {file_name} не найден.")
    
    # Добавляем расширение ".txt" к пути файла после удаления
    file_path = os.path.join('users_data', f"{file_name}.txt")
    
    # CREATING FILE
    new_file = open(file_path, 'w', encoding='utf-8')
    new_file.close()
    
    re_create(message, file_path)

def re_create(message, file_path):
    # Получаем только название файла из полного пути
    file_name = os.path.basename(file_path)
    
    # Дальнейшее взаимодействие с файлом
    
    # CREATING LOGIN
    bot.register_next_step_handler(message, re_creating_login, file_path, file_name)
    bot.send_message(message.chat.id, "Введите логин:")
    
def re_creating_login(message, file_path, file_name):
    # Открываем файл в режиме добавления (a) для сохранения предыдущего содержимого
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"login: {message.text}\n")

    # Продолжаем с запросом пароля
    bot.register_next_step_handler(message, re_creating_password, file_path, file_name)
    bot.send_message(message.chat.id, "Введите пароль: ")

def re_creating_password(message, file_path, file_name):
    # Открываем файл в режиме добавления (a) для сохранения предыдущего содержимого
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"password: {message.text}\n")

    # Опять же, получаем только название файла из полного пути
    file_name = os.path.basename(file_path)
    
    # Лог о создании файла
    print("Файл создан по пути", file_path)
    
    bot.send_message(message.chat.id, f"Файл <b>{file_name}</b> успешно заполнен", parse_mode='html')
    bot.send_document(message.chat.id, document=open(file_path, 'rb'), caption="Ваш файл!")
    
    help(message)
    


#---------------------------------------------FIND FILE---------------------------------------

@bot.message_handler(commands=['find'])
def find(message):
    bot.send_message(message.chat.id, "Вы выбрали поиск файла")
    bot.register_next_step_handler(message, find_process)
    bot.send_message(message.chat.id, "Введите название файла:")

def find_process(message):
    file_name = message.text
    file_name = file_name.replace(' ', '').lower()

    # Используем относительный путь от текущей директории
    file_path = os.path.join('users_data', f"{file_name}.txt")

    # Проверяем, является ли путь файлом
    if os.path.isfile(file_path):
        bot.send_document(message.chat.id, document=open(file_path, 'rb'), caption="Ваш файл!")

        # Переносим вызов функции help в конец обработчика
        help(message)
    else:
        bot.send_message(message.chat.id, f"Файл {file_name} не найден.")
        # В случае неудачного поиска тоже вызываем help
        help(message)
        

#-------------------------------------------------SHOW ALL----------------------------------------------------

@bot.message_handler(commands=['showall'])
def show_all_files(message):
    # Задайте путь к директории
    directory_path = r"C:\vs\python\TelegramBots\qwisex_password_bot\users_data"

    # Получите список файлов в директории
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    # Если есть файлы, отправьте их пользователю
    if files:
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'rb') as file:
                bot.send_document(message.chat.id, document=file, caption=f"Файл: {file_name}")
    else:
        bot.send_message(message.chat.id, "В директории нет файлов.")
        





#--------------------------------------REMOVE ALL---------------------------------------------

@bot.message_handler(commands=['rmall'])
def remove_all_files(message):
    # Задайте путь к директории
    directory_path = r"C:\vs\python\TelegramBots\qwisex_password_bot\users_data"

    # Получите список файлов в директории
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    # Удаляем каждый файл
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        os.remove(file_path)
        print(f"Файл удален: {file_path}")

    # bot.send_message(message.chat.id, "Все файлы успешно удалены.")
    
    
# Run 
bot.polling(none_stop=True)
