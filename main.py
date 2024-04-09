import flet as ft
import clienttracker.gui.pages.clients as pages_clients
import clienttracker.gui.pages.purchases as pages_purchases
import clienttracker.gui.pages.notes as pages_notes
import clienttracker.gui.pages.settings as pages_settings
from clienttracker.db.database import init_tables
from clienttracker.config import get_theme, get_service
from flet import (
    Page,
    AppBar,
    Container,
    Text,
    FloatingActionButton,
    icons,
)


class ClientTracker:
    def init_widgets(self):
        pages_clients.init_values(self)
        pages_purchases.init_values(self)
        pages_notes.init_values(self)
        pages_settings.init_values(self)

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.init_widgets()
        if self.page.snack_bar is not None:
            self.page.snack_bar.open = False
        self.page.update()

    def add_dialog(self, e):
        actions = [pages_clients.add_client_dialog, pages_purchases.add_purchase_dialog, pages_notes.add_note_dialog]
        actions[self.my_index](self)
        self.page.update()

    def notify(self, text: str):
        self.page.snack_bar = ft.SnackBar(ft.Text(text))
        self.page.snack_bar.open = True
        self.page.update()

    def update_tab(self, e):
        if (e is not None) and self.my_index == e.control.selected_index:
            return

        if e is not None:
            self.my_index = e.control.selected_index

        self.cont.content = self.tabs[self.my_index](self)
        self.page.update()

    def __init__(self, page: Page):
        # Main
        self.page = page
        self.page.title = 'ClientTracker'
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.theme_mode = get_theme()
        self.page.window_width = 270
        self.page.window_height = 540
        self.init_widgets()
        self.my_index = 0

        if not init_tables():
            self.notify('Создана база данных')

        # App bar
        self.page.appbar = AppBar(
            title=Text('Client Tracker', size=32),
            center_title=False,
            toolbar_height=75,
            actions=[ft.IconButton(icon=icons.SETTINGS, tooltip='Настройки',
                                   on_click=lambda e: pages_settings.launch(self))],

        )

        # Navigation bar
        self.page.navigation_bar = ft.NavigationBar(
            selected_index=0,
            on_change=self.update_tab,
            destinations=[
                ft.NavigationDestination(
                    icon=icons.CONTACT_PAGE_OUTLINED,
                    selected_icon=icons.CONTACT_PAGE,
                    label='Клиенты'
                ),
                ft.NavigationDestination(
                    icon=icons.SHOPPING_BAG_OUTLINED,
                    selected_icon=icons.SHOPPING_BAG,
                    label='Покупки' if not get_service() else 'Услуги'
                ),
                ft.NavigationDestination(
                    icon=icons.BOOKMARK_BORDER,
                    selected_icon=icons.BOOKMARK,
                    label='Заметки',
                ),
            ]
        )

        # Tabs
        self.tabs = [pages_clients.get_tab, pages_purchases.get_tab, pages_notes.get_tab]

        # Page content
        self.cont = Container(
            content=self.tabs[0](self)
        )
        self.page.add(self.cont)

        # Floating button
        self.page.add(FloatingActionButton(icon=icons.ADD, on_click=self.add_dialog))

        # Load it all!
        self.page.update()


if __name__ == '__main__':
    ft.app(
        target=ClientTracker,
        # view=ft.AppView.WEB_BROWSER
    )
