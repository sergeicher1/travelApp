# run_app.py

from kivy.app import App
from ui import TravelAppUI


class TravelApp(App):
    def build(self):
        return TravelAppUI()


if __name__ == '__main__':
    TravelApp().run()
