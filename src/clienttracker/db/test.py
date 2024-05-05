from .models import Purchase, Client, Note, session_factory, SellingType
from .database import create_tables


def test_data():
    create_tables()
    with session_factory() as session:
        andrew = Client(
            first_name="Андрей",
            last_name="Кузьмин",
            address='Кемерово',
            vk_link='reverselelush158'
        )

        me = Client(
            first_name='Глеб',
            last_name='Анохин',
            address='Кузбасс',
            description='Защищает проект',
            vk_link='etoslozhn0',
            phone_number='+78005553535',
        )

        van = Client(
            first_name='Иван',
            last_name='Петров'
        )

        banan = Purchase(
            name='Бананы',
            selling_type=SellingType.Штучно,
            unit_price=12,
            unit_quantity=10,
            client=andrew,
        )

        note = Note(
            client=andrew,
            purchase=banan,
            title='Понравился банан',
            text='Андрей хотел зайти купить еще'
        )
        session.add_all([andrew, me, van, banan, note])
        session.commit()
