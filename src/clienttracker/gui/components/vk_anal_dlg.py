from flet import Text, CircleAvatar, colors, icons, ExpansionTile, AlertDialog, IconButton, Column, ElevatedButton, \
    CrossAxisAlignment, MainAxisAlignment, ProgressRing

from ...config import get_subscription
from ...db.models import Client
from ...giga import get_giga_for_data
from ...parsers.vk import extract_info
from ..utils.decorators import loading


def resize_user_icon(parent, e):
    if e.data == 'true':
        parent.user_avatar.max_radius -= 40
    else:
        parent.user_avatar.max_radius += 40
    parent.page.update()


def do_anal(client: Client, data: dict, parent):
    old_but = parent.get_giga_button
    parent.get_giga_button = ProgressRing(width=16, height=16, stroke_width=2)
    parent.page.update()
    req = parent.anal_request.value
    ans = get_giga_for_data(data, req)
    parent.anal_response.value = ans
    parent.get_giga_button = old_but
    parent.page.update()


@loading
def analyze_vk(client: Client, parent):
    vk_data = extract_info(client.vk_link)

    parent.analyzed_info = Text(disabled=True)

    info = []
    if vk_data.get('photo', ''):
        parent.user_avatar = CircleAvatar(foreground_image_url=vk_data['photo'], max_radius=100)
        info.append(parent.user_avatar)

    info.extend([  # Add closable menus
            Text(
                vk_data['error'],
                visible=bool(vk_data['error']),
                color=colors.WHITE,
                bgcolor=colors.RED_ACCENT,
                size=18
            ),

            ExpansionTile(
                title=Text('О странице'),
                controls=[Text(vk_data.get("data", ''))],
                visible=bool(vk_data.get('data', False)),
                on_change=lambda e: resize_user_icon(parent, e),
            ),
#            Slider(min=0, max=10, divisions=10, value=10),  // For choosing dates range
    ])

    if not vk_data['error'] and get_subscription():
        parent.get_giga_button = IconButton(icon=icons.SEND, on_click=lambda e: do_anal(client, vk_data, parent))
        info.append(ExpansionTile(title=Text('Анализ'), controls=[
            parent.anal_request,
            parent.get_giga_button,
            parent.anal_response
        ], on_change=lambda e: resize_user_icon(parent, e)))

    parent.page.dialog = AlertDialog(
        open=True,
        modal=True,
        title=Text(str(client)),
        content=Column(info, tight=True, horizontal_alignment=CrossAxisAlignment.CENTER),
        actions=[
            ElevatedButton(text='Закрыть', on_click=parent.close_dialog)
        ],
        actions_alignment=MainAxisAlignment.CENTER,
    )
    parent.page.update()
