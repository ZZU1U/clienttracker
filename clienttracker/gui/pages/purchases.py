import flet as ft
from clienttracker.db.queries.orm import get_purchases, insert_purchases
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


def init_values(parent):
    parent.client_name = TextField(label='Имя', autofocus=True)
    parent.client_surname = TextField(label='Фамилия', autofocus=True)

    parent.client_pname = TextField(label='Отчество', autofocus=True)
    parent.client_phone_number = TextField(label='Номер телефона', keyboard_type=ft.KeyboardType.NUMBER)
    parent.client_bday = DatePicker()
    parent.page.overlay.append(parent.client_bday)  # Requested
    parent.client_bdaybutton = ElevatedButton(
        "Дата рождения",
        icon=icons.CALENDAR_MONTH,
        on_click=lambda _: parent.client_bday.pick_date(),
    )
    parent.client_note = TextField(label='Заметка', autofocus=True)
    parent.client_vk_link = TextField(label='VK id', autofocus=True)
    parent.client_address = TextField(label='Адрес', autofocus=True)


def add_purchase(parent, e):
    pass


def add_purchase_dialog(parent):
    additional_inputs = ft.ExpansionTile(
        title=Text('Другое'),
        controls=[
            Column(controls=[
                ft.ListView(controls=[
                    parent.client_pname,
                    parent.client_phone_number,
                    parent.client_note,
                    parent.client_vk_link,
                    parent.client_address,
                    parent.client_bdaybutton,
                ],
                    padding=ft.Padding(top=10, bottom=0, left=0, right=0),
                    spacing=12,
                    height=240,
                )])
        ],
        collapsed_shape=ft.CircleBorder(),
        shape=ft.CircleBorder(),
        controls_padding=ft.padding.symmetric(vertical=10),
        tile_padding=ft.Padding(top=3, bottom=0, left=0, right=0),
    )

    inputs = [
        parent.client_name,
        parent.client_surname,
        additional_inputs
    ]

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text('Клиент'),
        content=Column(inputs, tight=True),
        actions=[
            ElevatedButton(text='Добавить', on_click=add_purchase),
            ElevatedButton(text='Отмена', on_click=parent.close_dialog)
        ],
    )


def get_tab(page: Page) -> Column:
    purchases = get_purchases()

    return Column(controls=[
            Container(content=FilledTonalButton(text=str(i)), width=float('inf')) for i in purchases
        ],
        expand=True,
    )
