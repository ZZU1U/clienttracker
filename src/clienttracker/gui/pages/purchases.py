import flet as ft

from ..components.purchase_item import purchase_to_item
from ...db.models import Purchase, SellingType, Client
from ...config import get_service
from flet import (
    Row,
    Column,
    Container,
    Text,
    TextField,
    DatePicker,
    icons,
    AlertDialog,
    ElevatedButton,
    IconButton,
    colors,
)
from ..utils.object_methods import *


def update_fields(parent):
    unit_name = parent.unit_name.value
    parent.unit_price.disabled = False
    parent.unit_quantity.disabled = False
    parent.unit_quantity.suffix = Text('шт.') if parent.selling_type.value == 'Штучно' else Text(unit_name)
    parent.unit_price.label = f'Стоимость {"штуки" if parent.selling_type.value == "Штучно" else unit_name}'
    parent.unit_quantity.label = "Количество " + ("штук" if parent.selling_type.value == "Штучно" else unit_name)
    parent.unit_quantity.value = 1 if parent.selling_type.value == 'Штучно' else None
    parent.unit_name.disabled = parent.selling_type.value == 'Штучно'

    parent.page.update()


def init_values(parent):
    parent.product_name = TextField(label='Название', autofocus=True, enable_suggestions=True)
    parent.selling_type = ft.Dropdown(
        label='Тип продажи',
        options=[
            ft.dropdown.Option('Штучно'),
            ft.dropdown.Option('Развес'),
        ],
        on_change=lambda e: update_fields(parent)
    )
    parent.unit_price = TextField(label='', keyboard_type=ft.KeyboardType.NUMBER, suffix=Text('₽'), disabled=True)
    parent.unit_quantity = TextField(label='', keyboard_type=ft.KeyboardType.NUMBER, disabled=True)
    parent.unit_name = TextField(
        label='Название единицы',
        hint_text='кг',
        disabled=True,
        on_change=lambda e: update_fields(parent)
    )
    parent.purchase_date = DatePicker()
    parent.page.overlay.append(parent.purchase_date)  # Requested
    parent.purchase_date_button = ElevatedButton(
        "Дата",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: parent.purchase_date.pick_date(),
    )


def add_purchase(parent):
    _service = get_service()
    if not (parent.product_name.value and (parent.selling_type.value or _service) and parent.unit_price.value
            and (parent.unit_quantity or _service)):
        parent.notify('У продукта не заполнены обязательные поля')
        return

    if not (set(str(parent.unit_price.value) + str(parent.unit_quantity.value)) < set('0987654321.,')):
        parent.notify('Цена и количество должны быть числами')

        return

    try:
        Purchase.insert(Purchase(
            name=parent.product_name.value,
            client_id=parent.clients_list.value,
            selling_type=parent.selling_type.value if not _service else SellingType.Услуга,
            unit_name=parent.unit_name.value if not _service else 'Услуга',
            unit_price=parent.unit_price.value,
            unit_quantity=parent.unit_quantity.value if not _service else 1,
            purchase_date=parent.purchase_date.value
        ))
    except Exception as err:
        parent.page.snack_bar = ft.SnackBar(ft.Text(str(err)))
        parent.page.snack_bar.open = True
        parent.page.update()
        return

    parent.close_dialog(None)
    parent.update_tab(None)
    parent.page.update()


def add_purchase_dialog(parent):
    _clients = Client.get_all()
    _service = not get_service()

    if not _clients:
        parent.notify('У вас не добавлено клиентов')
        return

    parent.clients_list = ft.Dropdown(
        label='Клиент' if not _service else 'Покупатель',
        options=[ft.dropdown.Option(text=str(i), key=i.id) for i in Client.get_all()],
    )

    parent.unit_quantity.visible = _service
    parent.unit_name.visible = _service
    parent.selling_type.visible = _service
    parent.unit_price.disabled = _service
    if not _service:
        parent.unit_price.label = 'Стоимость услуги'

    inputs = [
        parent.product_name,
        parent.selling_type,
        parent.unit_name,
        parent.unit_quantity,
        parent.unit_price,
        parent.clients_list,
        parent.purchase_date_button
    ]

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text('Покупка' if _service else 'Услуга'),
        content=Column(inputs, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        actions=[
            ElevatedButton(text='Добавить', on_click=lambda e: add_purchase(parent)),
            ElevatedButton(text='Отмена', on_click=parent.close_dialog)
        ],
    )


def get_tab(parent, theme=None) -> ft.ListView:
    purchases = Purchase.get_all()

    return ft.ListView(controls=[
                purchase_to_item(i, parent, theme=theme) for i in purchases
            ],
            spacing=10,
            expand=True,
        )

