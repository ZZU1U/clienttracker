import datetime as dt
from enum import Flag
from typing import Annotated
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from clienttracker.db.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
dtnow = Annotated[dt.datetime, mapped_column(server_default=func.now())]


class SellingType(Flag):
    # For app switcher
    Развес = False
    Штучно = True


class Client(Base):
    __tablename__ = 'clients'
    id: Mapped[intpk]

    # Main info
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic_name: Mapped[str | None]
    birthday: Mapped[dt.datetime | None]
    address: Mapped[str | None]
    note: Mapped[str | None]

    # Contacts
    vk_link: Mapped[str | None]
    phone_number: Mapped[str | None]

    # Purchases
    purchases: Mapped[list["Purchase"]] = relationship(backref='client')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Purchase(Base):
    __tablename__ = 'purchases'
    id: Mapped[intpk]

    # Main
    client_id: Mapped[int] = mapped_column(ForeignKey(Client.id, ondelete='CASCADE'))
    name: Mapped[str]
    purchase_date: Mapped[dtnow]

    # Pricing
    selling_type: Mapped[SellingType]
    unit_name: Mapped[str] = 'шт.'
    unit_price: Mapped[float]
    unit_quantity: Mapped[float]

    def __str__(self):
        return f'{self.name} {self.unit_quantity} {self.unit_name}'


class Note(Base):
    __tablename__ = 'notes'
    id: Mapped[intpk]

    # Main
    title: Mapped[str]
    text: Mapped[str | None]
    date: Mapped[dt.datetime | None]

    # Dependencies
    client_id: Mapped[int | None] = mapped_column(ForeignKey(Client.id, ondelete='CASCADE'))
    purchase_id: Mapped[int | None] = mapped_column(ForeignKey(Purchase.id, ondelete='CASCADE'))

    def __str__(self):
        return f'{self.title} {self.text[:10]}'
