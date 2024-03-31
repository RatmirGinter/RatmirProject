import requests
import logging
from config import *
# Константы
SYSTEM_PROMT = SYSTEM_CONTENT_BOT
CONTINUE_STORY = 'Продолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = 'Напиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'




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


# Функция создает промт для начала истории, используя выбор пользователя (жанр, герой и т.п.)
# Принимает два параметра: user_data (словарь данных от пользователей)
# и user_id (id конкретного пользователя)
def create_prompt(user_data, user_id):
    # Начальный текст для нашей истории - это типа вводная часть
    prompt = SYSTEM_PROMT

    # Добавляем в начало истории инфу о жанре и главном герое, которых выбрал пользователь
    prompt += (f"\nНапиши начало истории в стиле {user_data[str(user_id)]['history']['genre']} "
              f"с главным героем {user_data[str(user_id)]['history']['character']}. "
              f"Вот начальный сеттинг: \n{user_data[str(user_id)]['history']['setting']}. \n"
              "Начало должно быть коротким, 1-3 предложения.\n")

    # Если пользователь указал что-то еще в "дополнительной информации", добавляем это тоже
    if user_data[str(user_id)]['history']['user_txt']:
        prompt += (f"Также пользователь попросил учесть "
                   f"следующую дополнительную информацию: {user_data[str(user_id)]['history']['user_txt']} ")

    # Добавляем к prompt напоминание не давать пользователю лишних подсказок
    prompt += 'Не пиши никакие подсказки пользователю, что делать дальше. Он сам знает'

    # Возвращаем сформированный текст истории
    return prompt

# Функция для запроса к YandexGPT
def ask_gpt(collection, mode='continue',):
    """Запрос к YandexGPT"""

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt/latest",
        "completionOptions": {"stream": False, "temperature": 0.6, "maxTokens": MAX_TOKENS},
        "messages": []
    }

    for row in collection:
        content = row['content']
        if mode == 'continue' and row['role'] == 'user':
            content += '\n' + CONTINUE_STORY
        elif mode == 'end' and row['role'] == 'user':
            content += '\n' + END_STORY
        data["messages"].append({"role": row["role"], "text": content})
        data["messages"].append({"role": 'system', "text": SYSTEM_CONTENT_BOT})
        data["messages"].append({"role": 'assistant', "text": row['assistant_text']})

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return f"Status code {response.status_code}."
        return response.json()['result']['alternatives'][0]['message']['text']
    except Exception as e:
        return "Произошла непредвиденная ошибка."



