import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class FilePickerWindow(tk.Toplevel):
    allowed_files=None
    def __init__(self, parent, database, directory):
        super().__init__(parent)
        self.title("Allowed Files")
        self.geometry("300x200")
        self.parent = parent
        self.database = database
        self.directory = directory

        self.create_widgets()

    def create_widgets(self):
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-Button-1>", self.open_selected_file)
        select_button = tk.Button(self, text="Select File", command=self.select_file)
        select_button.pack(pady=10)

        self.populate_listbox()

    def populate_listbox(self):
        self.allowed_files = self.get_allowed_files(self.directory)
        for file_path in self.allowed_files:
            file_name = os.path.basename(file_path)  # Extract the file name from the full path
            self.listbox.insert(tk.END, file_name)

    def get_allowed_files(self, directory):
        if not self.database.authenticated_user:
            messagebox.showinfo("Error", "Please authenticate first.")
            return []

        allowed_extensions = {
            0: [".txt"],
            1: [".png", ".jpg", ".jpeg"],
            2: [".exe"]
        }

        allowed_files = []
        current_access_level = int(self.get_user_access_level(self.database.authenticated_user))
        for root, _, files in os.walk(directory):
            for file in files:
                file_name, file_ext = os.path.splitext(file)
                for access_level, extensions in allowed_extensions.items():
                    if access_level <= current_access_level and file_ext in extensions:
                        allowed_files.append(os.path.join(root, file_name + file_ext))

        return allowed_files

    def get_user_access_level(self, username):
        if username in self.database.users:
            return self.database.users[username].get("Access level", None)
        elif username == 'admin':
            return 2
        else:
            messagebox.showinfo("Error", "User not found.")
            return None

    def open_selected_file(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_file = self.allowed_files[selected_index[0]]
            file_ext = os.path.splitext(selected_file)[1].lower()
            if file_ext in [".png", ".jpg", ".jpeg"]:
                self.open_image(selected_file)
            elif file_ext == ".exe":
                self.open_executable(selected_file)
            elif file_ext == ".txt":
                self.open_text_file(selected_file)
            else:
                messagebox.showinfo("Error", "File type not supported.")
            self.destroy()
        else:
            messagebox.showinfo("Error", "Please select a file.")
        

    def select_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_file = self.allowed_files[selected_index[0]]
            file_ext = os.path.splitext(selected_file)[1].lower()
            if file_ext in [".png", ".jpg", ".jpeg"]:
                self.open_image(selected_file)
            elif file_ext == ".exe":
                self.open_executable(selected_file)
            elif file_ext == ".txt":
                self.open_text_file(selected_file)
            else:
                messagebox.showinfo("Error", "File type not supported.")
            self.destroy()
        else:
            messagebox.showinfo("Error", "Please select a file.")

    def open_image(self, file_path):
        try:
            image = Image.open(file_path)
            image.show()
        except Exception as e:
            messagebox.showinfo("Error", f"Failed to open image: {str(e)}")

    def open_executable(self, file_path):
        try:
            os.system(file_path)
        except Exception as e:
            messagebox.showinfo("Error", f"Failed to open executable: {str(e)}")

    def open_text_file(self, file_path):
        try:
            os.system(f"notepad.exe {file_path}")
        except Exception as e:
            messagebox.showinfo("Error", f"Failed to open text file: {str(e)}")
