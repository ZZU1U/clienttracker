import flet as ft
from clienttracker.config import *
from clienttracker.db.database import create_tables
from clienttracker.db.models import Client, Note
from clienttracker.parsers.vcard import parse_vcard, vcard_to_clients
from clienttracker.gui.utils import edit_obj
from flet import (
    Switch,
    Column,
    Text,
    AlertDialog,
    ElevatedButton,
)


def update_service(parent):
    parent.page.navigation_bar.destinations[1].label = 'Покупки' if parent.is_service.value == 'no' else 'Услуги'
    parent.page.update()


def update_theme(parent):
    parent.theme_switcher.label = ("Светлая" if parent.theme_switcher.value else "Темная") + " тема"
    parent.page.theme_mode = 'dark' if not parent.theme_switcher.value else 'light'
    parent.update_tab(None)
    parent.page.update()


def import_vcard(e: ft.FilePickerResultEvent):
    if not e.files:
        return
    parsed = list(map(lambda v: vcard_to_clients(v), parse_vcard(e.files[0].path)))
    clients, notes = list(zip(*parsed))

    Client.insert_all(clients)
    Note.insert_all(notes)


def init_values(parent):
    parent.is_service = ft.RadioGroup(
        ft.Row([
            ft.Radio(value='yes', label='Услуги'),
            ft.Radio(value='no', label='Товары'),
        ]),
        value='yes' if get_service() else 'no',
        on_change=lambda _: update_service(parent)
    )

    parent.theme_switcher = Switch(
        label=("Светлая" if parent.page.theme_mode == 'light' else "Темная") + " тема",
        value=parent.page.theme_mode == 'light',
        on_change=(lambda e: update_theme(parent))
    )
    parent.pick_vcard_dialog = ft.FilePicker(on_result=import_vcard)
    parent.page.overlay.append(parent.pick_vcard_dialog)  # Requested

    parent.pick_vcard = ElevatedButton(
        text='Импорт книги контактов',
        on_click=lambda _: (
            parent.pick_vcard_dialog.pick_files(
                dialog_title='Выберите файл книги контактов (VCF)',
                allow_multiple=False,
                allowed_extensions=['vcf'],
            ),
            parent.update_tab(None)
        ),
        width=float('inf')
    )

    parent.clear_db = ElevatedButton(
        text='Очистить все данные',
        on_click=lambda _: (create_tables(), parent.update_tab(None)),
        width=float('inf')
    )

    parent.vk_login = ElevatedButton(
        text='Вход в ВКонтакте',
        on_click=lambda e: edit_obj(None, None),  # Probably should remove this
        width=float('inf')
    )

    parent.subscription = Switch(
        label='Подписка',
        value=get_subscription(),
        on_change=(lambda e: set_subscription(e.control.value))
    )


def cancel(parent):
    parent.page.navigation_bar.destinations[1].label = 'Покупки' if not get_service() else 'Услуги'
    parent.page.theme_mode = get_theme()
    parent.close_dialog(None)
    parent.page.update()


def apply(parent):
    if get_service() == parent.is_service.value and (get_theme() == 'light') == parent.theme_switcher.value:
        return

    set_service(parent.is_service.value)
    set_theme('light' if parent.theme_switcher.value else 'dark')

    cancel(parent)

    parent.notify('Настройки применены')


def launch(parent):
    inputs = [
        parent.is_service,
        parent.theme_switcher,
        parent.subscription,
        parent.pick_vcard,
        parent.vk_login,
        parent.clear_db,
    ]

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text('Настройки'),
        content=Column(inputs, tight=True, alignment=ft.MainAxisAlignment.CENTER),
        actions=[
            ElevatedButton(text='Сохранить', on_click=lambda e: apply(parent)),
            ElevatedButton(text='Отмена', on_click=lambda e: cancel(parent))
        ],
    )

    parent.page.update()
