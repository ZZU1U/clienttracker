from flet import Container, Row, Text, MainAxisAlignment, IconButton, icons, padding, alignment

from ..colors import bg_dict
from ...db.models import Note
from ..styles import item_font
from ..utils.object_methods import edit_obj, del_obj
from .infos import note_info


class NoteItem(Container):
    def __init__(self, note: Note, parent, theme):
        super().__init__(
            content=Row(
                spacing=0,
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Text(str(note), expand=1, style=item_font),
                    IconButton(
                        icon=icons.EDIT,
                        on_click=lambda e: edit_obj(note, parent),
                        tooltip='Изменить'
                    ),
                    IconButton(
                        icon=icons.DELETE,
                        on_click=lambda e: del_obj(note, parent),
                        tooltip='Удалить'
                    ),
                    IconButton(
                        icon=icons.MORE_VERT,
                        on_click=note_info(note, parent),
                        tooltip='Ещё'
                    ),
                ]
            ),
            bgcolor=bg_dict[parent.page.theme_mode],
            border_radius=14,
            padding=padding.symmetric(0, 10),
            alignment=alignment.center,
        )
