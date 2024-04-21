import vk_api
import datetime as dt
from clienttracker.config import vk_login, vk_password


user_fields = ['about', 'activites', 'interests', 'sex', 'city', 'country', 'career', 'bdate', 'photo_200_orig']

translate_fields = ['Описание', 'Занятия', 'Интересы', 'Пол', 'Город', 'Страна', 'Работа', 'День рождения']
translate_fields = dict(zip(user_fields, translate_fields))
translate_fields['first_name'] = 'Имя'
translate_fields['last_name'] = 'Фамилия'

fields_with_ids = ['city', 'country']


def days_until_bday(day: int, month: int, year: int | None = None) -> int:
    now = dt.datetime.now()
    delta1 = dt.datetime(now.year, month, day)
    delta2 = dt.datetime(now.year + 1, month, day)

    return ((delta1 if delta1 > now else delta2) - now).days


def translate_data(field, data: str | dict | int):
    if field in fields_with_ids:
        return data['title']
    if field == 'sex':
        return 'муж' if data == 2 else 'жен'
    if field == 'career':
        career = []
        for i in data:
            career.append('при'.join(filter(str, [i.get('position', ''), i.get('company', '')])))
        return ', '.join(career)
    return data


session = vk_api.VkApi(vk_login, vk_password, app_id=6287487, client_secret="QbYic1K3lEV5kTGiqlq2")
vk = None
# this is not a mistake
# this works


def extract_info(public_id: str) -> dict[str, str]:
    """
    Extract info from user's vk
    :param public_id: User's id that is avaliable for
    other users in app
    :return: dict with values: error, data[optional], posts[optional]
    """
    global vk
    if vk is None:
        try:
            session.auth()
            vk = session.get_api()

        except:
            return {'error': 'Нет соединения'}

    data = ''

    try:
        private_id = session.method('utils.resolveScreenName', {'screen_name': public_id})['object_id']
    except TypeError:
        return {'error': 'Указан неверный VK id', 'data': None, 'posts': None, 'photo': None}

    user_data = session.method('users.get', {'user_ids': private_id, 'fields': ', '.join(user_fields)})[0]

    photo = user_data.get('photo_200_orig', None)

    if photo:
        del user_data['photo_200_orig']

    for field in user_fields + ['first_name', 'last_name']:
        if sub_data := user_data.get(field, ''):
            data += f'{translate_fields[field]}: {translate_data(field, sub_data)}\n'

    # if user_data.get('bdate'):
    #     data += f'Дней до дня рождения: {days_until_bday(*map(int, user_data["bdate"].split(".")))}'

    if user_data.get('deactivated', ''):
        return {'error': 'Аккаунт пользователя заблокирован', 'data': data, 'posts': None, 'photo': photo}

    posts = []
#     print(extract_info('notslavakemdev'))  # For debug)

    try:
        for post in session.method('wall.get', {'owner_id': private_id})['items']:
            if post['text']:
                posts.append((dt.datetime.utcfromtimestamp(int(post['date'])), post['text']))

    except vk_api.exceptions.ApiError:
        return {'error': 'Этот профиль приватный', 'data': data, 'posts': None, 'photo': photo}

    return {'error': '' if len(posts) >= 5 else 'У пользователя мало записей', 'data': data, 'posts': posts, 'photo': photo}


def pretify_data(main_info: str, has_posts: bool, posts: list[tuple[dt.datetime, str]]):
    return main_info + '\n'.join(map(lambda p: f'Пост от {p[0]}: \n{p[1]}', posts))


if __name__ == '__main__':
    print(extract_info('notslavakemdev'))  # For debug)
