import flet as ft
from clienttracker.db.crud import insert_clients, get_clients, delete_client, get_client_purchases
from clienttracker.db.models import Client
from clienttracker.giga import get_giga
from clienttracker.parsers.vk import extract_info, pretify_data
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
)


def init_values(parent):
    parent.client_name = TextField(label='Имя', autofocus=True)
    parent.client_surname = TextField(label='Фамилия')

    parent.client_pname = TextField(label='Отчество')
    parent.client_phone_number = TextField(label='Номер телефона', keyboard_type=ft.KeyboardType.PHONE)
    parent.client_birth_day = DatePicker()
    parent.page.overlay.append(parent.client_birth_day)  # Requested
    parent.client_birth_day_button = ElevatedButton(
        "Дата рождения",
        icon=icons.CALENDAR_MONTH,
        on_click=parent.client_birth_day.pick_date,
        width=float('inf')
    )
    parent.client_note = TextField(label='Заметка', multiline=True)
    parent.client_vk_link = TextField(label='VK id')
    parent.client_address = TextField(label='Адрес', keyboard_type=ft.KeyboardType.STREET_ADDRESS)


def add_client(parent):
    if not (parent.client_name.value and parent.client_surname.value):
        parent.notify('У клиента обязательно должны быть имя и фамилия')
        return

    insert_clients([Client(
        first_name=parent.client_name.value,
        last_name=parent.client_surname.value,
        patronymic_name=parent.client_pname.value,
        birthday=parent.client_birth_day.value,
        address=parent.client_address.value,
        note=parent.client_note.value,
        vk_link=parent.client_vk_link.value,
        phone_number=parent.client_phone_number.value,
    )])
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
            ElevatedButton(text='Добавить', on_click=lambda e: add_client(parent)),
            ElevatedButton(text='Отмена', on_click=parent.close_dialog)
        ],
    )


def show_clients_interests(client: Client, parent):
    vk_data = extract_info(client.vk_link)
    info = ''

    if vk_data[1] or len(vk_data[2]) < 5:  # Has posts
        info += ('У пользователя мало постов, поэтому мы не можем провести анализ')
        info += vk_data[0]
    else:
        info += get_giga(pretify_data(*vk_data))

    print(info) # TODO SHOW THIS THING


def del_client(client: Client, parent):
    delete_client(client)
#    parent.close_dialog(None)
    parent.update_tab(None)


def edit_client(client: Client, parent):
    parent.notify('В разработке')
    pass


def show_info_about(client: Client, parent):
    client_purchases = get_client_purchases(client)
    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text(str(client)),
        content=Column([
            Text(f'Заметка: {client.note}', visible=bool(client.note)),
            Text(f'Всего покупок: {len(client_purchases)}'),
            Text(f'Последняя покупка: {client_purchases[-1] if client_purchases else None}', visible=bool(client_purchases)),
            ElevatedButton(text='Анализ увлечений', icon=icons.LIGHTBULB, visible=bool(client.vk_link),
                           on_click=lambda e: show_clients_interests(client, parent)),
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        actions=[
            ElevatedButton(text='Закрыть', on_click=parent.close_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    parent.page.update()


def client_to_item(c: Client, parent) -> Container:
    return Container(content=Row(
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            Text(f'{c.last_name} {c.first_name}', expand=1, style=ft.TextStyle(size=16)),
            IconButton(icon=icons.MANAGE_SEARCH, on_click=lambda e: show_info_about(c, parent), tooltip='Аналиц соц. сетей', visible=bool(c.vk_link)),
            IconButton(icon=icons.EDIT, on_click=lambda e: edit_client(c, parent), tooltip='Изменить'),
            IconButton(icon=icons.DELETE, on_click=lambda e: del_client(c, parent), tooltip='Удалить'),
            IconButton(
                icon=ft.icons.MORE_VERT,
                on_click=lambda e: show_info_about(c, parent),
                tooltip='Ещё'
            ),
        ]
    ),
        bgcolor="blue",
        border_radius=14,
        padding=ft.padding.symmetric(0, 10),
        alignment=ft.alignment.center,
    )


def get_tab(parent) -> ft.ListView:
    clients = get_clients()

    return ft.ListView(controls=[
            client_to_item(i, parent) for i in clients
        ],
        spacing=10,
        expand=True,
    )
