import tkinter as tk
from tkinter import messagebox

class AuthenticationWindow(tk.Toplevel):
    def __init__(self, parent, database, app):
        super().__init__(parent)
        self.title("Authentication")
        self.geometry("300x200")
        self.parent = parent
        self.database = database
        self.app = app

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.authenticate_user).pack(pady=10)

    def authenticate_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if self.database.authenticate_user(username, password):
                self.app.update_table()
                self.destroy()
        else:
            messagebox.showinfo("Error", "All fields (username, password) are required.")
