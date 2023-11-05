import telebot
import sqlite3

from telebot import types

#BOT 
bot = telebot.TeleBot('6795326742:AAEvAwxNlhNWGzwd6uhzJhI7PEoazkhyEUM')

@bot.message_handler(commands=['start'])
def start(message):
    # KEYBORD 
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    item1 = types.KeyboardButton("❓ About")
    item2 = types.KeyboardButton("💬 Functional")
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, "Hello, {0.first_name}!".format(message.from_user, bot.get_me()),
                    parse_mode='html', reply_markup=markup)
    
    # connect = sqlite3.connect('users.db') #DATA BASE NAME
    # cursor = connect.cursor()
    
    # cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
    #     id INTEGER
    #     )""")
    # connect.commit()
    
    # #CHECK ID IN FILES 
    # people_id = message.chat.id
    # cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    # data = cursor.fetchone()
    # if data is None:
        
    #     #ADD VALUES IN FIELDS
    #     user_id = [message.chat.id]
    #     cursor.execute("INSERT INTO login_id VALUES(?);", user_id)    
    #     connect.commit()
    # else:
    #     # bot.send_message(message.chat.id, 'Такой пользователь уже существует')
        
    #     #ALTER ANSWER
    #     bot.answer_callback_query(callback_query_id=id,show_alert=False,text='Такой пользователь уже существует')

@bot.message_handler(content_types=['text'])
def function_menu(message):
    if message.chat.type == 'private':
        if message.text == "💬 Functional":
            
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(types.InlineKeyboardButton("I can"))
            markup.add(types.InlineKeyboardButton("I can too"))
            bot.send_message(message.chat.id, "tooooooooooooo", reply_markup=markup)
            
        elif message.text == "❓ About":
            bot.send_message(message.chat.id, "My name is <b>{1.first_name}</b>, I was created to conveniently save and store the information that you give me. For example, passwords and logins from your accounts. I will save them, and when you need them, I will send them here in this format: "
                             .format(message.from_user, bot.get_me()),parse_mode='html')
            test_f = open('test.txt', 'rb')
            bot.send_document(message.chat.id, document=test_f, caption="This is an example!")
        else:
            bot.send_message(message.chat.id, "Wrong input!")
            
            

# RUN
bot.polling()