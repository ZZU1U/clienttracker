# Models
import datetime as dt
from enum import Flag
from typing import Annotated, Optional
from sqlalchemy import func, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base, session_factory


intpk = Annotated[int, mapped_column(primary_key=True)]
dtnow = Annotated[dt.datetime, mapped_column(server_default=func.now())]


class SellingType(Flag):
    # For app switcher
    Развес = 0
    Штучно = 1
    Услуга = 2


class CRUD:
    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

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
    purchases: Mapped[list["Purchase"]] = relationship(
        lazy='selectin',
        back_populates='client',
        cascade='all, delete-orphan',
    )
    notes: Mapped[list["Note"]] = relationship(
        lazy='selectin',
        back_populates='client',
        cascade='all, delete-orphan',
    )

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
    client_id: Mapped[int] = mapped_column(
        ForeignKey(
            "clients.id",
            ondelete="CASCADE",
        )
    )
    client: Mapped["Client"] = relationship(
        lazy='joined',
        back_populates='purchases',
    )
    notes: Mapped[list["Note"]] = relationship(
        lazy='selectin',
        back_populates='purchase',
        cascade='all, delete-orphan',
    )

    def __str__(self):
        return f'{self.name} ({self.unit_quantity} {self.unit_name}) {self.purchase_date.strftime("%d.%m")}'


class Note(Base, CRUD):
    __tablename__ = 'notes'
    id: Mapped[intpk]

    # Main
    title: Mapped[str]
    text: Mapped[str | None]
    date: Mapped[dt.datetime | None]

    # Dependencies
    client_id: Mapped[int] = mapped_column(
        ForeignKey(
            "clients.id",
            ondelete="CASCADE"
        )
    )
    purchase_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "purchases.id",
            ondelete="CASCADE"
        )
    )
    client: Mapped["Client"] = relationship(
        lazy='joined',
        back_populates='notes'
    )
    purchase: Mapped["Purchase"] = relationship(
        lazy='joined',
        back_populates='notes'
    )

    def __str__(self):
        return f'{self.title}'
