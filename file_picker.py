import tkinter as tk
from tkinter import filedialog, messagebox
from user_database import UserDatabase

class FilePickerWindow(tk.Toplevel):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.title("Allowed Files")
        self.geometry("300x200")
        self.parent = parent
        self.database = database

        self.create_widgets()

    def create_widgets(self):
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        select_button = tk.Button(self, text="Select File", command=self.select_file)
        select_button.pack(pady=10)

        self.populate_listbox()

    def populate_listbox(self):
        allowed_files = self.get_allowed_files()
        for file in allowed_files:
            self.listbox.insert(tk.END, file)

    def get_allowed_files(self):
        if not self.database.authenticated_user:
            messagebox.showinfo("Error", "Please authenticate first.")
            return []

        allowed_extensions = {
            0: [".txt"],
            1: [".png", ".jpg", ".jpeg"],
            2: [".exe"]
        }

        allowed_files = []
        for label, extensions in allowed_extensions.items():
            if self.database.authenticated_user == "admin" or self.database.users[self.database.authenticated_user].get("Acces level") == label:
                allowed_files.extend(extensions)

        return allowed_files

    def select_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_file = self.listbox.get(selected_index[0])
            messagebox.showinfo("Selected File", f"Selected File: {selected_file}")
            self.destroy()
        else:
            messagebox.showinfo("Error", "Please select a file.")

