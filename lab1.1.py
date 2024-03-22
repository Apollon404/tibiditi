import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv
import string
import tkinter.simpledialog

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

class UserDatabase:
    def __init__(self):
        self.users = {}
        self.authenticated_user = None  

    def PasswordChecker(self, password):
        check=0
        if any(i.isdigit() for i in password):
            check+=1
        if any(i.isupper() for i in password):
            check+=1
        if any(i.islower() for i in password):
            check+=1
        if ((i in string.punctuation) for i in password):
            check+=1
            pass
        return check>=3 and (len(password) >= 8)
        
    def load_database(self, filename):
        try:
            with open(filename, "r", newline='') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    username, password = row
                    
                    self.users[username] = {'password': password, 'Strength': "Strong" if self.PasswordChecker(password) else "Weak"}
        except FileNotFoundError:
            pass

    def save_database(self, filename):
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for username, data in self.users.items():
                writer.writerow([username, data['password']])

    def add_user(self, username, password, filename):
        if username not in self.users:
            if self.PasswordChecker(password):
                self.users[username] = {'password': password, 'Strength': "Strong"}
                self.save_database(filename)
                messagebox.showinfo("Success", "User added successfully. Password is strong.")
                return True
            else:
                user_confirmation = messagebox.askyesno("Password Warning", "The password is weak. Do you still want to proceed?")
                if user_confirmation:
                    self.users[username] = {'password': password, 'Strength': "Weak"}
                    self.save_database(filename)
                    messagebox.showinfo("Success", "User added successfully. Password is weak.")
                    return True
                else:
                    messagebox.showinfo("Cancelled", "User creation cancelled.")
                    return False
        else:
            messagebox.showinfo("Error", "User with the same username already exists.")
            return False

    def delete_user(self, username, filename):
        if username in self.users:
            del self.users[username]
            self.save_database(filename)
            return True
        else:
            messagebox.showinfo("Error", "User not found.")
            return False

    def authenticate_user(self, username, password):
        if (username in self.users and self.users[username]['password'] == password) or (username=='admin' and password=='admin'):
            self.authenticated_user = username
            messagebox.showinfo("Authentication", f"Authentication successful. Welcome, {username}!")
            return True
        else:
            messagebox.showinfo("Authentication", "Authentication failed. Invalid username or password.")
            return False

class App:
    file_path = ""

    def __init__(self, root):
        self.root = root
        self.root.title("ТБД_Левківський")

        self.database = UserDatabase()

        self.create_menu()
        self.create_file_selection()
        self.create_table()
        self.create_user_input()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        about_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Про автора", menu=about_menu)
        about_menu.add_command(label="Інформація про автора", command=self.show_author_info)

        login_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Login", menu=login_menu)
        login_menu.add_command(label="Authenticate", command=self.show_authentication_window)

    def show_authentication_window(self):
        if not self.database.authenticated_user:
            authentication_window = AuthenticationWindow(self.root, self.database, self)

    def create_file_selection(self):
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)

        self.selected_file_label = tk.Label(file_frame, text="Оберіть файл бази даних:")
        self.selected_file_label.grid(row=0, column=0, padx=10)

        select_file_button = tk.Button(file_frame, text="Обрати файл", command=self.select_file)
        select_file_button.grid(row=0, column=1)

    def create_table(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("Username", "Password", "Strength"), show="headings")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.heading("Strength", text="Strength")
        self.tree.pack()

        delete_user_button = tk.Button(table_frame, text="Видалити користувача", command=self.delete_user)
        delete_user_button.pack(pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_select)

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            selected_data = self.tree.item(selected_item)['values']
            print(selected_data)

    def create_user_input(self):
        user_input_frame = tk.Frame(self.root)
        user_input_frame.pack(pady=10)

        username_label = tk.Label(user_input_frame, text="Username:")
        username_label.grid(row=0, column=0, padx=10)
        self.username_entry = tk.Entry(user_input_frame)
        self.username_entry.grid(row=0, column=1, padx=10)

        password_label = tk.Label(user_input_frame, text="Password:")
        password_label.grid(row=0, column=2, padx=10)
        self.password_entry = tk.Entry(user_input_frame, show="*")
        self.password_entry.grid(row=0, column=3, padx=10)

        add_user_button = tk.Button(user_input_frame, text="Додати користувача", command=self.add_user)
        add_user_button.grid(row=0, column=6)

    def add_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if self.database.add_user(username, password, self.file_path):
                self.update_table()
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Error", "All fields (username, password) are required.")

    def delete_user(self):
        selected_item = self.tree.selection()
        if selected_item:
            selected_data = self.tree.item(selected_item)['values']
            if selected_data:
                username = selected_data[0]
                if self.database.delete_user(username, self.file_path):
                    self.update_table()

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for username, data in self.database.users.items():
            if self.database.authenticated_user == "admin":
                self.tree.insert("", "end", values=(username, data['password'], data['Strength']))
            elif username == self.database.authenticated_user:
                self.tree.insert("", "end", values=(username, data['password'], data['Strength']))
            else:
                self.tree.insert("", "end", values=(username, "*****", "Strong" if self.database.PasswordChecker(data['password']) else "Weak"))
                
    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            self.selected_file_label.config(text=f"Обраний файл: {self.file_path}")
            self.database.load_database(self.file_path)
            self.update_table()

    def show_author_info(self):
        messagebox.showinfo("Інформація про автора", "Номер групи: БІ-442\nПрізвище, ім'я: Левківський Ярослав Олексійович")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
