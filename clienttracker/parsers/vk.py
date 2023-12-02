import vk_api
from pprint import pprint

token = "vk1.a.XWWlQua-hAaP4e_BhkFD-xTglojbnCpc4_m8iJXToKbonQ8B3uD4o5rm61Z-gYpm52W-DPaiJiOmbhQrqc-BLHhZIpn_LzN_9V9UF7un925z78hSnJJEtHtC-7RkSk712c1o_P_CrsXjgxtSiM_0CUARLJt5sn1k2iURcYo-f96UCskBMAbalyf7FyzNycuqhi2_KEKhFSwvLmSqbbCnXw"
user_id = "531852925"

user_fields = ['about', 'personal', 'interests', 'schools', 'sex', 'education', 'city', 'country', 'career', 'bdate']

session = vk_api.VkApi(token=token)

vk = session.get_api()

friends = session.method('friends.get', {})['items']

guys = ['slavakemdev']

with open('../output.txt', 'w+',encoding='utf-8') as f:


    for guy in guys:
        guy = session.method('utils.resolveScreenName', {'screen_name': guy})['object_id']

        user_data = session.method('users.get', {'user_ids': guy, 'fields': ', '.join(user_fields)})[0]
        for field in ['first_name', 'last_name'] + user_fields:
            if (data := user_data.get(field, '')):
#                print(f'{field}: {data}', file=f)
                pass

        if user_data.get('deactivated', ''):
            continue

        for post in session.method('wall.get', {'owner_id': guy})['items']:
            if post['text']: print(post['text'], file=f)
