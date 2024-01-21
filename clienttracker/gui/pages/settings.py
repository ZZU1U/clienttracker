import flet as ft
from clienttracker.config import get_service, set_service, get_theme, set_theme
from flet import (
    Page,
    Switch,
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


def update_service(parent):
    parent.is_service.label = "Услуги" if parent.is_service.value else "Товары"
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


def apply(parent):
    if get_service() == parent.is_service.value and (get_theme() == 'light') == parent.theme_switcher.value:
        return

    set_service(parent.is_service.value)
    set_theme('light' if parent.theme_switcher.value else 'dark')

    parent.page.theme_mode = get_theme()

    parent.close_dialog(None)

    parent.page.snack_bar = ft.SnackBar(Text('Настройки применены'))
    parent.page.snack_bar.open = True
    parent.page.update()


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
            ElevatedButton(text='Отмена', on_click=parent.close_dialog)
        ],
    )

    parent.page.update()
