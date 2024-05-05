from flet import Container, Row, Text, IconButton, icons, MainAxisAlignment, padding, alignment
from ...db.models import Client
from ..utils.object_methods import del_obj, edit_obj
from .vk_anal_dlg import analyze_vk
from .infos import client_info
from ..styles import item_font
from ..colors import bg_dict


class ClientItem(Container):
    def __init__(self, c: Client, parent, theme):
        super().__init__(content=Row(
            spacing=0,
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(f'{c.last_name} {c.first_name}', expand=1, style=item_font),
                IconButton(
                    icon=icons.MANAGE_SEARCH,
                    on_click=lambda e: analyze_vk(c, parent),
                    tooltip='Аналиц соц. сетей',
                    visible=bool(c.vk_link)
                ),
                IconButton(
                    icon=icons.EDIT,
                    on_click=lambda e: edit_obj(c, parent),
                    tooltip='Изменить'
                ),
                IconButton(
                    icon=icons.DELETE,
                    on_click=lambda e: del_obj(c, parent),
                    tooltip='Удалить'
                ),
                IconButton(
                    icon=icons.MORE_VERT,
                    on_click=client_info(c, parent),
                    tooltip='Ещё'
                ),
            ]
        ),
            bgcolor=bg_dict[parent.page.theme_mode],
            border_radius=14,
            padding=padding.symmetric(0, 10),
            alignment=alignment.center,
        )
