from flet import AlertDialog, Column, Text, ElevatedButton, MainAxisAlignment, CrossAxisAlignment, ExpansionTile
from typing import Callable

from ...config import get_service
from ...db.models import Note, Client, Purchase
from ..utils.decorators import loading
from .buttons import PurchaseButton, NoteButton, ClientButton


@loading
def note_info(note: Note, parent) -> Callable:
    def show_info(*args):
        note_client = note.client
        note_purchase = note.purchase
        parent.page.dialog = AlertDialog(
            open=True,
            modal=True,
            title=Text(str(note)),
            content=Column([
                Text(f'Дата: {note.date}', visible=bool(note.date)),
                Text(note.text, visible=bool(note.text)),
                ClientButton(
                    note_client,
                    parent,
                    on_click=client_info(note_client, parent),
                ),
                PurchaseButton(
                    note_purchase,
                    parent,
                    on_click=purchase_info(note_purchase, parent),
                    visible=bool(note_purchase),
                ),
            ], tight=True, horizontal_alignment=CrossAxisAlignment.CENTER),
            actions=[
                ElevatedButton(text='Закрыть', on_click=parent.close_dialog)
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )
        parent.page.update()

    return show_info


@loading
def client_info(client: Client, parent) -> Callable:
    def show_info(*args):
        client_purchases = client.purchases
        client_notes = client.notes
        parent.page.dialog = AlertDialog(
            open=True,
            modal=True,
            title=Text(str(client)),
            content=Column([
                Text(f'Описание: {client.description}', visible=bool(client.description)),
                Text(f'День рождения: {client.birthday.strftime("%d/%m/%Y") if client.birthday else ""}', visible=bool(client.birthday)),
                Text(f'Адрес: {client.address}', visible=bool(client.address)),
                Text(f'Телефон: {client.phone_number}', visible=bool(client.phone_number)),
                ExpansionTile(
                    title=Text(f'{"Покупки" if not get_service() else "Услуги"} ({len(client_purchases)})'),
                    controls=[
                        PurchaseButton(
                            purchase,
                            parent,
                            on_click=purchase_info(purchase, parent)
                        ) for purchase in client_purchases
                    ],
                    visible=len(client_purchases) > 0
                ),
                ExpansionTile(
                    title=Text(f'Заметки ({len(client_notes)})'),
                    controls=[
                        NoteButton(
                            note,
                            parent,
                            on_click=note_info(note, parent)
                        ) for note in client_notes
                    ],
                    visible=len(client_notes) > 0
                )
            ], tight=True, horizontal_alignment=CrossAxisAlignment.CENTER),
            actions=[
                ElevatedButton(text='Закрыть', on_click=parent.close_dialog)
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )
        parent.page.update()
    return show_info


@loading
def purchase_info(purchase: Purchase, parent) -> Callable:
    def show_info(*args):
        purchase_client = purchase.client
        purchase_notes = purchase.notes
        parent.page.dialog = AlertDialog(
            open=True,
            modal=True,
            title=Text(str(purchase)),
            content=Column([
                Text(f'Продукт: {purchase.name}'),
                Text(f'Дата: {purchase.purchase_date}'),
                Text(f'Цена {purchase.unit_name}: {purchase.unit_price}'),
                Text(f'Количество: {purchase.unit_quantity} {purchase.unit_name}'),
                Text(f'Цена покупки: {purchase.unit_quantity * purchase.unit_price}'),
                ClientButton(purchase_client, parent, client_info(purchase_client, parent)),
                ExpansionTile(
                    title=Text(f'Заметки ({len(purchase_notes)})'),
                    controls=[
                        NoteButton(
                            note,
                            parent,
                            on_click=note_info(note, parent)
                        ) for note in purchase_notes
                    ],
                    visible=len(purchase_notes) > 0
                )
            ], tight=True, horizontal_alignment=CrossAxisAlignment.CENTER),
            actions=[
                ElevatedButton(text='Закрыть', on_click=parent.close_dialog)
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )
        parent.page.update()

    return show_info

