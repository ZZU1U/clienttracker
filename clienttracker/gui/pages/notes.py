import flet as ft
from clienttracker.db.queries.orm import get_notes
from flet import (
    Column,
    Text,
    FilledTonalButton,
    Page,
    Container
)


def init_values(parent):
    pass


def add_note(parent, e):
    pass


def add_note_dialog(parent):
    pass


def get_tab(page: Page) -> Column:
    notes = get_notes()

    return Column(controls=[
            Container(content=FilledTonalButton(text=str(i)), width=float('inf')) for i in notes
        ],
        expand=True,
    )
