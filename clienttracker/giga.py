from gigachat import GigaChat
from clienttracker.config import gigachat_token

giga = GigaChat(credentials=gigachat_token, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")


def get_giga(data: str):
    print('-'*100)
    response = giga.chat(f'Выпиши актуальные интересы и увлечения данного человека через запятую, исходя из следующей информации о нем:\n"{data[:8000]}"')
    return response.choices[0].message.content

