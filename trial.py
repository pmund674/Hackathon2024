import calendar
import datetime

class Event:
    def __init__(self, start_hour, end_hour, name):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.name = name

class ScheduleBuilder:
    def __init__(self):
        self.schedule = {}

    def display_calendar(self, year, month):
        print(calendar.month(year, month))

    def block_time(self, year, month, day, start_hour, end_hour, name):
        date = (year, month, day)
        if date not in self.schedule:
            self.schedule[date] = []
        self.schedule[date].append(Event(start_hour, end_hour, name))
        print("Time blocked successfully!")

    def view_schedule(self, year, month, day):
        date = (year, month, day)
        if date in self.schedule:
            print("Schedule for {}/{}/{}".format(month, day, year))
            for event in self.schedule[date]:
                print("{}:00 - {}:00: {}".format(event.start_hour, event.end_hour, event.name))
        else:
            print("No schedule for {}/{}/{}".format(month, day, year))

    def delete_event(self, year, month, day, start_hour, name):
        date = (year, month, day)
        if date in self.schedule:
            for event in self.schedule[date]:
                if event.start_hour == start_hour and event.name == name:
                    self.schedule[date].remove(event)
                    print("Event deleted successfully!")
                    return
            print("Event not found!")
        else:
            print("No schedule for {}/{}/{}".format(month, day, year))

    def add_recurring_event(self, year, month, day, start_hour, end_hour, name, frequency):
        for i in range(frequency):
            self.block_time(year, month, day + i, start_hour, end_hour, name)
        print("Recurring event added successfully!")

def main():
    builder = ScheduleBuilder()

    while True:
        print("\n1. Display Calendar")
        print("2. Block Time")
        print("3. View Schedule")
        print("4. Delete Event")
        print("5. Add Recurring Event")
        print("6. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            year = int(input("Enter year: "))
            month = int(input("Enter month: "))
            builder.display_calendar(year, month)
        elif choice == "2":
            year = int(input("Enter year: "))
            month = int(input("Enter month: "))
            day = int(input("Enter day: "))
            start_hour = int(input("Enter start hour: "))
            end_hour = int(input("Enter end hour: "))
            name = input("Enter name: ")
            builder.block_time(year, month, day, start_hour, end_hour, name)
        elif choice == "3":
            year = int(input("Enter year: "))
            month = int(input("Enter month: "))
            day = int(input("Enter day: "))
            builder.view_schedule(year, month, day)
        elif choice == "4":
            year = int(input("Enter year: "))
            month = int(input("Enter month: "))
            day = int(input("Enter day: "))
            start_hour = int(input("Enter start hour: "))
            name = input("Enter name: ")
            builder.delete_event(year, month, day, start_hour, name)
        elif choice == "5":
            year = int(input("Enter year: "))
            month = int(input("Enter month: "))
            day = int(input("Enter day: "))
            start_hour = int(input("Enter start hour: "))
            end_hour = int(input("Enter end hour: "))
            name = input("Enter name: ")
            frequency = int(input("Enter frequency: "))
            builder.add_recurring_event(year, month, day, start_hour, end_hour, name, frequency)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()