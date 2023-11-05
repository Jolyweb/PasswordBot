import telebot
import sqlite3

#BOT 
bot = telebot.TeleBot('6795326742:AAEvAwxNlhNWGzwd6uhzJhI7PEoazkhyEUM')

@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect('users.db') #DATA BASE NAME
    cursor = connect.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
        id INTEGER
        )""")
    connect.commit()
    
    #CHECK ID IN FILES 
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        
        #ADD VALUES IN FIELDS
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)    
        connect.commit()
    else:
        bot.send_message(message.chat.id, 'Такой пользователь уже существует')



@bot.message_handler(commands=['delete'])
def delete(message):
    #CONNECT DB
    connect = sqlite3.connect('users.db') 
    cursor = connect.cursor()
    
    #DELETE ID FROM TABLE 
    people_id = message.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
    connect.commit()


#POLLING
bot.polling()