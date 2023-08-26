# run_app.py

from kivy.app import App
from ui import TravelAppUI


# Define the main app class
class TravelApp(App):
    def build(self):
        app_ui = TravelAppUI()  # Create an instance of TravelAppUI
        app_ui.load_trips_from_file()  # Load trips from file
        return app_ui

if __name__ == '__main__':
    TravelApp().run()
