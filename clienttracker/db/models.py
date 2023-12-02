from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

metadata_obj = MetaData()


class Clients(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    second_name: Mapped[str]
    patronymic_name: Mapped[str]
    phone_number: Mapped[str]
    note: Mapped[str]
    address: Mapped[str]
    birthday: Mapped[str]
    vk_link: Mapped[str]
