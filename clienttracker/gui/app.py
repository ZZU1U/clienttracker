import flet as ft
import pages.clients
import pages.purchases
import pages.notes
import pages.settings
from clienttracker.db.crud import init_tables
from clienttracker.config import get_theme
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
        pages.clients.init_values(self)
        pages.purchases.init_values(self)
        pages.notes.init_values(self)
        pages.settings.init_values(self)

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.init_widgets()
        if self.page.snack_bar is not None:
            self.page.snack_bar.open = False
        self.page.update()

    def add_dialog(self, e):
        actions = [pages.clients.add_client_dialog, pages.purchases.add_purchase_dialog, pages.notes.add_note_dialog]
        actions[self.my_index](self)
        self.page.update()

    def update_tab(self, e):
        if e is not None and self.my_index == e.control.selected_index:
            return

        if e is not None:
            self.my_index = e.control.selected_index

        self.cont.content = self.tabs[self.my_index](self)
        self.page.update()

    def __init__(self, page: Page):
        # Main
        self.page = page
        self.page.theme_mode = get_theme()
        self.page.window_width = 400
        self.page.window_height = 700
        self.init_widgets()
        self.my_index = 0

        if not init_tables():
            self.page.snack_bar = ft.SnackBar(ft.Text('У вас не было баз данных, поэтому мы ее создали'))
            self.page.snack_bar.open = True

        # App bar
        self.page.appbar = AppBar(
            title=Text('Client Tracker', size=32),
            center_title=False,
            toolbar_height=75,
            actions=[ft.IconButton(icon=icons.SETTINGS, tooltip='Настройки', on_click=lambda e: pages.settings.launch(self))],

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
                    label='Покупки'
                ),
                ft.NavigationDestination(
                    icon=icons.BOOKMARK_BORDER,
                    selected_icon=icons.BOOKMARK,
                    label='Заметки',
                ),
            ]
        )

        # Tabs
        self.tabs = [pages.clients.get_tab, pages.purchases.get_tab, pages.notes.get_tab]

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
#        view=ft.AppView.WEB_BROWSER
    )
