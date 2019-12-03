import telebot


access_token ='1000855864:AAFdF7HMvV14s9rcad1gYhCRHVVcTQI6Jrk'


telebot.apihelper.proxy = {'https': 'https://104.196.138.30:3128'}

# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)


# Бот будет отвечать только на текстовые сообщения
@bot.message_handler(content_types=['text'])
def echo(message: str) -> None:
    bot.send_message(message.chat.id, message.text)



if __name__ == '__main__':
    bot.polling()
