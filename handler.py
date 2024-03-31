from funk import *
from config import *
import logging
import json
import telebot
from telebot import types
from config import TOKEN
from ya_gpt import *
from YaGpt_with_tokens import count_tokens
with open('output.json', 'r') as file:
    DATA_BASE_USERS = json.load(file)
    print(DATA_BASE_USERS)
DATA_BASE = {}
with open('CONST.json', 'r') as file:
    DATA_BASE = json.load(file)

with open('CONST.json', 'w') as file:
    json.dump(DATA_BASE, file)
# константы проекта
MAX_USERS = 2
USER = DATA_BASE['USERS']
MAX_SESION = 3
TOKEN_PROJECT = 9500


#
# настройка логинга
# Настройка журналирования
#завершено не трогать
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
#завершено не трогать
stats = { 0: 'start',
          1: "Выбор жанра",
          2: "Выбор персонажа",
          3: "Выбор локации",
          4: "пожелание",
          5: "генерация",
          6: "Чёрный список"
          }

def tokens_bot():
    bot_token = DATA_BASE['ALL_TOKENS']
    if bot_token >= 9400:
        for userid in DATA_BASE_USERS:
            userinfo = DATA_BASE_USERS[userid]
            print(f"User ID: {userid}")
            print(f"User Info: {userinfo}")
            DATA_BASE_USERS[str(userid)]['const']['state'] = stats[6]
token = TOKEN
bot = telebot.TeleBot(token=token)


#завершено не трогать
setings = {'seting1': """Кибер-RPG: Главный герой оказывается виртуальном мире, который напоминает компьютерную ролевую игру.""",
           'seting2': """Мир Краха: Этот сеттинг представляет собой постапокалиптический мир, где главный герой сталкивается с разрушением, хаосом и опасностями. Ресурсы ограничены, а люди вынуждены бороться за выживание.""",
           'seting3': """Мистические земли: Этот сеттинг представляет собой уникальный и загадочный мир, наполненный магией, чудесами и тайнами. На этих землях существуют древние расы, обладающие удивительными способностями и знаниями.""",}

#завершено не трогать
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.chat.id
    tokens_bot()
    json_str = json.dumps(DATA_BASE_USERS)
    print(json_str)
    bot.send_message(user_id, f'''Приветствую это бот генератор сценариев по имени Generarium.
    Давайте выберем жанр истории. Все тексты сделаны с использованием нейросетей. чтоб начать писать историю /new_story
    чтобы закончить /end пока что у вас огранченое количество историй сгененерировать можно только 3.''')
    if int(DATA_BASE['USERS']) <= MAX_USERS :
        if str(user_id) not in json_str:
            f = DATA_BASE['USERS']
            g = f + 1
            DATA_BASE['USERS'] = g
            DATA_BASE_USERS[str(user_id)] = {'const': {'token': 0, 'session': 0, 'state': stats[0]},
                                          'promt': {'gpt_promts': '', 'system_promts': '', 'user_promt': ''},
                                             'history': {'genre': '', 'setting': '', 'character': '', 'user_txt': ''}}

            print(json_str)
        with open('output.json', 'w') as file:
            json.dump(DATA_BASE_USERS, file)
        with open('CONST.json', 'w') as file:
            json.dump(DATA_BASE, file)

        user_stats = DATA_BASE_USERS[str(user_id)]['const']['state']

    else:
        bot.send_message(user_id, "Прошу прошения но у вас нету доступак данному телеграм боту ")



    if user_stats != stats[6]:
        bot.send_message(user_id,"Вам разрешено в доступе")
    else:
        bot.send_message(user_id, "Просим прошения вы не можете воспользоваться ботом вы потратили все сессии или вам отказано в доступе ")


# завершено не трогать
@bot.message_handler(commands=['new_story'])
def story(message):
    user_id = message.chat.id
    user_session = DATA_BASE_USERS[str(user_id)]['const']['session']
    ost_session = MAX_SESION - user_session
    user_stats = DATA_BASE_USERS[str(user_id)]['const']['state']
    if user_stats != stats[6]:
        if user_session == MAX_SESION:
            bot.send_message(user_id, "Ваши сессии подошли к концу вам больше нельзя генерировать истории >:(!")
            DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[6]

        elif user_session < MAX_SESION:
            if user_stats == stats[0]:
                bot.send_message(user_id,
                                 f"Отлично у вас осталось {ost_session}. Cессии снимаются когда у вас в одной сессии будет 1500 токенов это максимум для одной сессии или когда вы завершите написание истории командой /end")
                seting(user_id)
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[1]
                with open('output.json', 'w') as file:
                    json.dump(DATA_BASE_USERS, file)

            else:
                bot.send_message(user_id, "Прошу прошения вы либо выбираете данные либо генерируете историю завершите прошлые действия сначало")


    else:
        bot.send_message(user_id, "Просим прошения вы не можете воспользоваться ботом вы потратили все сессии или вам отказано в доступе ")
    tokens_bot()

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    user_stats = DATA_BASE_USERS[str(user_id)]['const']['state']
    if user_stats != stats[6]:
        if user_stats == stats[1]:
            if call.data == 'Post-Apocalyptic':
                bot.send_message(user_id, "Ваш сетинг истории Постапокалипсис")
                characters(user_id)
                DATA_BASE_USERS[str(user_id)]['history']['genre'] = 'Постапокалпсис'
                print(DATA_BASE_USERS[str(user_id)]['history']['genre'])
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[2]
                with open('output.json', 'w') as file:
                    json.dump(DATA_BASE_USERS, file)
            elif call.data == 'Fantasy':
                bot.send_message(user_id, "Ваш сетинг истории Фентези")
                characters(user_id)
                DATA_BASE_USERS[str(user_id)]['history']['genre'] = 'Фентези'
                print(DATA_BASE_USERS[str(user_id)]['history']['genre'])
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[2]
                with open('output.json', 'w') as file:
                    json.dump(DATA_BASE_USERS, file)
            elif call.data == 'Science Fictionk':
                bot.send_message(user_id, "Ваш сетинг истории Научная фантастика")
                characters(user_id)
                DATA_BASE_USERS[str(user_id)]['history']['genre'] = 'Научная фантастика'
                print(DATA_BASE_USERS[str(user_id)]['history']['genre'])
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[2]
                with open('output.json', 'w') as file:
                    json.dump(DATA_BASE_USERS, file)
        elif user_stats == stats[2]:
            pass
            if call.data == 'characters1':
                DATA_BASE_USERS[str(user_id)]['history']['character'] = 'Найла - отважная воительница своего племени'
                print(DATA_BASE_USERS[str(user_id)]['history']['character'])
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[3]
                bot.send_message(user_id,
                                 f"отлично вы выбрали персонажа {DATA_BASE_USERS[str(user_id)]['history']['character']} отличный выбор.")
                with open('output.json', 'w') as file:
                    json.dump(DATA_BASE_USERS, file)
                    seting_history(user_id)
            elif call.data == 'characters2':
                DATA_BASE_USERS[str(user_id)]['history']['character'] = 'Арагорн из властелина колец'
                print(DATA_BASE_USERS[str(user_id)]['history']['character'])
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[3]
                bot.send_message(user_id,f"отлично вы выбрали персонажа {DATA_BASE_USERS[str(user_id)]['history']['character']} отличный выбор.")
                with open('output.json', 'w') as file:
                    json.dump(DATA_BASE_USERS, file)
                    seting_history(user_id)
            elif call.data == 'characters3':
                DATA_BASE_USERS[str(user_id)]['history']['character'] = 'Боб Хой главный герой из фильма шпион по соседству'
                print(DATA_BASE_USERS[str(user_id)]['history']['character'])
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[3]
                bot.send_message(user_id,
                                 f"отлично вы выбрали персонажа {DATA_BASE_USERS[str(user_id)]['history']['character']} отличный выбор.")
                with open('output.json', 'w') as file:
                    json.dump(DATA_BASE_USERS, file)
                    seting_history(user_id)
            elif call.data == 'characters4':
                DATA_BASE_USERS[str(user_id)]['history']['character'] = 'Эллен Рипли из чужого'
                print(DATA_BASE_USERS[str(user_id)]['history']['character'])
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[3]
                bot.send_message(user_id,
                                 f"отлично вы выбрали персонажа {DATA_BASE_USERS[str(user_id)]['history']['character']} отличный выбор.")
                with open('output.json', 'w') as file:
                    json.dump(DATA_BASE_USERS, file)
                    seting_history(user_id)
        elif user_stats == stats[3]:
            if call.data == "seting1" or call.data == "seting2" or call.data == "seting3":

                DATA_BASE_USERS[str(user_id)]['history']['setting'] = setings[call.data]
                prompt = create_prompt(DATA_BASE_USERS,user_id)
                bot.send_message(user_id,f"""Отлично ваш промт для истории
             
{prompt} 

для продолжения либо напишите пожелание либо /create""")
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[4]
            else:
                bot.send_message(user_id,"Вы нажали не на ту кнопку прошу используйте кнопки которые вам предоставлены на этой стадии")
            print(call.data)

            with open('output.json', 'w') as file:
                json.dump(DATA_BASE_USERS, file)




    else:
        bot.send_message(user_id, "Просим прошения вы не можете воспользоваться ботом вы потратили все сессии или вам отказано в доступе ")
    tokens_bot()

#завершено не трогать
@bot.message_handler(commands=['debag'])
def antibag(message):
    user_id = message.chat.id
    user_stats = DATA_BASE_USERS[str(user_id)]['const']['state']
    if user_stats != stats[6]:
        try:
            logging.info('функция debager работает')
            bot.send_message(user_id, "вам отправлен файлс логингом ошибок удачи вам :)")
            # Отправка файла "exemple"
            file_name = '/example.log'
            with open(file_name, 'rb') as file:
                antibag = file
                bot.send_document(user_id, antibag)
        except:
            logging.debug('тут надо подправить это функция debager')

    else:
        bot.send_message(user_id, "Просим прошения вы не можете воспользоваться ботом вы потратили все сессии или вам отказано в доступе ")
    tokens_bot()

# завершено
@bot.message_handler(commands=['create'])
def create(message):
    user_id = message.chat.id
    user_stats = DATA_BASE_USERS[str(user_id)]['const']['state']
    user_token = DATA_BASE_USERS[str(user_id)]['const']['token']
    bot_token = DATA_BASE["ALL_TOKENS"]
    if user_stats == stats[4]:
        DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[5]
        prompt = create_prompt(DATA_BASE_USERS, user_id)
        with open('output.json', 'w') as file:
            json.dump(DATA_BASE_USERS, file)
        with open('CONST.json', 'w') as file:
            json.dump(DATA_BASE, file)
        try:
            tokens = count_tokens(prompt)
            if tokens >= 300:
                bot.send_message(user_id,"Ваш изначальный промт превышает максимально допустимый в начале запроса к gpt. Начните заново /start")
                DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[0]
            else:
                pass
        except:
            tokens = "Приношу извенения пока что просчёт токенов невозможен! "
        bot.send_message(user_id,f"Количество потраченых токенов при первом запросе {tokens} ожидайте генерацию")
        if tokens == "Приношу извенения пока что просчёт токенов невозможен! ":
            DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[4]
            with open('output.json', 'w') as file:
                json.dump(DATA_BASE_USERS, file)
            bot.send_message(user_id,"Приносим большие извинения произрошла ошибка в токенизации или генерации ответа попробуйте сново")
        else:
            if user_stats == stats[4]:
                prompts = create_prompt(DATA_BASE_USERS, user_id)
                tokens_users_promt = count_tokens(prompts)
                collection = [{'role': 'user', 'content': prompts, 'assistant_text': prompt}]  # Начинаем собирать данные для запроса.

                # Первый запрос для продолжения истории.
                response = ask_gpt(collection, mode='continue')
                print(f"Первое продолжение истории от YandexGPT:\n{response}\n")

                try:
                    if response == "Произошла непредвиденная ошибка.":
                        bot.send_message(user_id,"Просим прошения при генерации запроса произошла ошибка попробуйте заново")
                        DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[4]
                        with open('output.json', 'w') as file:
                            json.dump(DATA_BASE_USERS, file)
                    else:
                        token = count_tokens(response)
                        user_token = DATA_BASE_USERS[str(user_id)]['const']['token']
                        plus_token = tokens + token
                        DATA_BASE_USERS[str(user_id)]['const']['token'] = plus_token

                        bot.send_message(user_id,f"Отлично первая часть истории готова \n{response}\n токенов в обшем затрачено {DATA_BASE_USERS[str(user_id)]['const']['token']} чтобы продолжить напишите переход к продолжению")
                        promts = prompt +" "+ response
                        DATA_BASE_USERS[str(user_id)]['promt']['user_promt'] = promts
                        session_user_token = tokens + token + tokens_users_promt
                        botplus_token = bot_token + session_user_token
                        DATA_BASE['ALL_TOKENS'] = botplus_token
                        with open('output.json', 'w') as file:
                            json.dump(DATA_BASE_USERS, file)
                        with open('CONST.json', 'w') as file:
                            json.dump(DATA_BASE, file)

                except:
                    bot.send_message(user_id,f"Прошу прошения вам следует начать с начала!")
                    DATA_BASE_USERS[str(user_id)]['const']['state'] = stats[0]

            else:

                bot.send_message(user_id,f"Вы сейчас на стадии {user_stats} прошу когда вам не предлагают не трогайте эту команду ")


    else:
        bot.send_message(user_id,f"Вы сейчас на стадии {user_stats} прошу когда вам не предлагают не трогайте эту команду ")
    tokens_bot()

#завершено
@bot.message_handler(commands=['end'])
def end_ya_gpt(message):
    user_id = message.chat.id
    user_stats = DATA_BASE_USERS[str(user_id)]['const']['state']
    user_tokens = DATA_BASE_USERS[str(user_id)]['const']['token']
    user_session = DATA_BASE_USERS[str(user_id)]['const']['session']
    if user_tokens >= 1300:

        user_session = user_session + 1
        ost_session = MAX_SESION - user_session
        bot.send_message(user_id, f"вы наврятле сможете завершить историю с таким количеством потраченых токенов ваши токены сгорели у вас осталось{ost_session}")
        DATA_BASE_USERS[str(user_id)]['const']['state'] = 'start'
        DATA_BASE_USERS[str(user_id)]['const']['session'] = user_session
        DATA_BASE_USERS[str(user_id)]['const']['token'] = 0
        with open('output.json', 'w') as file:
            json.dump(DATA_BASE_USERS, file)
    if user_stats == stats[5]:
        prompt = DATA_BASE_USERS[str(user_id)]['promt']['user_promt']
        token_in_prompt = count_tokens(prompt)
        if user_tokens + token_in_prompt > 1300:
            user_session = user_session + 1
            ost_session = MAX_SESION - user_session
            bot.send_message(user_id,
                             f"вы не сможете завершить историю с таким количеством потраченых токенов ваши токены сгорели у вас осталось {ost_session}")
            DATA_BASE_USERS[str(user_id)]['const']['state'] = 'start'
            DATA_BASE_USERS[str(user_id)]['const']['session'] = user_session
            DATA_BASE_USERS[str(user_id)]['const']['token'] = 0
            with open('output.json', 'w') as file:
                json.dump(DATA_BASE_USERS, file)
        else:
            bot.send_message(user_id,"Ожидайте генерацию :)")
            prompts = create_prompt(DATA_BASE_USERS, user_id)
            tokens_users_promt = count_tokens(prompts)
            collection = [{'role': 'user', 'content': prompts, 'assistant_text': prompt}]
            response = ask_gpt(collection, mode='end')
            print(f"Завершение истории от YandexGPT:\n{response}\n")
            bot.send_message(user_id, f"Отлично ваша история готова."
                                      f"Завершение истории от YandexGPT:\n{response}\n")
            tokens = count_tokens(response)
            bot_token = DATA_BASE['ALL_TOKENS']
            botplus_token = bot_token + tokens + token_in_prompt + tokens_users_promt
            DATA_BASE['ALL_TOKENS'] = botplus_token
            with open('CONST.json', 'w') as file:
                json.dump(DATA_BASE, file)
            user_session = DATA_BASE_USERS[str(user_id)]['const']['session']
            user_session = user_session + 1
            ost_session = MAX_SESION - user_session
            bot.send_message(user_id, f"вы завершили написание истории у вас осталось сессий {ost_session}")

            DATA_BASE_USERS[str(user_id)] = {'const': {'token': 0, 'session': 0, 'state': stats[0]},
                                          'promt': {'gpt_promts': '', 'system_promts': '', 'user_promt': ''},
                                             'history': {'genre': '', 'setting': '', 'character': '', 'user_txt': ''}}
            DATA_BASE_USERS[str(user_id)]['const']['session'] = user_session

            with open('output.json', 'w') as file:
                json.dump(DATA_BASE_USERS, file)
    tokens_bot()


#завершено не трогать
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, """Приветствую я телеграм бот Generarium мои команды 
/help - выводит дополнительную информацию о боте
/new_story - начинает создание истории
/create - начинает генерацию истории
/end - завершает генерацию истории
я создан для генерации историй во мне есть заложеные сетинги перснажи и жанры расказы будут иникальными поскольку я использую для их создания нейро сеть.""")
    tokens_bot()

#протестировать
@bot.message_handler(content_types=['text'])
def gpts(message):
    user_id = message.chat.id
    user_stats = DATA_BASE_USERS[str(user_id)]['const']['state']
    user_tokens = DATA_BASE_USERS[str(user_id)]['const']['token']

    if user_tokens >= 500:
        bot.send_message(user_id, "Ваш промт скоро составит половину от допустимого в сессии сессии советую скорее завершить историю конец может быть не сгенерирован!")


    if user_stats == stats[5]:
        prompt = DATA_BASE_USERS[str(user_id)]['promt']['user_promt']

        prompt = prompt + ' ' + message.text
        DATA_BASE_USERS[str(user_id)]['promt']['user_promt'] = prompt
        with open('output.json', 'w') as file:
            json.dump(DATA_BASE_USERS, file)
        prompt = DATA_BASE_USERS[str(user_id)]['promt']['user_promt']
        token_in_prompt = count_tokens(prompt)

        if user_tokens >= 600:
            bot.send_message(user_id," оно слишком большое перейди к функции /end")
        else:
            prompts = create_prompt(DATA_BASE_USERS, user_id)
            tokens_users_promt = count_tokens(prompts)
            DATA_BASE_USERS[str(user_id)]['const']['token'] = token_in_prompt
            collection = [{'role': 'user', 'content': prompts, 'assistant_text': prompt}]
            bot.send_message(user_id, "Ожидайте генерацию :)")
            response = ask_gpt(collection, mode='continue')
            promts = prompt + ' ' + response
            print(collection)
            DATA_BASE_USERS[str(user_id)]['promt']['user_promt'] = promts
            prompt = DATA_BASE_USERS[str(user_id)]['promt']['user_promt']
            tokens = count_tokens(prompt)
            print(f"Второе продолжение истории от YandexGPT:\n{response}\n")
            bot.send_message(user_id,f"Второе продолжение истории от YandexGPT:\n{response}\n ваши токены которые вы потратили  за этот запрос {tokens} вы можете продолжить или завершить историю /end советую всёже не затягивать и не писат войну и мир токенов всего 1500 на  1 историю")
            token_response = count_tokens(response)
            new_tokens = user_tokens + tokens + token_response + tokens_users_promt
            DATA_BASE_USERS[str(user_id)]['const']['token'] = new_tokens
            bot_token = DATA_BASE['ALL_TOKENS']
            response_prompt = count_tokens(response)
            botplus_token = bot_token + token_in_prompt + response_prompt
            DATA_BASE['ALL_TOKENS'] = botplus_token
            with open('CONST.json', 'w') as file:
                json.dump(DATA_BASE, file)
            user_session = DATA_BASE_USERS[str(user_id)]['const']['session']

            with open('output.json', 'w') as file:
                json.dump(DATA_BASE_USERS, file)

    elif user_stats == stats[4]:
        user_txt = message.text
        DATA_BASE_USERS[str(user_id)]['history']['user_txt'] = user_txt
        with open('output.json', 'w') as file:
            json.dump(DATA_BASE_USERS, file)
        bot.send_message(user_id,"Отлично ваше пожелание сохранено чтобы начать генерацию истории /create а если хотите изменить пожелание просто напишите его заново.")
    else:
        print(user_stats)
        bot.send_message(user_id,"Прошу прошения но у вас сейчас другое дело займитесь им :)")
    tokens_bot()



bot.polling()
