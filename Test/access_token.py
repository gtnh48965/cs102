import telebot
import config 

access_token ='1000855864:AAFdF7HMvV14s9rcad1gYhCRHVVcTQI6Jrk'


telebot.apihelper.proxy = {'https': 'https://104.196.138.30:3128'}
bot = telebot.TeleBot(access_token)


if __name__ == '__main__':
    bot.polling()
