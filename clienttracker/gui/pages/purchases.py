import flet as ft
from clienttracker.db.queries.orm import get_purchases, insert_purchases, get_clients
from clienttracker.db.models import Purchases, SellingType
from flet import (
    Page,
    Column,
    AppBar,
    Container,
    Text,
    TextField,
    DatePicker,
    FloatingActionButton,
    FilledTonalButton,
    AlertDialog,
    ElevatedButton,
    icons,
)


def update_fields(parent):
    unit_name = parent.unit_name.value
    parent.unit_price.disabled = False
    parent.unit_quantity.disabled = False
    parent.unit_quantity.suffix = Text(unit_name)
    parent.unit_price.label = f'Стоимость {"штуки" if parent.selling_type.value == "Штучно" else unit_name}'
    parent.unit_quantity.label = "Количество " + ("штук" if parent.selling_type.value == "Штучно" else unit_name)
    parent.unit_quantity.value = 1
    parent.unit_name.disabled = parent.selling_type.value == 'Штучно'

    parent.page.update()


def init_values(parent):
    parent.product_name = TextField(label='Продукт', autofocus=True, enable_suggestions=True)
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
    parent.unit_name = TextField(label='Название единицы', hint_text='кг', disabled=True, on_change=lambda e: update_fields(parent))


def add_purchase(parent):
    if not (parent.product_name.value and parent.selling_type.value and parent.unit_price.value
            and parent.unit_quantity):
        parent.page.snack_bar = ft.SnackBar(ft.Text('У продукта не заполнены обязательные поля'))
        parent.page.snack_bar.open = True
        parent.page.update()
        return

    if not (set(parent.unit_price.value + parent.unit_quantity.value) < set('0987654321.,')):
        parent.page.snack_bar = ft.SnackBar(ft.Text('Цена и количество должны быть числами'))
        parent.page.snack_bar.open = True
        parent.page.update()
        return

    try:
        insert_purchases([Purchases(
            name=parent.product_name.value,
            client_id=parent.clients_list.value,
            selling_type=parent.selling_type.value,
            unit_name=parent.unit_name.value,
            unit_price=parent.unit_price.value,
            unit_quantity=parent.unit_quantity.value
        )])


    except Exception as err:
        parent.page.snack_bar = ft.SnackBar(ft.Text(str(err)))
        parent.page.snack_bar.open = True
        parent.page.update()
        return

    parent.close_dialog(None)
    parent.update_tab(None)
    parent.page.update()


def add_purchase_dialog(parent):
    _clients = get_clients()

    if not _clients:
        parent.page.snack_bar = ft.SnackBar(ft.Text('У вас не добавлено клиентов'))
        parent.page.snack_bar.open = True
        parent.page.update()
        return


    parent.clients_list = ft.Dropdown(
        label='Покупатель',
        options=[ft.dropdown.Option(text=f'{i.last_name} {i.first_name}', key=i.id) for i in get_clients()],
    )

    inputs = [
        parent.product_name,
        parent.selling_type,
        parent.unit_name,
        parent.unit_quantity,
        parent.unit_price,
        parent.clients_list,
    ]

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text('Покупка'),
        content=Column(inputs, tight=True),
        actions=[
            ElevatedButton(text='Добавить', on_click=lambda e: add_purchase(parent)),
            ElevatedButton(text='Отмена', on_click=parent.close_dialog)
        ],
    )


def get_tab(page: Page) -> Column:
    purchases = get_purchases()

    return Column(controls=[
            Container(content=FilledTonalButton(text=f'{i.client_id} {i.name}'), width=float('inf')) for i in purchases
        ],
        expand=True,
    )
