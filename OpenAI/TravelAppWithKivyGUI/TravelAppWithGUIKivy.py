from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
import re


# Define the Trip class to store trip information
class Trip:
    def __init__(self, destination, start_date, end_date):
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.activities = []

    def add_activity(self, activity):
        self.activities.append(activity)

    def __str__(self):
        activities_str = "\n".join(self.activities)
        return f"Trip to {self.destination} ({self.start_date} - {self.end_date}):\n{activities_str}"


#
# Define the main UI class
class TravelAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.trips = []

        # Create "Create Trip" button
        self.create_trip_button = Button(text="Create Trip")
        self.create_trip_button.bind(on_press=self.show_create_trip_popup)
        self.add_widget(self.create_trip_button)

        # Create "Add Activity" button
        self.add_activity_button = Button(text="Add Activity")
        self.add_activity_button.bind(on_press=self.show_add_activity_popup)
        self.add_widget(self.add_activity_button)

        # Create "Show All Trips" button
        self.show_all_trips_button = Button(text="Show All Trips")
        self.show_all_trips_button.bind(on_press=self.show_all_trips_popup)
        self.add_widget(self.show_all_trips_button)

        # Initialize popup instances
        self.create_trip_popup = None
        self.add_activity_popup = None

        error_popup = None  # Initialize the error popup reference

    # Method to show the "Create Trip" popup
    def show_create_trip_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.destination_input = TextInput(hint_text='Destination')
        self.start_date_input = TextInput(hint_text='Start Date')
        self.end_date_input = TextInput(hint_text='End Date')

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
    def create_trip(self, instance):
        destination = self.destination_input.text
        if not self.is_valid_destination(destination):
            error_callback = lambda instance: self.dismiss_popup(self.error_popup)  # Callback to dismiss error popup
            self.error_popup = self.show_message_popup("Error", "Invalid destination. Please enter only letters.",
                                                       error_callback)
            return

        start_date = self.start_date_input.text
        end_date = self.end_date_input.text
        trip = Trip(destination, start_date, end_date)
        self.trips.append(trip)
        if self.create_trip_popup:  # Check if popup exists before dismissing
            self.create_trip_popup.dismiss()  # Dismiss the popup after creating the trip

    # Method to check if a destination is valid (contains only letters)
    def is_valid_destination(self, destination):
        return bool(re.match("^[A-Za-z]+$", destination))

    # Method to show the "Add Activity" popup
    def show_add_activity_popup(self, instance):
        if not self.trips:
            self.show_message_popup("Error", "No trips available. Create a trip first.")
            return

        content = BoxLayout(orientation='vertical')
        self.trip_spinner = Spinner(values=[trip.destination for trip in self.trips])
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

    # Method to add an activity to a trip
    def add_activity(self, instance, popup):
        selected_trip_destination = self.trip_spinner.text
        activity = self.activity_input.text
        for trip in self.trips:
            if trip.destination == selected_trip_destination:
                trip.add_activity(activity)
                popup.dismiss()  # Dismiss the popup after adding the activity
                return
        self.show_message_popup("Error", "Selected trip not found.")

    def show_all_trips_popup(self, instance):
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
    def show_message_popup(self, title, message, callback=None):
        content = BoxLayout(orientation='vertical')
        message_label = Label(text=message)
        ok_button = Button(text="OK")
        if callback:
            ok_button.bind(on_press=callback)  # Bind the OK button to the provided callback
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        content.add_widget(message_label)
        content.add_widget(ok_button)
        popup.open()
        return popup

    # Method to dismiss a popup
    def dismiss_popup(self, popup):
        if popup:
            popup.dismiss()


# Define the main app class
class TravelApp(App):
    def build(self):
        return TravelAppUI()


# Run the app if executed as the main script
if __name__ == '__main__':
    TravelApp().run()
