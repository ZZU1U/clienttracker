from db.crud import *
from clienttracker.db.models import Client, Purchase, SellingType, Note


init_tables()

insert_clients([
    Client(first_name="Gleb", last_name="Anohin"),
    Client(first_name="John", last_name="Doe"),
    Client(first_name="Yuri", last_name="ShapaValoV"),
    Client(first_name="Vlad", last_name="Borisenko"),
])

insert_purchases([
    Purchase(name="Bread", client_id=2, selling_type=SellingType.Штучно,
             unit_price=30.5, unit_quantity=12),
    Purchase(name="Bread", client_id=1, selling_type=SellingType.Штучно,
             unit_price=30.5, unit_quantity=12),
    Purchase(name="Bread", client_id=2, selling_type=SellingType.Штучно,
             unit_price=30.5, unit_quantity=12)
])

insert_notes([
    Note(text="Взять обратную связь о хлебе", client_id=1, purchase_id=2)
])

set_client(1, last_name="Cena")

print(*get_clients(), sep=', ')
