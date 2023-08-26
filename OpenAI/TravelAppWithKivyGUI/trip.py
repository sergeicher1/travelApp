
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
