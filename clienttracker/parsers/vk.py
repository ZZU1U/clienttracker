import vk_api
from clienttracker.config import vk_token


user_fields = ['about', 'interests', 'sex', 'city', 'country', 'career', 'bdate']
# TODO Add activities - Деятельность

translate_fields = ['описание', 'интересы', 'пол', 'город', 'страна', 'работа', 'дата рождения']
translate_fields = dict(zip(user_fields, translate_fields))
translate_fields['first_name'] = 'имя'
translate_fields['last_name'] = 'фамилия'

fields_with_ids = ['city', 'country']


def retranslate_data(field, data: str | dict | int):
    if field in fields_with_ids:
        return data['title']
    if field == 'sex':
        return 'муж' if data == 2 else 'жен'
    if field == 'career':
        return ', '.join([i['position'] for i in data])
    return data


session = vk_api.VkApi(token=vk_token)

vk = session.get_api()


def guys_to_str(guys: list) -> list[str]:
    info = []

    for guy in guys:
        guy_str = ''

        guy = session.method('utils.resolveScreenName', {'screen_name': guy})['object_id']

        user_data = session.method('users.get', {'user_ids': guy, 'fields': ', '.join(user_fields)})[0]
        for field in user_fields + ['first_name', 'last_name']:
            if (data := user_data.get(field, '')):
                guy_str += f'{translate_fields[field]}: {retranslate_data(field, data)}\n'

        if user_data.get('deactivated', ''):
            continue

        guy_str += 'посты данного пользователя:\n'

        for post in session.method('wall.get', {'owner_id': guy})['items']:
            if post['text']:
                guy_str += post['text'] + '\n'

        info.append(guy_str)

    return info
