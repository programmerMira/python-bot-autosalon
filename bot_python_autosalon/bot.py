import telebot
import config
from db import SQLighter
import random
from telebot import types
import time

bot = telebot.TeleBot(config.TOKEN)

#welcome message
@bot.message_handler(commands=['start'])
def welcome(message):   
    db_worker = SQLighter(config.database_name)
    username = str(message.chat.username)
    print("Your username is "+username)
    db_worker.insert_client(username)
    db_worker.close()
    bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ твой персональный помощник <b>{1.first_name}</b> для помощи при выборе вида починки.".format(message.from_user, bot.get_me()), parse_mode="html")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start\n/help\n/view_servises \n/add_order [order number] \n/view_my_orders".format(parse_mode="html"))

@bot.message_handler(commands=['admin_help'])
def admin_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/add_service [title, duration, cost]\n/view_orders \n/view_clients".format(parse_mode="html"))

@bot.message_handler(commands=['add_service'])
def add_service(message):
    msg_text = message.text.replace("/add_service","").strip().replace(" ","")
    msg_text_arr = msg_text.split(",")#CHECK IF LEN<3
    if len(msg_text_arr)==3:
        db_worker = SQLighter(config.database_name)
        db_worker.insert_service(msg_text_arr[0], msg_text_arr[1], msg_text_arr[2])
        db_worker.close()
        bot.send_message(message.chat.id,"<i><b>Сервис добавлен!</b></i>", parse_mode="html")
    else:
        bot.send_message(message.chat.id,"<i>Неверные входные данные</i>", parse_mode="html")

@bot.message_handler(commands=['view_servises'])
def view_servises(message):
    db_worker = SQLighter(config.database_name)
    db_log=db_worker.select_all_services()
    log="Номер - Услуга - Время - Стоимость\n\n"
    for db_log_single in db_log:
        for tmp in db_log_single:
            log += "".join(str(tmp))+"  "
        log+="\n"
    db_worker.close()
    bot.send_message(message.chat.id,"<i><b>Доступные услуги:\n</b>"+log+"</i>", parse_mode="html")

@bot.message_handler(commands=['add_order'])
def add_order(message):
    msg_text = message.text.replace("/add_order","").strip().replace(" ","")
    if len(msg_text)>0:
        db_worker = SQLighter(config.database_name)
        db_worker.insert_order(message.chat.username,msg_text)
        db_worker.close()
        bot.send_message(message.chat.id, "<i>«Услуга была добавлена.»</i>", parse_mode="html")
    else:
        bot.send_message(message.chat.id,"<i>Неверные входные данные</i>", parse_mode="html")

@bot.message_handler(commands=['view_my_orders'])
def view_my_orders(message):
    db_worker = SQLighter(config.database_name)
    db_log=db_worker.select_user_orders(message.chat.username)
    log=""
    for db_log_single in db_log:
        for tmp in db_log_single:
            log += "".join(str(tmp))+"  "
        log+="\n"
    db_worker.close()
    bot.send_message(message.chat.id,"<i><b>Заказы пользователя "+message.chat.username+":\n</b>"+log+"</i>", parse_mode="html")

@bot.message_handler(commands=['view_orders'])
def view_orders(message):
    db_worker = SQLighter(config.database_name)
    db_log=db_worker.select_all_orders()
    log=""
    for db_log_single in db_log:
        for tmp in db_log_single:
            log += "".join(str(tmp))+"  "
        log+="\n"
    db_worker.close()
    bot.send_message(message.chat.id,"<i><b>Все текущие заказы:\n</b>"+log+"</i>", parse_mode="html")

@bot.message_handler(commands=['view_clients'])
def view_clients(message):
    db_worker = SQLighter(config.database_name)
    db_log=db_worker.select_all_clients()
    log=""
    for db_log_single in db_log:
        for tmp in db_log_single:
            log += "".join(str(tmp))+"  "
        log+="\n"
    db_worker.close()
    bot.send_message(message.chat.id,"<i><b>Все текущие клиенты:\n</b>"+log+"</i>", parse_mode="html")

#menu replies  
@bot.message_handler(content_types=['text'])
def lalala(message):
    bot.send_message(message.chat.id, "<i>«Извините, я ограничен в ответах.»</i>", parse_mode="html")
    help(message)


#RUN
while True:
    try:
        print("[*] bot starting..")
        #bot.send_message(owner, "[*] bot starting..")
        print("[*] bot started!")
        #bot.send_message(owner, "[*] bot started!")
        bot.polling(none_stop=True, interval=2)
        # Предполагаю, что бот может мирно завершить работу, поэтому
        # даем выйти из цикла
        break

    except Exception as ex:
        print("[*] error - {}".format(str(ex))) # Описание ошибки
        #bot.send_message(owner, "[*] error - {}".format(str(ex)))
        print("[*] rebooting..")
        #bot.send_message(owner, "[*] rebooting..")
        bot.stop_polling()
        # Останавливаем чтобы не получить блокировку
        time.sleep(15)
        print("[*] restarted!")
        #bot.send_message(owner, "[*] restarted!")