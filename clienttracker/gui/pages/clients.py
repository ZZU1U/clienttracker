import flet as ft
from clienttracker.db.models import Client
from clienttracker.giga import get_giga_for_data
from clienttracker.parsers.vk import extract_info
from clienttracker.gui.utils import *
from clienttracker.config import *
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


def resize_user_icon(parent, e):
    if e.data == 'true':
        parent.user_avatar.max_radius -= 30
    else:
        parent.user_avatar.max_radius += 30
    parent.page.update()
    parent.page.update()


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


def show_info_about(client: Client, parent):
    client_purchases = client.purchases
    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text(str(client)),
        content=Column([
            Text(f'Описание: {client.description}', visible=bool(client.description)),
            Text(f'Всего покупок: {len(client_purchases)}'),
            Text(
                f'Последняя покупка: {client_purchases[-1] if client_purchases else None}',
                visible=bool(client_purchases)
            ),
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        actions=[
            ElevatedButton(text='Закрыть', on_click=parent.close_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    parent.page.update()


def do_anal(client: Client, data: str, parent):
    req = parent.anal_request.value
    ans = get_giga_for_data(data, req)
    #parent.anal_response.


def analyze_vk(client: Client, parent):
    vk_data = extract_info(client.vk_link)

    parent.analyzed_info = Text(disabled=True)

    info = []
    if vk_data.get('photo', ''):
        parent.user_avatar = ft.CircleAvatar(foreground_image_url=vk_data['photo'], max_radius=100)
        info.append(parent.user_avatar)

    info.extend([  # Add closable menus
            Text(
                vk_data['error'],
                visible=bool(vk_data['error']),
                color=colors.WHITE,
                bgcolor=colors.RED_ACCENT,
                size=18
            ),

            ft.ExpansionTile(
                title=Text('О странице'),
                controls=[Text(vk_data.get("data", ''))],
                visible=bool(vk_data.get('data', False)),
                on_change=lambda e: resize_user_icon(parent, e),
            ),
#            Slider(min=0, max=10, divisions=10, value=10),  // For choosing dates range
    ])

    if not vk_data['error'] and get_subscription():
        info.append(ft.ExpansionTile(title=Text('Анализ'), controls=[
            parent.anal_request, 
            IconButton(icon=ft.icons.SEND, on_click=lambda e: do_anal(client, vk_data, parent)), 
            parent.anal_response], on_change=lambda e: resize_user_icon(parent, e)))

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text(str(client)),
        content=Column(info, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        actions=[
            ElevatedButton(text='Закрыть', on_click=parent.close_dialog)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    parent.page.update()


def client_to_item(c: Client, parent, theme=None) -> Container:
    return Container(content=Row(
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            Text(f'{c.last_name} {c.first_name}', expand=1, style=ft.TextStyle(size=16)),
            IconButton(
                icon=icons.MANAGE_SEARCH,
                on_click=lambda e: analyze_vk(c, parent),
                tooltip='Аналиц соц. сетей',
                visible=bool(c.vk_link)
            ),
            IconButton(
                icon=icons.EDIT,
                on_click=lambda e: edit_obj(c, parent),
                tooltip='Изменить'
            ),
            IconButton(
                icon=icons.DELETE,
                on_click=lambda e: del_obj(c, parent),
                tooltip='Удалить'
            ),
            IconButton(
                icon=ft.icons.MORE_VERT,
                on_click=lambda e: show_info_about(c, parent),
                tooltip='Ещё'
            ),
        ]
    ),
        bgcolor=(colors.BLUE_ACCENT if parent.page.theme_mode == 'dark' else colors.LIGHT_BLUE_ACCENT_200),
        border_radius=14,
        padding=ft.padding.symmetric(0, 10),
        alignment=ft.alignment.center,
    )


def get_tab(parent, theme=None) -> ft.ListView:
    clients = Client.get_all()

    return ft.ListView(controls=[
            client_to_item(i, parent, theme=theme) for i in clients
        ],
        spacing=10,
        expand=True,
    )
