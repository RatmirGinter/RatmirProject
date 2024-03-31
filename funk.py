import telebot
from telebot import types
from config import TOKEN
import sqlite3
import logging
import os
token = TOKEN
bot = telebot.TeleBot(token=token)
#
# настройка логинга
# Настройка журналирования
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Создание обработчика для записи логов в файл с кодировкой UTF-8
file_handler = logging.FileHandler('example.log', mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Добавление обработчика в корневой логгер
root_logger = logging.getLogger()
root_logger.addHandler(file_handler)

logging.info('Это сообщение уровня INFO логирование настроено можно продолжать')

# тадамс


def seting(user_id):

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Постапокалипсис", callback_data='Post-Apocalyptic'),
               types.InlineKeyboardButton("Фэнтези", callback_data='Fantasy'),
               types.InlineKeyboardButton("Научная фантастика", callback_data='Science Fictionk'))

    bot.send_message(user_id,"""Приветствую! В этом боте представлены различные жанры:

- Постапокалипсис (Post-Apocalyptic): Мир после глобальной катастрофы, борьба за выживание, разрушенные города, нехватка ресурсов.
  
- Фэнтези (Fantasy): Мир с магией, волшебством, героями, эльфами, драконами, эпические приключения и загадочные земли.

- Научная фантастика (Science Fiction): Будущее, технологии, инопланетяне, примеры - 'Звездный путь' и 'Матрица'.""",reply_markup=markup)


def characters(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Найла", callback_data='characters1'),
               types.InlineKeyboardButton("Арагорн", callback_data='characters2'),
               types.InlineKeyboardButton("Боб Хой.- Джеки Чан", callback_data='characters3'),
               types.InlineKeyboardButton("Эллен Рипли", callback_data='characters4'))

    bot.send_message(user_id, """Приветствую! В этом боте представлены различные главные герои вот их список:

- 1 Найла - отважная воительница из древнего воинского клана, обученная искусству меча и стратегии. 
Ее цель - защищать свою землю от врагов и вернуть утраченную славу своему народу.

- Арагорн - персонаж из "Властелина колец" Дж. Р. Р. Толкина. 
Наследник королей Гондора и Арнора, последний из рейнгов Данедаинов.

- В фильме "Шпион по соседству" ("The Spy Next Door") Джеки Чан играл персонажа по имени Боб Хой. Он исполнил роль бывшего агента ЦРУ, 
который вынужден столкнуться с опасностью и использовать свои навыки шпионажа, чтобы защитить своих соседей и их детей..

- Эллен Рипли - главная героиня франшизы "Чужой" (Alien), которую исполняет актриса Сигурни Уивер. В первом фильме "Чужой" (1979) Рипли является одним из членов экипажа космического корабля "Ностромо".

Часть персонажей выбрана и добавлена с помощью GPT создателем бота.""",
                     reply_markup=markup)


def seting_history(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Кибер-RPG", callback_data='seting1'),
               types.InlineKeyboardButton("Мир краха", callback_data='seting2'),
               types.InlineKeyboardButton("Мистические земли", callback_data='seting3'))

    bot.send_message(user_id, """Приветствую! В этом боте представлены различные сетинги истории:

- Кибер-RPG: Главный герой оказывается виртуальном мире, который напоминает компьютерную ролевую игру.

- Мир Краха: Этот сеттинг представляет собой постапокалиптический мир, где главный герой сталкивается с разрушением, хаосом и опасностями. Ресурсы ограничены, а люди вынуждены бороться за выживание.

- Мистические земли: Этот сеттинг представляет собой уникальный и загадочный мир, наполненный магией, чудесами и тайнами. На этих землях существуют древние расы, обладающие удивительными способностями и знаниями.""",
                     reply_markup=markup)





