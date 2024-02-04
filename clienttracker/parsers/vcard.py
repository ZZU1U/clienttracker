import vobject
import datetime as dt
from clienttracker.db.models import Client, Note


def parse_vcard(path: str, items: None | list[str] = None) -> list[dict]:
    """
    This function parses vcard files
    :param path: path to the vcard file
    :param items: items to import from vcard, default are
    full name, telephone number, category, address, birthday and note
    :return: info about each person - list[dict]
    """

    if items is None:
        items = ['fn', 'tel', 'categories', 'adr', 'bday', 'note']

    contacts = []
    with open(path, 'r') as f:
        vcard = vobject.readComponents(f.read())

        for obj in vcard:
            contacts.append({item: obj.getChildValue(item) for item in items})

    for contact in contacts:
        if contact['bday'] is not None:
            contact['bday'] = dt.datetime.strptime(contact['bday'], '%Y%m%d')
        if contact['adr'] is not None:
            contact['adr'] = str(contact['adr'])

    return contacts


def vcard_to_clients(vcard_item: dict) -> tuple[Client, (Note | None)]:
    fn = vcard_item['fn'].split()
    print(dir(vcard_item['adr']))
    print(type(vcard_item['adr']))

    return (Client(first_name=fn[0], last_name=(fn[1] if len(fn) > 1 else ''), birthday=vcard_item['bday'],
                   address=vcard_item['adr'], phone_number=vcard_item['tel']),
            Note(title=f'Записка о {vcard_item["fn"]}', text=vcard_item['note']) if vcard_item['note'] else None)
