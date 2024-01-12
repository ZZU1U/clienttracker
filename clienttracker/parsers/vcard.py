import vobject
import datetime as dt
from clienttracker.db.models import Clients, Notes


def parse_vcard(path: str, items: None | list[str] =None) -> list[dict]:
    """
    This function parses vcard files
    :param path: path to the vcard file
    :param items: items to import from vcard, default are
    full name, telephone number, category, address, birthday and note
    :return: info about each person - list[dict]
    """
    # Нам нужны fn - полное имя, tel - телефон, categories - категории, может photo - фото, note - описание/заметки,
    # adr - адресс и bgay - дата рождения

    if items is None:
        items = ['fn', 'tel', 'categories', 'adr', 'bday', 'note']

    contacts = []
    with open(path, 'r') as f:
        vcard = vobject.readComponents(f.read())

        for obj in vcard:
            print(dir(obj))
            print(*obj.getChildren())
            contacts.append({item: obj.getChildValue(item) for item in items})

    for contact in contacts:
        if contact['bday'] is not None:
            contact['bday'] = dt.datetime.strptime(contact['bday'], '%Y%m%d')

    return contacts


def vcard_to_clients(vcard_item: dict) -> tuple[Clients, (Notes | None)]:
    # TODO categories parsing f.e. - ask what categorie to add
    return Clients(first_name=vcard_item['fn'], last_name='', birthday=vcard_item['bday'], address=vcard_item['adr'],
                   phone_number=vcard_item['tel']), Notes(title='Imported from vcard', text=vcard_item['note'])
