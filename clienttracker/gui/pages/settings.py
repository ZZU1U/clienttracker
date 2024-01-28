import flet as ft
from clienttracker.config import get_service, set_service, get_theme, set_theme
from flet import (
    Switch,
    Column,
    Text,
    AlertDialog,
    ElevatedButton,
)


def update_service(parent):
    parent.is_service.label = "Услуги" if parent.is_service.value else "Товары"
    parent.page.navigation_bar.destinations[1].label = 'Покупки' if not parent.is_service.value else 'Услуги'
    parent.page.update()


def update_theme(parent):
    parent.theme_switcher.label = ("Светлая" if parent.theme_switcher.value else "Темная") + " тема"
    parent.page.theme_mode = 'dark' if not parent.theme_switcher.value else 'light'
    parent.page.update()


def init_values(parent):
    parent.is_service = Switch(label="Услуги" if get_service() else "Товары", value=get_service(),
                               on_change=(lambda e: update_service(parent)))
    parent.theme_switcher = Switch(label=("Светлая" if parent.page.theme_mode == 'light' else "Темная") + " тема",
                                   value=parent.page.theme_mode == 'light', on_change=(lambda e: update_theme(parent)))


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
        parent.theme_switcher
    ]

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text('Настройки'),
        content=Column(inputs, tight=True),
        actions=[
            ElevatedButton(text='Сохранить', on_click=lambda e: apply(parent)),
            ElevatedButton(text='Отмена', on_click=lambda e: cancel(parent))
        ],
    )

    parent.page.update()
