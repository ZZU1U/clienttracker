import vk_api
import datetime as dt
from clienttracker.config import vk_token


user_fields = ['about', 'activites', 'interests', 'sex', 'city', 'country', 'career', 'bdate']
# TODO Add activities - Деятельность

translate_fields = ['описание', 'занятия', 'интересы', 'пол', 'город', 'страна', 'работа', 'дата рождения']
translate_fields = dict(zip(user_fields, translate_fields))
translate_fields['first_name'] = 'имя'
translate_fields['last_name'] = 'фамилия'

fields_with_ids = ['city', 'country']


def translate_data(field, data: str | dict | int):
    if field in fields_with_ids:
        return data['title']
    if field == 'sex':
        return 'муж' if data == 2 else 'жен'
    if field == 'career':
        return ', '.join([i['position'] for i in data])
    return data


session = vk_api.VkApi(token=vk_token)

vk = session.get_api()


def extract_info(public_id: str) -> tuple[str, bool, None | list[tuple[dt.datetime, str]]]:
    """
    Extract info from user's vk
    :param public_id: User's id that is avaliable for
    other users in app
    :return: Tuple of russified info string,
    boolean flag if account is deactivated or not,
    because if it's deactivated then it has not posts,
    and None if no posts, or list of tuples of date and post text
    """

    data = ''

    private_id = session.method('utils.resolveScreenName', {'screen_name': public_id})['object_id']

    user_data = session.method('users.get', {'user_ids': private_id, 'fields': ', '.join(user_fields)})[0]
    for field in user_fields + ['first_name', 'last_name']:
        if sub_data := user_data.get(field, ''):
            data += f'{translate_fields[field]}: {translate_data(field, sub_data)}\n'

    if user_data.get('deactivated', ''):
        return data, True, None

    posts = []

    for post in session.method('wall.get', {'owner_id': private_id})['items']:
        if post['text']:
            posts.append((dt.datetime.utcfromtimestamp(int(post['date'])), post['text']))

    return data, False, posts


if __name__ == '__main__':
    print(extract_info('notslavakemdev'))  # For debug)
