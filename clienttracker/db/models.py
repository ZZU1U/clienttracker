# Models
import datetime as dt
from enum import Flag
from typing import Annotated, Optional
from sqlalchemy import func, ForeignKey, desc
from sqlalchemy.orm import Mapped, mapped_column, relationship
from clienttracker.db.database import Base, session_factory


intpk = Annotated[int, mapped_column(primary_key=True)]
dtnow = Annotated[dt.datetime, mapped_column(server_default=func.now())]


class SellingType(Flag):
    # For app switcher
    Развес = 0
    Штучно = 1
    Услуга = 2


class CRUD:
    def remove(self) -> None:
        with session_factory() as session:
            session.delete(self)
            session.commit()

    @staticmethod
    def insert(obj) -> None:
        with session_factory() as session:
            session.add(obj)
            session.commit()

    @staticmethod
    def insert_all(objs: list) -> None:
        with session_factory() as session:
            session.add_all(objs)
            session.commit()

    @classmethod
    def get_all(cls) -> list:
        with session_factory() as session:
            return session.query(cls).all()

    @classmethod
    def get_id(cls, id):
        with session_factory() as session:
            return session.query(cls).get(id)


class Client(Base, CRUD):
    __tablename__ = 'clients'
    id: Mapped[intpk]

    # Main info
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic_name: Mapped[str | None]
    birthday: Mapped[dt.datetime | None]
    address: Mapped[str | None]
    description: Mapped[str | None]

    # Contacts
    vk_link: Mapped[str | None]
    phone_number: Mapped[str | None]

    # Relationships
    purchases: Mapped[list["Purchase"]] = relationship(backref="client", cascade="all, delete-orphan", lazy='subquery')
    notes: Mapped[list["Note"]] = relationship(backref="client", cascade="all, delete-orphan", lazy='subquery')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Purchase(Base, CRUD):
    __tablename__ = 'purchases'
    id: Mapped[intpk]

    # Main
    name: Mapped[str]
    purchase_date: Mapped[dtnow]

    # Pricing
    selling_type: Mapped[SellingType]
    unit_name: Mapped[str] = 'шт.'
    unit_price: Mapped[float]
    unit_quantity: Mapped[float]

    # Dependencies
    client_id: Mapped["Client"] = mapped_column(ForeignKey("clients.id"))
    notes: Mapped[list["Note"]] = relationship(backref="purchase", cascade="all, delete-orphan", lazy='subquery')

    def __str__(self):
        return f'{self.name} {self.unit_quantity} {self.unit_name}'


class Note(Base, CRUD):
    __tablename__ = 'notes'
    id: Mapped[intpk]

    # Main
    title: Mapped[str]
    text: Mapped[str | None]
    date: Mapped[dt.datetime | None]

    # Dependencies
    client_id: Mapped["Client"] = mapped_column(ForeignKey("clients.id"))
    purchase_id: Mapped["Purchase"] = mapped_column(ForeignKey("purchases.id"))

    def __str__(self):
        return f'{self.title} {self.text[:10]}'
