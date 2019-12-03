import requests
import telebot
from telebot import apihelper
from bs4 import BeautifulSoup
import datetime
from typing import List, Tuple
import config

telebot.apihelper.proxy = config.proxy
token = config.token

no_les='пар нет'
no_group ='Нет токой группы '
no_write = 'Неправильный ввод '
now = datetime.datetime.now()
bot = telebot.TeleBot(token)
no_building ='Напиши правильно '
day_p = ['monday',
         'tuesday',
         'wednesday',
         'thursday',
         'friday',
         'saturday',
         'sunday']


cache = dict()  # кэш


def day_number():
    return datetime.datetime.today().weekday()+1


def namber_week():
    return now.strftime("%u")

def get_parity(day: datetime.date) -> int:
    """ Возвратить четность недели для данной даты """
    first_day = datetime.date(datetime.date.today().year, 9, 1)
    if day.month < 9:
        first_day = datetime.date(datetime.date.today().year - 1, 9, 1)
    if first_day.weekday() == 6:
        # если 1 сентября приходится на воскресенье, первым днем считается 2 сентября
        first_day = datetime.date(datetime.date.today().year, 9, 2)
    else:
        while first_day.weekday() != 0:
            # нахождение понедельника недели, содержащей 1 сентября
            first_day.day = first_day.day - 1
    dataa = day - first_day
    return -1 * ((dataa.days // 7) % 2 - 2)




def get_page(group: str, week:str='') ->str:

    if week == '0':
        week = ''
    if week:
        week = str(week) + '/'
    url = '{domain}/0/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain = config.dom,
        group = group,
        week = week)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_weekday(web_page : str, day: str) -> Tuple[list, list,  List[str]]:

    soup = BeautifulSoup(web_page, "html5lib")

    if day == '1':
        day = 'monday'
    if day == '2':
        day = 'tuesday'
    if day == '3':
        day = 'wednesda'
    if day == '4':
        day = 'thursday'
    if day == '5':
        day = 'friday'
    if day == '6':
        day = 'saturday'
    if day == '7':
        day = 'sunday'


    if day == 'monday':
        schedule_table = soup.find("table", attrs={"id": "1day"})
    if day == 'tuesday':
        schedule_table = soup.find("table", attrs={"id": "2day"})
    if day == 'wednesda':
        schedule_table = soup.find("table", attrs={"id": "3day"})
    if day == 'thursday':
        schedule_table = soup.find("table", attrs={"id": "4day"})
    if day == 'friday':
        schedule_table = soup.find("table", attrs={"id": "5day"})
    if day == 'saturday':
        schedule_table = soup.find("table", attrs={"id": "6day"})
    if day == 'sunday':
        schedule_table = soup.find("table", attrs={"id": "7day"})

    # Получаем таблицу с расписанием
    #schedule_table = soup.find("table", attrs={"id": day_p})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    '''''    #Номер аудитории
    aud_list = schedule_table.find("td", attrs={"class": "time"}).find_all('dd', attrs={"class": "rasp_aud_mobile"})
    aud_list = [aud.dd.text for aud in aud_list]
    '''
    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"},)
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list ,lessons_list






@bot.message_handler(commands={'monday':1, 'tuesday':2, 'wednesda':3, 'thursday':4, 'friday':5, 'saturday':6, 'sunday':7})
def get_schedule(message):
    """ Получить расписание на указанный день """
    # PUT YOUR CODE HERE

    if len(message.text.split()) == 2:
        day= message.text
        day=day[1:]
        day=day.split()
        days=day[0]
        group = day[1]
        week = '0'
    if len(message.text.split()) == 3:
        day = message.text
        day = day[1:]
        day = day.split()
        days = day[0]
        group = day[1]
        week = day[2]
    web_page = get_page(group, week)
    times_lst, locations_lst, lessons_lst =\
        parse_schedule_for_a_weekday(web_page, days)
    resp = ''

    for time, location,  lession in zip(times_lst, locations_lst,   lessons_lst):
        resp += '<b>{}</b>, {},{}\n'.format(time, location, lession)
    return bot.send_message(message.chat.id, resp, parse_mode='HTML')









@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    if len(message.text.split())==2:
        _, group = message.text.split()
        day = day_number()
        days = datetime.datetime.today().date()

        time= datetime.datetime.today().time()
        week = get_parity(days)
        hour = time.hour
        chec = False
        minutes = time.minute
        if day ==7:
            day=1
        web_page = get_page(group,week)
        parse = parse_schedule_for_a_weekday(web_page, str(day))
        times_lst, locations_lst, lessons_lst = parse
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            if hour < int(time[6:8]) or (hour == int(time[6:8]) and minutes < int(time[9:11])):
                # если текущее время меньше времени конца пары, выводится эта пара
                resp = 'Ближайшая пара:\n\n<b>Cегодня</b>\n\n'
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
                chec = True
                break

        if chec==True:
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        else:
            day=day+1
            parse = parse_schedule_for_a_weekday(web_page, str(day))
            while parse == None:
                if(day<6):
                    day +=1
                    parse = parse_schedule_for_a_weekday(web_page,str(day))
                else:
                    day=0
                    week = -(week - 3)
                    web_page = get_page(group, week)
                    parse = parse_schedule_for_a_weekday(web_page, str(day))
                resp = 'Ближайшая пара: '
                times_lst, locations_lst, lessons_lst = parse
                for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    break


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    # PUT YOUR CODE HERE

    day = day_number()
    _, group = message.text.split()
    if len(message.text.split()) == 2:
        if day == 1:
            day ='monday'
        elif day ==2:
            day ='tuesday'
        elif day == 3:
            day = 'wednesday'
        elif day ==4:
            day = 'thursday'
        elif day==5:
            day = 'friday'
        elif day==6:
            day = 'saturday'
        elif day==7:
            return bot.send_message(message.chat.id, no_les, parse_mode='HTML')

        week = get_parity(datetime.date.today())
        week = str(week)
        web_page = get_page(group, week)
        if web_page:

            pars = parse_schedule_for_a_weekday(web_page, day)
            if pars:
                times_lst, locations_lst, lessons_lst = pars
                resp = ''
                for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
                return bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """

    # PUT YOUR CODE HERE

    if 2 <= len(message.text.split()) <= 3:
        if len(message.text.split()) == 2:
            _, group = message.text.split()
            web_page = get_page(group)

        else:
            _, week, group = message.text.split()
            group = group.capitalize()
            web_page = get_page(group, week)

        if web_page:
            resp = ''
            for i in range(6):
                pars = parse_schedule_for_a_weekday(web_page, str(i + 1))
                resp += '\n<b>{}</b>\n\n'.format(day_p[i + 1])
                if pars:
                    times_lst, locations_lst, lessons_lst = pars
                    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    return bot.send_message(message.chat.id, resp, parse_mode='HTML')



if __name__ == '__main__':
    bot.polling(none_stop=True)


