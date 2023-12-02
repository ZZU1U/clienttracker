from sqlalchemy import text, insert
from database import sync_engine, session_factory
from models import metadata_obj, Clients


def create_tables():
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)


def view_table():
    with session_factory() as session:
        print(session.info())


def insert_data():
    client = Clients(first_name='gleb', second_name='anohin', patronymic_name='alekseevich', phone_number='+7-(952)-173-14-00', note='he\'s dumb', address='Kemerovo', birthday='1999', vk_link='etoslozhn0')

    with session_factory() as session:
        session.add(client)
