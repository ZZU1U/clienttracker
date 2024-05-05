import flet as ft
from ...db.models import Client
from ..components.client_item import ClientItem
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
    ProgressBar,
)


def init_values(parent):
    parent.client_name = TextField(label='Имя')
    parent.client_surname = TextField(label='Фамилия', autofocus=True)

    parent.client_pname = TextField(label='Отчество')
    parent.client_phone_number = TextField(label='Номер телефона', keyboard_type=ft.KeyboardType.PHONE)
    parent.client_birth_day = DatePicker()
    parent.page.overlay.append(parent.client_birth_day)  # Requested
    parent.client_birth_day_button = ElevatedButton(
        "Дата рождения",
        icon=icons.CALENDAR_MONTH,
        on_click=lambda e: parent.client_birth_day.pick_date(),
        width=float('inf')
    )
    parent.client_note = TextField(label='Описание', multiline=True)
    parent.client_vk_link = TextField(label='VK id')
    parent.client_address = TextField(label='Адрес', keyboard_type=ft.KeyboardType.STREET_ADDRESS)

    parent.anal_request = TextField(label='Запрос', hint_text='Чем увлекается клиент?')
    parent.anal_response = Text('Здесь будет ответ от гигачата')
    parent.anal_ring = ProgressBar(width=16, height=16)


def add_client(parent):
    if not (parent.client_name.value and parent.client_surname.value):
        parent.notify('У клиента обязательно должны быть имя и фамилия')
        return

    Client.insert(Client(
        first_name=parent.client_name.value,
        last_name=parent.client_surname.value,
        patronymic_name=parent.client_pname.value,
        birthday=parent.client_birth_day.value,
        address=parent.client_address.value,
        description=parent.client_note.value,
        vk_link=parent.client_vk_link.value,
        phone_number=parent.client_phone_number.value,
    ))

    parent.close_dialog(None)
    parent.update_tab(None)
    parent.page.update()


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
                    parent.client_birth_day_button,
                ],
                    padding=ft.Padding(top=10, bottom=10, left=0, right=0),
                    spacing=12,
                    height=240
                )], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ],
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        controls_padding=ft.padding.symmetric(vertical=10),
        tile_padding=ft.Padding(top=3, bottom=0, left=0, right=0),
    )

    inputs = [
        parent.client_surname,
        parent.client_name,
        additional_inputs
    ]

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text('Клиент'),
        content=Column(inputs, tight=True),
        actions=[
            ElevatedButton(text='Добавить', on_click=lambda e: add_client(parent)),
            ElevatedButton(text='Отмена', on_click=parent.close_dialog)
        ],
    )


def get_tab(parent, theme=None) -> ft.ListView:
    clients = Client.get_all()

    return ft.ListView(controls=[
            ClientItem(i, parent, theme=theme) for i in clients
        ],
        spacing=10,
        expand=True,
    )
