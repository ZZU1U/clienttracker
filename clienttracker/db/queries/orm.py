from sqlalchemy import desc, inspect
from clienttracker.db.database import sync_engine, session_factory, Base
from clienttracker.db.models import Clients, Purchases, Notes


# Base
def create_tables() -> None:
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


def init_tables() -> bool:
    if not inspect(sync_engine).has_table("clients") or \
            not inspect(sync_engine).has_table("purchases") or \
            not inspect(sync_engine).has_table("notes"):
        create_tables()
        return False

    return True


# Clients
def insert_clients(clients: list[Clients]) -> None:
    with session_factory() as session:
        for client in clients:
            session.add(client)

        session.commit()


def get_clients() -> list[Clients]:
    with session_factory() as session:
        return session.query(Clients).all()


def get_client_id_purchases(client_id: id) -> list[Purchases]:
    with session_factory() as session:
        return session.query(Purchases).where(Purchases.client_id == client_id)


def get_client_purchases(client: Clients) -> list[Purchases]:
    with session_factory() as session:
        return session.query(Purchases).where(Purchases.client_id == client.id)


def get_client_by_id(cid: int) -> Clients:
    with session_factory() as session:
        return session.query(Clients).where(Clients.id == cid).first()


def set_client(cid: int, **kwargs) -> None:
    with session_factory() as session:
        session.query(Clients).where(Clients.id == cid).update(kwargs)

        session.commit()


# Purchases
def get_purchases() -> list[Purchases]:
    with session_factory() as session:
        return session.query(Purchases).order_by(desc(Purchases.purchase_date)).all()


def insert_purchases(purchases: list[Purchases]) -> None:
    with session_factory() as session:
        for purchase in purchases:
            session.add(purchase)

        session.commit()


# Notes
def get_notes() -> list[Notes]:
    with session_factory() as session:
        return session.query(Notes).all()


def insert_notes(notes: list[Notes]) -> None:
    with session_factory() as session:
        for note in notes:
            session.add(note)

        session.commit()
