import telebot
import config


telebot.apihelper.proxy = {'https': 'https://23.237.173.102:3128'}

# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(config.token)


# Бот будет отвечать только на текстовые сообщения
@bot.message_handler(content_types=['text'])
def echo(message: str) -> None:
    bot.send_message(message.chat.id, message.text)



if __name__ == '__main__':
    bot.polling(none_stop = True)

