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


def create_trip():
    destination = input("Enter the destination: ")
    start_date = input("Enter the start date: ")
    end_date = input("Enter the end date: ")
    trip = Trip(destination, start_date, end_date)
    return trip


def add_activity_to_trip(trip):
    activity = input("Enter an activity: ")
    trip.add_activity(activity)


def main():
    trips = []

    while True:
        print("\nMenu:")
        print("1. Create a new trip")
        print("2. Add activity to a trip")
        print("3. Show trips")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            trip = create_trip()
            trips.append(trip)
            print("Trip created successfully!")
        elif choice == '2':
            if not trips:
                print("No trips available. Create a trip first.")
            else:
                for i, trip in enumerate(trips):
                    print(f"{i + 1}. {trip.destination}")
                trip_idx = int(input("Select a trip by index: ")) - 1
                add_activity_to_trip(trips[trip_idx])
                print("Activity added successfully!")
        elif choice == '3':
            for trip in trips:
                print(trip)
        elif choice == '4':
            print("Exiting the travel planning app.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
