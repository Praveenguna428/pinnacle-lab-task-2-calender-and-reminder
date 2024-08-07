import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reminders
                      (id INTEGER PRIMARY KEY, date TEXT, reminder TEXT)''')
    conn.commit()
    conn.close()

# Add a reminder to the database
def add_reminder(date, reminder):
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (date, reminder) VALUES (?, ?)", (date, reminder))
    conn.commit()
    conn.close()

# Get reminders for a specific date
def get_reminders(date):
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT reminder FROM reminders WHERE date=?", (date,))
    reminders = cursor.fetchall()
    conn.close()
    return reminders

# Delete a reminder from the database
def delete_reminder(date, reminder):
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reminders WHERE date=? AND reminder=?", (date, reminder))
    conn.commit()
    conn.close()

# Display reminders for a selected date
def show_reminders():
    selected_date = cal.selection_get()
    reminders = get_reminders(selected_date)
    reminders_text = "\n".join([reminder[0] for reminder in reminders]) if reminders else "No reminders for this date."
    messagebox.showinfo("Reminders", reminders_text)

# Add a new reminder
def add_reminder_prompt():
    selected_date = cal.selection_get()
    reminder = reminder_entry.get()
    if reminder:
        add_reminder(selected_date, reminder)
        messagebox.showinfo("Success", "Reminder added successfully!")
        reminder_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter a reminder.")

# Delete a reminder
def delete_reminder_prompt():
    selected_date = cal.selection_get()
    reminder = reminder_entry.get()
    if reminder:
        delete_reminder(selected_date, reminder)
        messagebox.showinfo("Success", "Reminder deleted successfully!")
        reminder_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter a reminder to delete.")

# Initialize the main application window
root = tk.Tk()
root.title("Monthly Calendar with Reminders")

# Create the calendar widget
cal = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
cal.pack(pady=20)

# Create an entry widget for adding reminders
reminder_entry = tk.Entry(root, width=50)
reminder_entry.pack(pady=10)

# Create buttons for adding, showing, and deleting reminders
add_btn = tk.Button(root, text="Add Reminder", command=add_reminder_prompt)
add_btn.pack(pady=5)

show_btn = tk.Button(root, text="Show Reminders", command=show_reminders)
show_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete Reminder", command=delete_reminder_prompt)
delete_btn.pack(pady=5)

# Initialize the database
init_db()

# Start the main application loop
root.mainloop()
