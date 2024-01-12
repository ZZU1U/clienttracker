import flet as ft
from clienttracker.db.queries.orm import insert_notes, get_notes, get_clients, get_client_by_id, get_purchases, get_client_id_purchases
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
    parent.note_title = TextField(label='Название', autofocus=True)
    parent.note_text = TextField(label='Текст', multiline=True)
    parent.note_dl = DatePicker()
    parent.page.overlay.append(parent.note_dl)  # Requested
    parent.note_dlbutton = ElevatedButton(
        "Дедлайн",
        icon=icons.CALENDAR_MONTH,
        on_click=lambda _: parent.note_dl.pick_date(),
    )
    parent.note_sched = DatePicker()
    parent.note_schedbutton = ElevatedButton(
        "Запланировано",
        icon=icons.CALENDAR_MONTH,
        on_click=lambda _: parent.note_dl.pick_date(),
    )


def add_note(parent):
    pass


def change_client(parent):
    client = get_client_by_id(parent.purchases_list.key.client_id)
    parent.clients_list.value = f'{client.last_name} {client.first_name}'
    parent.clients_list.key = client


def add_note_dialog(parent):
    parent.clients_list = ft.Dropdown(
        label='Покупатель',
        options=[ft.dropdown.Option(text=f'{i.last_name} {i.first_name}', key=i.id) for i in get_clients()]
    )

    parent.clients_list.disabled = not parent.clients_list.options

    parent.purchases_list = ft.Dropdown(
        label='Покупка',
        options=[ft.dropdown.Option(text=f'{i.name} {i.purchase_date}', key=i.id) for i in (get_purchases() if not parent.clients_list.value else get_client_id_purchases(parent.clients_list.key.id))],
        on_change=lambda _: change_client(parent),
    )

    parent.purchases_list.disabled = not parent.purchases_list.options

    inputs = [
        parent.note_title,
        parent.note_text,
        parent.clients_list,
        parent.purchases_list,
        parent.note_dlbutton,
        parent.note_schedbutton,
    ]

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text('Заметка'),
        content=Column(inputs, tight=True),
        actions=[
            ElevatedButton(text='Добавить', on_click=lambda e: add_note(parent)),
            ElevatedButton(text='Отмена', on_click=parent.close_dialog)
        ],
    )


def get_tab(page: Page) -> Column:
    notes = get_notes()

    return Column(controls=[
            Container(content=FilledTonalButton(text=f'{i.title} {i.text[:10]}'), width=float('inf')) for i in notes
        ],
        expand=True,
    )
