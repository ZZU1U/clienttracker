import datetime as dt
from clienttracker.db.models import SellingType
from pydantic import BaseModel


class Clients(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic_name: str | None

    birthday: dt.datetime | None
    address: str | None
    note: str | None

    vk_link: str | None
    phone_number: str | None

    class Config:
        orm_mode = True


class Purchases(BaseModel):
    id: int
    client_id: int

    purchase_date: dt.datetime
    selling_type: SellingType

    unit_name: str
    unit_price: float
    unit_quantity: float

    class Config:
        orm_mode = True


class Notes(BaseModel):
    id: int
    title: str
    text: str
    deadline: dt.datetime

    client_id: int | None
    purchase_id: int | None

    class Config:
        orm_mode = True
