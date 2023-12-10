import flet as ft
from clienttracker.db.queries.orm import get_purchases, insert_purchases, get_clients
from clienttracker.db.models import Purchases, SellingType
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


def launch(parent):
    # Not in progress now
    parent.page.snack_bar = ft.SnackBar(Text('Настроек пока что нет :)'))
    parent.page.snack_bar.open = True
    parent.page.update()
    pass
