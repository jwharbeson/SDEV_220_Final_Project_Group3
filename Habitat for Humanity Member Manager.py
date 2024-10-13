import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import threading
import time
import os
import json

# Class to store member data
class Member:
    def __init__(self, first_name: str, last_name: str, address: str, email_address: str, contact_phone: str, birthday: str, join_date: str, role: str = None):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email_address = email_address
        self.contact_phone = contact_phone
        self.birthday = birthday
        self.join_date = join_date
        self.skills = []
        self.role = role  # Initialize role

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def get_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address,
            'email_address': self.email_address,
            'contact_phone': self.contact_phone,
            'birthday': self.birthday,
            'join_date': self.join_date,
            'role': self.role
        }

# Class to handle communications (letters/emails)
class Communication:
    def __init__(self):
        self.messages = []  # To store messages

    def schedule_message(self, member, message, send_time):
        self.messages.append((member, message, send_time))  # Store message with send time
        threading.Thread(target=self._send_message, args=(member, message, send_time)).start()  # Start a new thread to send message

    def _send_message(self, member, message, send_time):
        # Calculate how long to wait before sending the message
        delay = (send_time - datetime.now()).total_seconds()
        if delay > 0:
            time.sleep(delay)  # Wait until it's time to send the message

        print(f"Sending '{message}' to {member.first_name} {member.last_name} ({member.email_address})")

# Collections to organize data
members = []
communication_system = Communication()

class MemberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habitat for Humanity Member Manager")
        self.root.geometry("850x1000")
        self.root.resizable(width=False, height=False)

        # Load the image
        image_path = os.path.join(os.path.dirname(__file__), "main.png")  # Use the current directory
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        background_label = tk.Label(self.root, image=photo)
        background_label.place(x=400, y=250, relwidth=0.6, relheight=0.5)
        self.photo = photo  

        # Labels and Entry fields for member details
        entry_width = 60
        self.first_name_entry = self.create_label_entry("First Name", 0)
        self.last_name_entry = self.create_label_entry("Last Name", 1)
        self.address_entry = self.create_label_entry("Address", 2)
        self.email_entry = self.create_label_entry("Email", 3)
        self.contact_entry = self.create_label_entry("Primary Contact Phone #", 4)
        self.birthday_entry = self.create_label_entry("Birthday (MM-DD-YYYY)", 5)
        self.join_date_entry = self.create_label_entry("Join Date (MM-DD-YYYY)", 6)
        
        # List to display members
        self.members_listbox = tk.Listbox(root, width=25, height=25, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.members_listbox.grid(row=10, column=0, sticky="nsew", padx=10, pady=10) 
        
        # Add Member button
        self.add_button = tk.Button(root, text="Add Member", command=self.add_member, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.add_button.grid(row=7, column=1, padx=5, pady=5)

        # Role Management
        self.assign_role_button = tk.Button(root, text="Assign Role", command=self.assign_role, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.assign_role_button.grid(row=8, column=1, padx=5, pady=5)

        self.view_role_members_button = tk.Button(root, text="View Role Members", command=self.view_role_members, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.view_role_members_button.grid(row=9, column=1, padx=5, pady=5)

        # Save and Load buttons
        self.save_button = tk.Button(root, text="Save Members", command=self.save_members, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.save_button.grid(row=11, column=1, padx=5, pady=5)

        self.load_button = tk.Button(root, text="Load Members", command=self.load_members, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.load_button.grid(row=12, column=1, padx=5, pady=5)

        # Schedule Message button
        self.message_button = tk.Button(root, text="Schedule Message", command=self.schedule_message, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.message_button.grid(row=13, column=1, padx=10, pady=10)

    def create_label_entry(self, label_text, row):
        label = tk.Label(self.root, text=label_text, relief='groove', borderwidth=3, background='gray25', fg='white')
        label.grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(self.root, width=60, relief='sunken', borderwidth=3, background='gray64', fg='black')
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def add_member(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        address = self.address_entry.get()
        email_address = self.email_entry.get()
        contact_phone = self.contact_entry.get()
        birthday = self.birthday_entry.get()
        join_date = self.join_date_entry.get()

        if not (first_name and last_name and address and email_address and contact_phone and birthday and join_date):
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return

        new_member = Member(first_name, last_name, address, email_address, contact_phone, birthday, join_date)
        members.append(new_member)
        self.members_listbox.insert(tk.END, f"{first_name} {last_name}")

        # Clear entry fields
        self.clear_entries()

    def clear_entries(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.birthday_entry.delete(0, tk.END)
        self.join_date_entry.delete(0, tk.END)

    def assign_role(self):
        selected_index = self.members_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a member.")
            return

        member = members[selected_index[0]]
        role = simpledialog.askstring("Input", f"Enter the role for {member.first_name} {member.last_name}:")
        if not role:
            messagebox.showwarning("Input Error", "Please enter a role.")
            return

        member.role = role  # Assign the role
        messagebox.showinfo("Success", f"Role '{role}' assigned to {member.first_name} {member.last_name}.")

    def view_role_members(self):
        role = simpledialog.askstring("Input", "Enter the role to view members:")
        if not role:
            messagebox.showwarning("Input Error", "Please enter a role.")
            return

        role_members = [f"{m.first_name} {m.last_name}" for m in members if m.role == role]
        if role_members:
            members_str = "\n".join(role_members)
            messagebox.showinfo("Members with Role", f"Members with role '{role}':\n{members_str}")
        else:
            messagebox.showinfo("Members with Role", f"No members found with role '{role}'.")

    def schedule_message(self):
        selected_index = self.members_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a member.")
            return

        member = members[selected_index[0]]
        message = simpledialog.askstring("Input", f"Enter the message for {member.first_name} {member.last_name}:")
        if not message:
            messagebox.showwarning("Input Error", "Please enter a message.")
            return

        # Get the date and time for scheduling
        date_time_str = simpledialog.askstring("Input", "Enter the date and time to send the message (YYYY-MM-DD HH:MM):")
        if not date_time_str:
            messagebox.showwarning("Input Error", "Please enter a date and time.")
            return
        
        try:
            send_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
            if send_time < datetime.now():
                messagebox.showwarning("Input Error", "Please enter a future date and time.")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid date and time in the format YYYY-MM-DD HH:MM.")
            return

        communication_system.schedule_message(member, message, send_time)
        messagebox.showinfo("Success", f"Message scheduled to be sent to {member.first_name} {member.last_name} at {send_time}.")

    def save_members(self):
        file_path = os.path.join(os.path.dirname(__file__), "members_data.json")  # Save to a JSON file
        with open(file_path, 'w') as f:
            json.dump([member.get_dict() for member in members], f, indent=4)
        messagebox.showinfo("Success", "Members data saved successfully!")

    def load_members(self):
        file_path = os.path.join(os.path.dirname(__file__), "members_data.json")  # Load from a JSON file
        if not os.path.exists(file_path):
            messagebox.showwarning("File Not Found", "No saved data found.")
            return
        
        with open(file_path, 'r') as f:
            member_data = json.load(f)
        
        global members
        members = [Member.from_dict(data) for data in member_data]  # Load members from data
        self.members_listbox.delete(0, tk.END)  # Clear the listbox
        for member in members:
            self.members_listbox.insert(tk.END, f"{member.first_name} {member.last_name}")  # Populate the listbox
        messagebox.showinfo("Success", "Members data loaded successfully!")

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MemberApp(root)
    root.mainloop()

