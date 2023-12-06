import flet as ft
from clienttracker.db.queries.orm import insert_clients, get_clients
from clienttracker.db.models import Clients
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


def add_client(parent, e):
    if parent.client_name.value and parent.client_surname.value:
        parent.close_dialog(None)

        parent.page.update()
    else:
        parent.page.snack_bar = ft.SnackBar(ft.Text('У клиента обязательно должны быть имя и фамилия'))
        parent.page.snack_bar.open = True
        parent.page.update()
        return

    insert_clients([Clients(
        first_name=parent.client_name.value,
        last_name=parent.client_surname.value,
        patronymic_name=parent.client_pname.value,
        birthday=parent.client_bday.value,
        address=parent.client_address.value,
        note=parent.client_note.value,
        vk_link=parent.client_vk_link.value,
        phone_number=parent.client_phone_number.value,
    )])

    parent.update_tab(None)


def add_client_dialog(parent):
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
            ElevatedButton(text='Добавить', on_click=add_client),
            ElevatedButton(text='Отмена', on_click=parent.close_dialog)
        ],
    )


def get_tab(page: Page):
    clients = get_clients()

    return Column(controls=[
            Container(content=FilledTonalButton(text=str(i)), width=float('inf')) for i in clients
        ],
        expand=True,
    )
