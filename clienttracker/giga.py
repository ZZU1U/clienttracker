# -*- coding: utf-8 -*-
from gigachat import GigaChat
from config import gigachat_token

with GigaChat(credentials=gigachat_token, verify_ssl_certs=False) as giga:
    with open('output.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    response = giga.chat(f'Выведи краткую информацию о человеке:{data}В формате: ФИО, возраст, страна, город, интересы.')
    print(response.choices[0].message.content)
