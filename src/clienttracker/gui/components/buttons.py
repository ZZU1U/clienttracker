from ...db.models import Note, Client, Purchase

from flet import FilledButton, icons, ButtonStyle, padding


style = ButtonStyle(
    padding=padding.all(15),
)


class NoteButton(FilledButton):
    def __init__(self, note: Note, parent, on_click=None, **kwargs):
        super().__init__(
            text=str(note),
            icon=icons.NOTE,
            width=float('inf'),
            on_click=on_click,
            style=style,
            **kwargs
        )


class ClientButton(FilledButton):
    def __init__(self, client: Client, parent, on_click=None, **kwargs):
        super().__init__(
            text=str(client),
            icon=icons.PERSON,
            width=float('inf'),
            on_click=on_click,
            style=style,
            **kwargs
        )


class PurchaseButton(FilledButton):
    def __init__(self, purchase: Purchase, parent, on_click=None, **kwargs):
        super().__init__(
            text=str(purchase),
            icon=icons.PAYMENTS,
            width=float('inf'),
            on_click=on_click,
            style=style,
            **kwargs
        )
