import requests
import logging
from transformers import AutoTokenizer
from ya_gpt import *

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(message)s")



GPT_MODEL = 'yandexgpt'



# Раньше было так
# def count_tokens(prompt):
#     tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")  # название модели
#     return len(tokenizer.encode(prompt))


# Теперь подсчитывать токены необходимо вот так
def count_tokens(text: str) -> int:
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    return len(
        requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",
            json={"modelUri": f"gpt://{folder_id}/yandexgpt/latest", "text": text},
            headers=headers
        ).json()['tokens']
    )

