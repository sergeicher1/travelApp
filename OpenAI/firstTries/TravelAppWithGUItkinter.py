import tkinter as tk
from tkinter import messagebox

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

class TravelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Planning App")
        self.trips = []

        self.create_trip_button = tk.Button(root, text="Create Trip", command=self.create_trip)
        self.create_trip_button.pack()

        self.add_activity_button = tk.Button(root, text="Add Activity", command=self.add_activity)
        self.add_activity_button.pack()

        self.show_trips_button = tk.Button(root, text="Show Trips", command=self.show_trips)
        self.show_trips_button.pack()

    def create_trip(self):
        trip_window = tk.Toplevel(self.root)

        destination_label = tk.Label(trip_window, text="Destination:")
        destination_label.pack()
        self.destination_entry = tk.Entry(trip_window)
        self.destination_entry.pack()

        start_date_label = tk.Label(trip_window, text="Start Date:")
        start_date_label.pack()
        self.start_date_entry = tk.Entry(trip_window)
        self.start_date_entry.pack()

        end_date_label = tk.Label(trip_window, text="End Date:")
        end_date_label.pack()
        self.end_date_entry = tk.Entry(trip_window)
        self.end_date_entry.pack()

        submit_button = tk.Button(trip_window, text="Create", command=self.save_trip)
        submit_button.pack()

    def save_trip(self):
        destination = self.destination_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        trip = Trip(destination, start_date, end_date)
        self.trips.append(trip)
        messagebox.showinfo("Success", "Trip created successfully!")

    def add_activity(self):
        activity_window = tk.Toplevel(self.root)

        trip_label = tk.Label(activity_window, text="Select Trip:")
        trip_label.pack()
        self.trip_var = tk.StringVar(activity_window)
        self.trip_var.set(self.trips[0].destination if self.trips else "")
        trip_dropdown = tk.OptionMenu(activity_window, self.trip_var, *([trip.destination for trip in self.trips]))
        trip_dropdown.pack()

        activity_label = tk.Label(activity_window, text="Activity:")
        activity_label.pack()
        self.activity_entry = tk.Entry(activity_window)
        self.activity_entry.pack()

        submit_button = tk.Button(activity_window, text="Add Activity", command=self.save_activity)
        submit_button.pack()

    def save_activity(self):
        selected_trip_destination = self.trip_var.get()
        activity_text = self.activity_entry.get()
        for trip in self.trips:
            if trip.destination == selected_trip_destination:
                trip.add_activity(activity_text)
                break
        messagebox.showinfo("Success", "Activity added successfully!")

    def show_trips(self):
        if not self.trips:
            messagebox.showinfo("Info", "No trips available. Create a trip first.")
        else:
            trips_text = "\n\n".join(str(trip) for trip in self.trips)
            trips_window = tk.Toplevel(self.root)
            trips_label = tk.Label(trips_window, text=trips_text)
            trips_label.pack()

def main():
    root = tk.Tk()
    app = TravelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
