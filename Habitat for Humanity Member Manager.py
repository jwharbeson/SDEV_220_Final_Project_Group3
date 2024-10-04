import tkinter as tk
from tkinter import messagebox
from datetime import date

# Class to store member data
class Member:
    def __init__(self, first_name, last_name, address, email_address, contact_phone, birthday, join_date):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.email_address = email_address
        self.contact_phone = contact_phone
        self.birthday = birthday
        self.join_date = join_date
        self.skills = []  # List to store member's skills

    def add_skill(self, skill):
        self.skills.append(skill)

# Class to store role/skills and assign them to members
class Role:
    def __init__(self, role_name):
        self.role_name = role_name
        self.members = []  # List to store members in this role

    def assign_member(self, member):
        self.members.append(member)

    def get_members(self):
        return [f"{m.first_name} {m.last_name}" for m in self.members]

# Class for handling communications (letters/emails)
class Communication:
    def __init__(self):
        self.messages = []

    def schedule_message(self, member, message):
        self.messages.append((member, message, date.today()))

    def send_messages(self):
        for msg in self.messages:
            member, message, _ = msg
            print(f"Sending '{message}' to {member.first_name} {member.last_name} ({member.email_address})")
        self.messages.clear()  # Clear after sending

# Collections to organize data
members = []  # List to store all members
roles = {}    # Dictionary to store roles by name and corresponding members
communication_system = Communication()  # Communication instance

class MemberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habitat for Humanity Member Manager")

        # Increase window size for a better layout
        self.root.geometry("1000x1000")
        self.root.configure(background='gray55')

        # Labels and Entry fields for member details with consistent size
        entry_width = 60

        # First Name
        self.first_name_label = tk.Label(root, text=" First Name: ", relief='groove', borderwidth=3, background='gray25', fg='white')
        self.first_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.first_name_entry = tk.Entry(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Last Name
        self.last_name_label = tk.Label(root, text=" Last Name: ", relief='groove', borderwidth=3, background='gray25', fg='white')
        self.last_name_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.last_name_entry = tk.Entry(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Address
        self.address_label = tk.Label(root, text=" Address: ", relief='groove', borderwidth=3, background='gray25', fg='white')
        self.address_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.address_entry = tk.Entry(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.address_entry.grid(row=2, column=1, padx=10, pady=5)

        #Email Address
        self.email_label = tk.Label(root, text=" Email: ", relief='groove', borderwidth=3, background='gray25', fg='white')
        self.email_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = tk.Entry(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.email_entry.grid(row=3, column=1, padx=10, pady=5)

        # Primary Contact Phone #
        self.contact_label = tk.Label(root, text=" Primary Contact Phone #: ", relief='groove', borderwidth=3, background='gray25', fg='white')
        self.contact_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.contact_entry = tk.Entry(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.contact_entry.grid(row=4, column=1, padx=10, pady=5)

        # Birthday
        self.birthday_label = tk.Label(root, text=" Birthday (MM-DD-YYYY): ", relief='groove', borderwidth=3, background='gray25', fg='white')
        self.birthday_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.birthday_entry = tk.Entry(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.birthday_entry.grid(row=5, column=1, padx=10, pady=5)

        # Join Date
        self.join_date_label = tk.Label(root, text=" Join Date (MM-DD-YYYY): ", relief='groove', borderwidth=3, background='gray25', fg='white')
        self.join_date_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.join_date_entry = tk.Entry(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.join_date_entry.grid(row=6, column=1, padx=10, pady=5)

        # Add Member button
        self.add_button = tk.Button(root, text=" Add Member", command=self.add_member, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.add_button.grid(row=7, column=1, padx=10, pady=10)

        # List to display members
        self.members_listbox = tk.Listbox(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.members_listbox.grid(row=8, column=0, columnspan=2, sticky="e", padx=10, pady=10)

        # Assign Role button
        self.assign_role_button = tk.Button(root, text=" Assign Role", command=self.assign_role, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.assign_role_button.grid(row=9, column=1, padx=10, pady=10)

        # View Role Members button
        self.view_roles_button = tk.Button(root, text=" View Role Members", command=self.view_role_members, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.view_roles_button.grid(row=10, column=1, padx=10, pady=10)

        # Role Entry (Moved below View Role Members button)
        self.role_label = tk.Label(root, text=" Role: ", relief='groove', borderwidth=3, background='gray25', fg='white')
        self.role_label.grid(row=11, column=0, sticky="w", padx=10, pady=5)
        self.role_entry = tk.Entry(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.role_entry.grid(row=11, column=1, padx=10, pady=5)

        # Schedule Message button
        self.message_button = tk.Button(root, text="Schedule Message", command=self.schedule_message, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.message_button.grid(row=13, column=1, padx=10, pady=10)

        # Send Message button
        self.send_message_button = tk.Button(root, text="Send Messages", command=self.send_messages, relief='raised', borderwidth=3, background='gray64', fg='black')
        self.send_message_button.grid(row=14, column=1, padx=10, pady=10)

        # Custom message entry
        self.custom_message_label = tk.Label(root, text=" Custom Message: ", relief='groove', borderwidth=3, background='gray25', fg='white')
        self.custom_message_label.grid(row=15, column=0, sticky="w", padx=10, pady=5)
        self.custom_message_entry = tk.Entry(root, width=entry_width, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.custom_message_entry.grid(row=15, column=1, padx=10, pady=5)

        # Text box to display role members
        self.role_members_textbox = tk.Listbox(root, width=entry_width, height=10, relief='sunken', borderwidth=3, background='gray64', fg='black')
        self.role_members_textbox.grid(row=12, column=0, columnspan=2, sticky="e", padx=10, pady=10)

    def add_member(self):
        # Get the details from the entries
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        address = self.address_entry.get()
        email_address = self.email_entry.get()
        contact_phone = self.contact_entry.get()
        birthday = self.birthday_entry.get()
        join_date = self.join_date_entry.get()

        if not first_name or not contact_phone:
            messagebox.showwarning("Input Error", "First name and contact phone are required!")
            return

        # Create a new member object and add it to the list
        member = Member(first_name, last_name, address, email_address, contact_phone, birthday, join_date)
        members.append(member)

        # Update the display list
        self.members_listbox.insert(tk.END, f"{first_name} {last_name} - {contact_phone} - {email_address}")

        # Clear the entry fields
        self.clear_fields()

    def assign_role(self):
        # Get selected member and role
        selected_index = self.members_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No member selected!")
            return

        role_name = self.role_entry.get()
        if not role_name:
            messagebox.showwarning("Input Error", "Please enter a role.")
            return

        member = members[selected_index[0]]

        # Assign the role to the member
        if role_name not in roles:
            roles[role_name] = Role(role_name)
        roles[role_name].assign_member(member)

        messagebox.showinfo("Role Assignment", f"{member.first_name} {member.last_name} assigned to role '{role_name}'.")

    def view_role_members(self):
        role_name = self.role_entry.get()
        if role_name not in roles:
            messagebox.showwarning("Role Error", "Role does not exist.")
            return

        role_members = roles[role_name].get_members()
        self.role_members_textbox.delete("1.0", tk.END)  # Clear existing text
        self.role_members_textbox.insert(tk.END, f"Members in role '{role_name}':\n")
        self.role_members_textbox.insert(tk.END, "\n".join(role_members))

    def schedule_message(self):
        # Get selected member and custom message
        selected_index = self.members_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Selection Error", "No member selected!")
            return

        member = members[selected_index[0]]
        custom_message = self.custom_message_entry.get()

        if not custom_message:
            messagebox.showwarning("Input Error", "Please enter a message.")
            return

        # Schedule a message for the member
        communication_system.schedule_message(member, custom_message)
        messagebox.showinfo("Message Scheduled", f"Message scheduled for {member.first_name} {member.last_name}.")

    def send_messages(self):
        communication_system.send_messages()
        messagebox.showinfo("Messages Sent", "All scheduled messages have been sent.")

    def clear_fields(self):
        # Clear all entry fields
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.birthday_entry.delete(0, tk.END)
        self.join_date_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)
        self.custom_message_entry.delete(0, tk.END)

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MemberApp(root)
    root.mainloop()