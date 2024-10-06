import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import threading
from datetime import datetime, timedelta

class Event:
    def __init__(self, start_hour, end_hour, name, email):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.name = name
        self.email = email
        self.date_time = None

class ScheduleBuilder:
    def __init__(self):
        self.schedule = {}

    def block_time(self, year, month, day, start_hour, end_hour, name, email):
        date = (year, month, day)
        event = Event(start_hour, end_hour, name, email)
        event.date_time = datetime(year, month, day, start_hour)
        
        if date not in self.schedule:
            self.schedule[date] = []
        self.schedule[date].append(event)
        
        # Schedule email reminders
        self.schedule_email_reminders(event)
        return "Time blocked successfully!"

    def schedule_email_reminders(self, event):
        """Schedule emails to be sent 1 day and 10 minutes before the event."""
        event_time = event.date_time
        day_before = event_time - timedelta(days=1)
        ten_minutes_before = event_time - timedelta(minutes=10)

        # Scheduling day-before reminder
        schedule.every().day.at(day_before.strftime("%H:%M")).do(self.send_email_reminder, event, "Reminder: Your event is tomorrow!")

        # Scheduling 10-minutes-before reminder
        schedule.every().day.at(ten_minutes_before.strftime("%H:%M")).do(self.send_email_reminder, event, "Reminder: Your event is in 10 minutes!")

    def send_email_reminder(self, event, message):
        """Sends an email reminder."""
        try:
            sender_email = "sreeragvaddel@example.com"  # Replace with your email
            sender_password = "yourpassword"  # Replace with your email password

            # Create the email content
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = event.email
            msg['Subject'] = f"Reminder: {event.name} event"

            body = f"{message}\n\nEvent: {event.name}\nTime: {event.start_hour}:00 - {event.end_hour}:00"
            msg.attach(MIMEText(body, 'plain'))

            # Setup the SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Change this if not using Gmail
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, event.email, text)
            server.quit()

            print(f"Reminder email sent to {event.email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def view_schedule(self, year, month, day):
        date = (year, month, day)
        if date in self.schedule:
            events = ["{}:00 - {}:00: {} (Email: {})".format(event.start_hour, event.end_hour, event.name, event.email) for event in self.schedule[date]]
            return "\n".join(events)
        else:
            return "No events scheduled for {}/{}/{}".format(month, day, year)

    def delete_event(self, year, month, day, start_hour, name):
        date = (year, month, day)
        if date in self.schedule:
            for event in self.schedule[date]:
                if event.start_hour == start_hour and event.name == name:
                    self.schedule[date].remove(event)
                    return "Event deleted successfully!"
            return "Event not found!"
        else:
            return "No events found for {}/{}/{}".format(month, day, year)

    def add_recurring_event(self, year, month, day, start_hour, end_hour, name, email, frequency):
        for i in range(frequency):
            self.block_time(year, month, day + i, start_hour, end_hour, name, email)
        return "Recurring event added successfully!"

class App:
    def __init__(self, root):
        self.builder = ScheduleBuilder()
        self.root = root
        self.root.title("Schedule Manager")

        # Main Title
        self.label = tk.Label(root, text="Schedule Manager", font=('Helvetica', 16))
        self.label.pack(pady=10)

        # Block Time Button
        self.block_button = tk.Button(root, text="Block Time", command=self.block_time_gui)
        self.block_button.pack(pady=5)

        # View Schedule Button
        self.view_button = tk.Button(root, text="View Schedule", command=self.view_schedule_gui)
        self.view_button.pack(pady=5)

        # Delete Event Button
        self.delete_button = tk.Button(root, text="Delete Event", command=self.delete_event_gui)
        self.delete_button.pack(pady=5)

    def block_time_gui(self):
        block_window = tk.Toplevel(self.root)
        block_window.title("Block Time")

        # Labels and Entries for input
        tk.Label(block_window, text="Year:").grid(row=0, column=0)
        year_entry = tk.Entry(block_window)
        year_entry.grid(row=0, column=1)

        tk.Label(block_window, text="Month:").grid(row=1, column=0)
        month_entry = tk.Entry(block_window)
        month_entry.grid(row=1, column=1)

        tk.Label(block_window, text="Day:").grid(row=2, column=0)
        day_entry = tk.Entry(block_window)
        day_entry.grid(row=2, column=1)

        tk.Label(block_window, text="Start Hour:").grid(row=3, column=0)
        start_hour_entry = tk.Entry(block_window)
        start_hour_entry.grid(row=3, column=1)

        tk.Label(block_window, text="End Hour:").grid(row=4, column=0)
        end_hour_entry = tk.Entry(block_window)
        end_hour_entry.grid(row=4, column=1)

        tk.Label(block_window, text="Event Name:").grid(row=5, column=0)
        name_entry = tk.Entry(block_window)
        name_entry.grid(row=5, column=1)

        tk.Label(block_window, text="Email:").grid(row=6, column=0)
        email_entry = tk.Entry(block_window)
        email_entry.grid(row=6, column=1)

        # Add a checkbox for a recurring event
        is_recurring = tk.IntVar()  # 1 for recurring, 0 for not
        recurring_checkbox = tk.Checkbutton(block_window, text="Recurring Event?", variable=is_recurring)
        recurring_checkbox.grid(row=7, columnspan=2)

        # Entry for frequency (only if recurring)
        tk.Label(block_window, text="Frequency (in days):").grid(row=8, column=0)
        frequency_entry = tk.Entry(block_window)
        frequency_entry.grid(row=8, column=1)

        def block_time_action():
            year = int(year_entry.get())
            month = int(month_entry.get())
            day = int(day_entry.get())
            start_hour = int(start_hour_entry.get())
            end_hour = int(end_hour_entry.get())
            name = name_entry.get()
            email = email_entry.get()

            # Check if the event is recurring
            if is_recurring.get():
                frequency = int(frequency_entry.get())  # Get frequency from the entry
                result = self.builder.add_recurring_event(year, month, day, start_hour, end_hour, name, email, frequency)
            else:
                result = self.builder.block_time(year, month, day, start_hour, end_hour, name, email)

            messagebox.showinfo("Info", result)

        submit_button = tk.Button(block_window, text="Block Time", command=block_time_action)
        submit_button.grid(row=9, column=1)

    def view_schedule_gui(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Schedule")

        tk.Label(view_window, text="Year:").grid(row=0, column=0)
        year_entry = tk.Entry(view_window)
        year_entry.grid(row=0, column=1)

        tk.Label(view_window, text="Month:").grid(row=1, column=0)
        month_entry = tk.Entry(view_window)
        month_entry.grid(row=1, column=1)

        tk.Label(view_window, text="Day:").grid(row=2, column=0)
        day_entry = tk.Entry(view_window)
        day_entry.grid(row=2, column=1)

        def view_schedule_action():
            year = int(year_entry.get())
            month = int(month_entry.get())
            day = int(day_entry.get())

            events = self.builder.view_schedule(year, month, day)
            messagebox.showinfo("Schedule", events)

        submit_button = tk.Button(view_window, text="View Schedule", command=view_schedule_action)
        submit_button.grid(row=3, column=1)

    def delete_event_gui(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Event")

        tk.Label(delete_window, text="Year:").grid(row=0, column=0)
        year_entry = tk.Entry(delete_window)
        year_entry.grid(row=0, column=1)

        tk.Label(delete_window, text="Month:").grid(row=1, column=0)
        month_entry = tk.Entry(delete_window)
        month_entry.grid(row=1, column=1)

        tk.Label(delete_window, text="Day:").grid(row=2, column=0)
        day_entry = tk.Entry(delete_window)
        day_entry.grid(row=2, column=1)

        tk.Label(delete_window, text="Start Hour:").grid(row=3, column=0)
        start_hour_entry = tk.Entry(delete_window)
        start_hour_entry.grid(row=3, column=1)

        tk.Label(delete_window, text="Event Name:").grid(row=4, column=0)
        name_entry = tk.Entry(delete_window)
        name_entry.grid(row=4, column=1)

        def delete_event_action():
            year = int(year_entry.get())
            month = int(month_entry.get())
            day = int(day_entry.get())
            start_hour = int(start_hour_entry.get())
            name = name_entry.get()

            result = self.builder.delete_event(year, month, day, start_hour, name)
            messagebox.showinfo("Info", result)

        submit_button = tk.Button(delete_window, text="Delete Event", command=delete_event_action)
        submit_button.grid(row=5, column=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
