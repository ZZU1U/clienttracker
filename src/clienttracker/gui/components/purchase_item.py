from flet import Container, Row, Text, IconButton, icons, MainAxisAlignment, colors, padding, alignment
from ..utils.object_methods import del_obj, edit_obj
from ...db.models import Purchase
from ..colors import bg_dict
from .infos import purchase_info


def purchase_to_item(p: Purchase, parent, theme=None) -> Container:
    return Container(content=Row(
        spacing=0,
        alignment=MainAxisAlignment.CENTER,
        controls=[
            Text(f'{p.name}({int(p.unit_quantity)} {p.unit_name})', expand=True),
            IconButton(icon=icons.EDIT, on_click=lambda e: edit_obj(p, parent), tooltip='Изменить'),
            IconButton(icon=icons.DELETE, on_click=lambda e: del_obj(p, parent), tooltip='Удалить'),
            IconButton(
                icon=icons.MORE_VERT,
                on_click=purchase_info(p, parent),
                tooltip='Ещё'
            ),
        ]
    ),
        bgcolor=bg_dict[parent.page.theme_mode],
        border_radius=14,
        padding=padding.symmetric(0, 10),
        alignment=alignment.center,
    )
