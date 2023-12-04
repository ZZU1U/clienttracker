import datetime as dt
from enum import Flag
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from clienttracker.db.database import Base


class SellingType(Flag):
    # For app switcher
    BY_WEIGHT = True
    BY_PIECE = False


class Clients(Base):
    __tablename__ = 'clients'
    id: Mapped[int] = mapped_column(primary_key=True)

    # Main info
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic_name: Mapped[str | None]
    birthday: Mapped[str | None]
    address: Mapped[str | None]
    note: Mapped[str | None]

    # Contacts
    vk_link: Mapped[str | None]
    phone_number: Mapped[str | None]

    # Dates
    first_purchase_date: Mapped[dt.datetime] = mapped_column(server_default=func.now())
    last_purchase_date: Mapped[dt.datetime] = mapped_column(server_default=func.now())
    purchases_count: Mapped[int] = 1

    def __str__(self):
        return f'[{self.id}] {self.first_name} {self.last_name}'


class Purchases(Base):
    __tablename__ = 'purchases'
    id: Mapped[int] = mapped_column(primary_key=True)

    # Main
    client_id: Mapped[int] = mapped_column(ForeignKey(Clients.id, ondelete='CASCADE'))
    name: Mapped[str]
    purchase_date: Mapped[dt.datetime] = mapped_column(server_default=func.now())

    # Pricing
    selling_type: Mapped[SellingType]
    unit_price: Mapped[float]
    unit_quantity: Mapped[float]

    def __str__(self):
        return f'({self.id}) <- [{self.client_id}]: {self.name}, {self.unit_price}Р x{self.unit_quantity}, {self.purchase_date}'
