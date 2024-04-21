from gigachat import GigaChat
from clienttracker.config import gigachat_token


giga = GigaChat(credentials=gigachat_token, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")


def get_giga(data: str, quest: str) -> str: 
    """
    Extract info from user's vk
    :param data: Info about user, generates from vk
    :param quest: User's prompt
    :return: llm answer
    """
    response = giga.chat(f'Ответь на вопрос "{quest}", исходя из следующей информации о клиенте:\n"{data[:8000]}"')
    return response.choices[0].message.content


def get_giga_for_data(data: dict, quest: str):
    inp = data['data'] + '\n' + '\n'.join((map(lambda e: str(e[0]) + ': ' + e[1].replace('\n', ''),data['posts'])))

    return get_giga(inp, quest)

if __name__ == '__main__':
    response = giga.chat('Hello, World!')
    print(response.choices[0].message.content)
