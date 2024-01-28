# Create, read, update, delete! (orm queries)
from sqlalchemy import desc, inspect
from clienttracker.db.database import sync_engine, session_factory, Base
from clienttracker.db.models import Client, Purchase, Note


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
def insert_clients(clients: list[Client]) -> None:
    with session_factory() as session:
        for client in clients:
            session.add(client)

        session.commit()


def get_clients() -> list[Client]:
    with session_factory() as session:
        return session.query(Client).all()


def get_client_id_purchases(client_id: id) -> list[Purchase]:
    with session_factory() as session:
        return session.query(Purchase).where(Purchase.client_id == client_id).order_by(Purchase.purchase_date).all()


def get_client_purchases(client: Client) -> list[Purchase]:
    return get_client_id_purchases(client.id)


def get_client_by_id(cid: int) -> Client:
    with session_factory() as session:
        return session.query(Client).get(cid)


def delete_client(client: Client) -> None:
    with session_factory() as session:
        session.delete(client)
        session.commit()


# Purchases
def get_purchases() -> list[Purchase]:
    with session_factory() as session:
        return session.query(Purchase).order_by(desc(Purchase.purchase_date)).all()


def insert_purchases(purchases: list[Purchase]) -> None:
    with session_factory() as session:
        for purchase in purchases:
            session.add(purchase)

        session.commit()


def get_purchase_by_id(pid: int) -> Purchase:
    with session_factory() as session:
        return session.query(Purchase).get(pid)


def get_products() -> list[str]:
    with session_factory() as session:
        return session.query(Purchase.name).distinct().all()


# Notes
def get_notes() -> list[Note]:
    with session_factory() as session:
        return session.query(Note).all()


def insert_notes(notes: list[Note]) -> None:
    with session_factory() as session:
        for note in notes:
            session.add(note)

        session.commit()
