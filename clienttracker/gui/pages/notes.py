import flet as ft
from clienttracker.db.crud import (get_notes, get_clients, get_client_by_id, get_purchases,
                     get_client_id_purchases, get_purchase_by_id, insert_notes)
from clienttracker.db.models import Note
from flet import (
    Page,
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
        on_click=lambda _: parent.note_schedule.pick_date(),
#        width=float('inf')
    )


def add_note(parent):
    if not parent.note_title.value:
        parent.page.snack_bar = ft.SnackBar(ft.Text('У заметки должен быть заголовок!'))
        parent.page.snack_bar.open = True
        parent.page.update()
        return

    insert_notes([Note(
        title=parent.note_title.value,
        text=parent.note_text.value,
        date=parent.note_schedule.value,
        client_id=parent.clients_list.value,
        purchase_id=parent.purchases_list.value
    )])

    parent.close_dialog(None)
    parent.update_tab(None)
    parent.page.update()


def change_client(parent):
    purchases = get_client_id_purchases(parent.clients_list.value)
    parent.purchases_list.options = [ft.dropdown.Option(text=f'{i.name} {i.purchase_date}', key=i.id) for i in purchases]
    parent.page.update()


def change_purchase(parent):
    client = get_client_by_id(get_purchase_by_id(parent.purchases_list.value).client_id)
    parent.clients_list.value = str(client)
    parent.page.update()


def add_note_dialog(parent):
    parent.clients_list = ft.Dropdown(
        label='Покупатель',
        options=[ft.dropdown.Option(text=str(i), key=i.id) for i in get_clients()],
        on_change=lambda _: change_client(parent)
    )

    parent.clients_list.disabled = not parent.clients_list.options

    parent.purchases_list = ft.Dropdown(
        label='Покупка',
        options=[ft.dropdown.Option(text=f'{i.name} {i.purchase_date}', key=i.id) for i in (get_purchases() if not parent.clients_list.key else get_client_id_purchases(get_purchase_by_id(int(parent.clients_list.key))))],
        on_change=lambda _: change_purchase(parent),
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


def get_tab(parent) -> Column:
    notes = get_notes()

    return Column(controls=[
            Container(content=FilledTonalButton(text=str(i)), width=float('inf')) for i in notes
        ],
        expand=True,
    )
