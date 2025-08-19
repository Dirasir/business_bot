import asyncio
from telebot.async_telebot import AsyncTeleBot
import sqlite3
import datetime
import schedule
import time
import threading

bot = AsyncTeleBot('5580790814:AAEs2urC5bCZ0vXxYSMn9ViVYhhg8-CYfIU')
moi = '1128824404'
name_db = "db_message.db"


# стартовое сообщение
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.send_message(message.chat.id,
                           'Привет, я бот который позволяет следить за перепиской.\n\nПодключи меня к бизнес чату')


# обработка подключения бота в бизнес аккаунт
'''
spisok_business_connection = []

@bot.business_connection_handler()
async def proverka_connect(message):
    if message.id not in spisok_business_connection:
        await bot.send_message('1128824404', 'бот подключён')
        spisok_business_connection.append(message.id)
    else:
        await bot.send_message('1128824404', 'бот отключён')
        spisok_business_connection.remove(message.id)
'''


# обработка сообщения
@bot.business_message_handler()
async def send_message(message):
    # запись сообщения в бд
    con = sqlite3.connect(name_db)
    cur = con.cursor()
    cur.execute(
        f"""INSERT INTO text_message(id_chat,id_message,time,text) VALUES ({message.chat.id},{message.id},{datetime.datetime.now().toordinal()},"{message.text}")""")
    con.commit()
    con.close()


# обработка изменений
@bot.edited_business_message_handler()
async def send_edited(message):
    con = sqlite3.connect(name_db)
    cur = con.cursor()
    qwe = cur.execute(
        f"""SELECT * FROM text_message WHERE id_chat = '{message.chat.id}' AND id_message = {message.id}""").fetchone()[
        3]
    cur.execute(f"""UPDATE text_message SET text = '{message.text}' WHERE id_message = {message.id}""")
    con.commit()
    con.close()
    await bot.send_message('1128824404', f'@{message.chat.username} изменил сообщение:\n{qwe} -> {message.text}')


# обработка удалённых сообщений
@bot.deleted_business_messages_handler()
async def send_deleted(message):
    con = sqlite3.connect(name_db)
    cur = con.cursor()
    for message_id in message.message_ids:
        qwe = cur.execute(
            f"""SELECT * FROM text_message WHERE id_chat = '{message.chat.id}' AND id_message = {message_id}""").fetchone()[
            3]
        cur.execute(f"""DELETE FROM text_message WHERE id_message = {message_id}""")
        con.commit()
        await bot.send_message('1128824404', f'@{message.chat.username} удалил сообщение:\n{qwe}')

    con.close()


# удаление старых сообщений каждый день
def delete_old_message():
    print("Delete")
    date_now = datetime.datetime.now().toordinal()
    con = sqlite3.connect(name_db)
    cur = con.cursor()
    cur.execute(f"""DELETE FROM text_message WHERE time <= {date_now - 7}""")
    con.commit()
    con.close()

def plane():
    schedule.every(1).days.do(delete_old_message)
    while True:
        schedule.run_pending()
        time.sleep(1000)

threading.Thread(target=plane, daemon=True).start()

asyncio.run(bot.polling())
