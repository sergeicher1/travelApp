# ui.py
import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
import re
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from trip import Trip


#
# Define the main UI class
class TravelAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.trips = []

        # Create a horizontal BoxLayout for the logo and button
        logo_and_button_layout = BoxLayout(orientation='horizontal')

        # Create a FloatLayout to center the logo and button both vertically and horizontally
        center_layout = FloatLayout()

        # Add the logo image widget to the center layout, centered horizontally and vertically
        logo_image = Image(source='E:\pyCharm\kivy\OpenAI\TravelAppWithKivyGUI\sources\logo.png',
                           size_hint=(None, None), size=(300, 300))
        logo_image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Centered both horizontally and vertically
        center_layout.add_widget(logo_image)
        # Add the center layout to the main UI layout
        self.add_widget(center_layout)

        # Create an AnchorLayout to center the "Create Trip" button
        create_trip_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.create_trip_button = Button(text="Create Trip", size_hint=(None, None), size=(200, 100))
        self.create_trip_button.bind(on_press=self.show_create_trip_popup)
        create_trip_layout.add_widget(self.create_trip_button)
        self.add_widget(create_trip_layout)

        # Create an AnchorLayout to center the "Add Activity" button
        add_activity_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.add_activity_button = Button(text="Add Activity", size_hint=(None, None), size=(200, 100))
        self.add_activity_button.bind(on_press=self.show_add_activity_popup)
        add_activity_layout.add_widget(self.add_activity_button)
        self.add_widget(add_activity_layout)

        # Create an AnchorLayout to center the "Show All Trips" button
        show_all_trips_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        self.show_all_trips_button = Button(text="Show All Trips", size_hint=(None, None), size=(200, 100))
        self.show_all_trips_button.bind(on_press=self.show_all_trips_popup)
        show_all_trips_layout.add_widget(self.show_all_trips_button)
        self.add_widget(show_all_trips_layout)

        # Initialize popup instances
        self.create_trip_popup = None
        self.add_activity_popup = None
        self.selected_trip = None  # Initialize selected_trip
        error_popup = None  # Initialize the error popup reference

    # Method to show the "Create Trip" popup
    def show_create_trip_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.destination_input = TextInput(hint_text='Destination')
        self.start_date_input = TextInput(hint_text='Start Date (dd/mm/yyyy)')
        self.end_date_input = TextInput(hint_text='End Date (dd/mm/yyyy)')

        create_button = Button(text="Create")
        create_button.bind(on_press=lambda instance: self.create_trip(instance))  # Pass only the instance

        close_button = Button(text="Close")
        close_button.bind(on_press=lambda instance: self.dismiss_popup(self.create_trip_popup))  # Pass popup instance

        content.add_widget(self.destination_input)
        content.add_widget(self.start_date_input)
        content.add_widget(self.end_date_input)
        content.add_widget(create_button)
        content.add_widget(close_button)

        self.create_trip_popup = Popup(title='Create Trip', content=content, size_hint=(None, None), size=(400, 300))
        self.create_trip_popup.open()

    # Method to create a new trip
    def is_valid_date(self, date_str):
        pattern = r"\d{2}/\d{2}/\d{4}"  # Pattern for dd/mm/yyyy format
        return re.match(pattern, date_str)

    def is_valid_date_format(self, date_str):
        try:
            datetime.datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    def create_trip(self, instance):
        destination = self.destination_input.text.strip()
        start_date = self.start_date_input.text.strip()
        end_date = self.end_date_input.text.strip()

        if not destination or not start_date or not end_date:
            self.show_message_popup("Error", "Please fill in all fields.")
            return

        # Verify date format for start_date
        if not self.is_valid_date_format(start_date):
            self.show_message_popup("Error", "Invalid start date format. Please use dd/mm/yyyy.")
            return

        # Verify date format for end_date
        if not self.is_valid_date_format(end_date):
            self.show_message_popup("Error", "Invalid end date format. Please use dd/mm/yyyy.")
            return
        destination = self.destination_input.text
        if not self.is_valid_destination(destination):
            error_callback = lambda instance: self.dismiss_popup(self.error_popup)
            self.error_popup = self.show_message_popup("Error", "Invalid destination. Please enter only letters.",
                                                       error_callback)
            return

        start_date = self.start_date_input.text
        if not self.is_valid_date(start_date):
            error_callback = lambda instance: self.dismiss_popup(self.error_popup)
            self.error_popup = self.show_message_popup("Error", "Invalid start date format. Please use dd/mm/yy.",
                                                       error_callback)
            return

        end_date = self.end_date_input.text
        if not self.is_valid_date(end_date):
            error_callback = lambda instance: self.dismiss_popup(self.error_popup)
            self.error_popup = self.show_message_popup("Error", "Invalid end date format. Please use dd/mm/yy.",
                                                       error_callback)
            return

        trip = Trip(destination, start_date, end_date)
        self.trips.append(trip)
        if self.create_trip_popup:
            self.create_trip_popup.dismiss()

    # Method to check if a destination is valid (contains only letters)
    def is_valid_destination(self, destination):
        return bool(re.match("^[A-Za-z]+$", destination))

    # Method to show the "Add Activity" popup
    def show_add_activity_popup(self, instance):
        if not self.trips:
            self.show_message_popup("Error", "No trips available. Create a trip first.")
            return

        content = BoxLayout(orientation='vertical')
        trip_values = [trip.destination for trip in self.trips]
        self.trip_spinner = Spinner(values=trip_values, text="Select a Trip")
        self.activity_input = TextInput(hint_text='Activity')

        add_button = Button(text="Add")
        add_button.bind(
            on_press=lambda instance: self.add_activity(instance, self.add_activity_popup))  # Pass popup instance

        close_button = Button(text="Close")
        close_button.bind(on_press=lambda instance: self.dismiss_popup(self.add_activity_popup))  # Pass popup instance

        content.add_widget(self.trip_spinner)
        content.add_widget(self.activity_input)
        content.add_widget(add_button)
        content.add_widget(close_button)

        self.add_activity_popup = Popup(title='Add Activity', content=content, size_hint=(None, None), size=(400, 300))
        self.add_activity_popup.open()

    def on_trip_select(self, trip_text):
        self.trip_spinner.text = trip_text  # Update text of the dropdown button
        self.selected_trip = trip_text  # Store selected trip
        self.trip_dropdown.dismiss()  # Dismiss the dropdown after selection

    # Method to add an activity to a trip
    def add_activity(self, instance, popup):
        selected_trip_destination = self.trip_spinner.text
        if selected_trip_destination == "Select a Trip":
            self.show_message_popup("Error", "Please select a trip first.")
            return

        activity = self.activity_input.text
        for trip in self.trips:
            if trip.destination == selected_trip_destination:
                trip.add_activity(activity)
                popup.dismiss()  # Dismiss the popup after adding the activity
                return
        self.show_message_popup("Error", "Selected trip not found.")

    def show_all_trips_popup(self, instance):
        if not self.trips:
            self.show_message_popup("Info", "No active trips.")
            return

        content = BoxLayout(orientation='vertical')
        trips_list = Label(text='\n'.join([str(trip) for trip in self.trips]), halign='center')

        close_button = Button(text="Close")
        close_button.bind(on_press=lambda instance: self.dismiss_popup(
            self.show_all_trips_popup_instance))  # Use a distinct variable name

        content.add_widget(trips_list)
        content.add_widget(close_button)

        self.show_all_trips_popup_instance = Popup(title='All Trips', content=content, size_hint=(None, None),
                                                   size=(400, 300))
        self.show_all_trips_popup_instance.open()

    # Method to show a message popup
    def show_message_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        message_label = Label(text=message)

        ok_button = Button(text="OK")
        ok_button.bind(on_press=lambda instance: self.dismiss_popup(self.error_popup))  # Dismiss the error popup

        content.add_widget(message_label)
        content.add_widget(ok_button)

        self.error_popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        self.error_popup.open()

    # Method to dismiss a popup
    def dismiss_popup(self, popup):
        if popup:
            popup.dismiss()
