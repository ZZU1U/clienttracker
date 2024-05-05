from flet import app
from clienttracker.gui.app import ClientTracker
from clienttracker.db.test import test_data

test_data()

app(
    ClientTracker,
    # view=ft.AppView.WEB_BROWSER
)
