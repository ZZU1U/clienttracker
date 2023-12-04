from sqlalchemy import desc
from clienttracker.db.database import sync_engine, session_factory, Base
from clienttracker.db.models import Clients, Purchases


# Insert/Create
def create_tables() -> None:
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


def insert_clients(clients: list[Clients]) -> None:
    with session_factory() as session:
        for client in clients:
            session.add(client)

        session.commit()


def insert_purchases(purchases: list[Purchases]) -> None:
    with session_factory() as session:
        for purchase in purchases:
            session.add(purchase)

        session.commit()


# Getters
def get_client_purchases(client: Clients) -> list[Purchases]:
    with session_factory() as session:
        return session.query(Purchases).where(Purchases.client_id == client.id)


def get_clients() -> list[Clients]:
    with session_factory() as session:
        return session.query(Clients).all()


def get_purchases() -> list[Purchases]:
    with session_factory() as session:
        return session.query(Purchases).order_by(desc(Purchases.purchase_date)).all()


def get_client_purchases(client: Clients) -> list[Purchases]:
    with session_factory() as session:
        return session.query(Purchases).where(Purchases.client_id == client.id).all()


def get_client_by_id(id: int) -> Clients:
    with session_factory() as session:
        return session.query(Clients).where(Clients.id == id).first()


# Setters
def set_client(id: int, **kwargs) -> None:
    with session_factory() as session:
        session.query(Clients).where(Clients.id == id).update(kwargs)

        session.commit()
