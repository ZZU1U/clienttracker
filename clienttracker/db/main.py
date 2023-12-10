from clienttracker.db.queries.orm import *
from clienttracker.db.models import Clients, Purchases, SellingType, Notes


init_tables()

insert_clients([
    Clients(first_name="Gleb", last_name="Anohin"),
    Clients(first_name="John", last_name="Doe"),
    Clients(first_name="Yuri", last_name="ShapaValoV"),
    Clients(first_name="Vlad", last_name="Borisenko"),
])

insert_purchases([
    Purchases(name="Bread", client_id=2, selling_type=SellingType.Штучно,
              unit_price=30.5, unit_quantity=12),
    Purchases(name="Bread", client_id=1, selling_type=SellingType.Штучно,
              unit_price=30.5, unit_quantity=12),
    Purchases(name="Bread", client_id=2, selling_type=SellingType.Штучно,
              unit_price=30.5, unit_quantity=12)
])

insert_notes([
    Notes(text="Взять обратную связь о хлебе", client_id=1, purchase_id=2)
])

set_client(1, last_name="Cena")

print(*get_clients(), sep=', ')
