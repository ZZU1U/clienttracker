import flet as ft
from ...db.models import Note, Purchase, Client
from ..components.note_item import NoteItem
from flet import (
    Column,
    Container,
    Text,
    TextField,
    DatePicker,
    FilledTonalButton,
    AlertDialog,
    ElevatedButton,
    icons,
)


def init_values(parent):
    parent.note_title = TextField(label='Название', autofocus=True)
    parent.note_text = TextField(label='Текст', multiline=True)
    parent.note_schedule = DatePicker()
    parent.page.overlay.append(parent.note_schedule)
    parent.note_schedule_button = ElevatedButton(
        "Запланировать",
        icon=icons.CALENDAR_MONTH,
        on_click=lambda e: parent.note_schedule.pick_date,
#        width=float('inf')
    )


def add_note(parent):
    if not parent.note_title.value:
        parent.notify('У заметки должен быть заголовок!')
        return

    Note.insert(Note(
        title=parent.note_title.value,
        text=parent.note_text.value,
        date=parent.note_schedule.value,
        client_id=parent.clients_list.value,
        purchase_id=parent.purchases_list.value
    ))

    parent.close_dialog(None)
    parent.update_tab(None)
    parent.page.update()


def change_client(parent):
    purchases = Client.get_id(parent.clients_list.value).purchases
    parent.purchases_list.options = [
        ft.dropdown.Option(text=str(i), key=i.id) for i in purchases
    ]
    parent.purchases_list.visible = True
    parent.page.update()


def add_note_dialog(parent):
    parent.clients_list = ft.Dropdown(
        label='Покупатель',
        options=[ft.dropdown.Option(text=str(i), key=i.id) for i in Client.get_all()],
        on_change=lambda _: change_client(parent)
    )

    parent.clients_list.disabled = not parent.clients_list.options

    parent.purchases_list = ft.Dropdown(
        label='Покупка',
        options=[
            ft.dropdown.Option(text=str(i), key=i.id)
            for i in (
                Purchase.get_all() if not parent.clients_list.key
                else Client.get_id(parent.clients_list.key).purchases
            )],
        visible=False,
    )

    parent.purchases_list.disabled = not parent.purchases_list.options

    inputs = [
        parent.note_title,
        parent.note_text,
        parent.clients_list,
        parent.purchases_list,
        parent.note_schedule_button,
    ]

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text('Заметка'),
        content=Column(inputs, tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        actions=[
            ElevatedButton(text='Добавить', on_click=lambda e: add_note(parent)),
            ElevatedButton(text='Отмена', on_click=parent.close_dialog)
        ],
    )


def get_tab(parent, theme=None) -> ft.ListView:
    notes = Note.get_all()

    return ft.ListView(controls=[
            NoteItem(note, parent, theme) for note in notes
        ],
        expand=True,
        spacing=10,
    )
