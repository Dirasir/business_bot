import asyncio
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot('5580790814:AAEs2urC5bCZ0vXxYSMn9ViVYhhg8-CYfIU')
moi = '1128824404'

spisok_business_connection = []

# стартовое сообщение
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.send_message(message.chat.id,
                           'Привет, я бот который позволяет следить за перепиской.\n\nПодключи меня к бизнес чату')


# обработка подключения бота в бизнес аккаунт
'''
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
    await bot.send_message('1128824404', f'@{message.chat.username} написал сообщение')

# обработка изменений
@bot.edited_business_message_handler()
async def send_edited(message):
    await bot.send_message('1128824404', f'@{message.chat.username} изменил сообщение {message.text}на {message.text}')

# обработка удалённых сообщений
@bot.deleted_business_messages_handler()
async def send_deleted(message):
    await bot.send_message('1128824404', f'@{message.chat.username} удалил сообщение {message.text}')


asyncio.run(bot.polling())
