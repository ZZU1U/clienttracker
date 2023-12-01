import vobject
import datetime as dt


def parse_vcard(path, items=['fn', 'tel', 'categories', 'adr', 'bday', 'note']):
    """
    This function parses vcard files
    :param path: path to the vcard file
    :param items: items to import from vcard, default are
    full name, telephone number, category, address, birthday and note
    :return: info about each person - list[dict]
    """
    # Нам нужны fn - полное имя, tel - телефон, categories - категории, может photo - фото, note - описание/заметки, adr - адресс и bgay - дата рождения
    contacts = []
    with open(path, 'r') as f:
        vcard = vobject.readComponents(f.read())
        for obj in vcard:
            contacts.append({item: obj.getChildValue(item) for item in items})

    for contact in contacts:
        if contact['bday'] is not None:
            contact['bday'] = dt.datetime.strptime(contact['bday'], '%Y%m%d')

    return contacts
