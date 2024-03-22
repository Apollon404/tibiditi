import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv

class UserDatabase:
    def init(self):
        self.users = {}
    def PasswordChecker(self, password):
        return any(i.isdigit()  for i in password) and any(i.isupper()  for i in password) and any(i.islower()  for i in password) and (len(password)>=8)
    def load_database(self, filename):
        try:
            with open(filename, "r", newline='') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    username, password = row
                    
                    self.users[username] = {'password': password, 'Strenght': "Strong" if self.PasswordChecker(password) else "Week"}
        except FileNotFoundError:
            pass

    def save_database(self, filename):
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for username, data in self.users.items():
                writer.writerow([username, data['password']])

    def add_user(self, username, password, filename):
        if username not in self.users:
            self.users[username] = {'password': password }
            self.save_database(filename)
            return True
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

    def change_password(self, username, new_password):
        if username in self.users:
            self.users[username]['password'] = new_password
            self.save_database()
            return True
        else:
            messagebox.showinfo("Error", "User not found.")
            return False

    def authenticate_user(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            messagebox.showinfo("Authentication", f"Authentication successful. Welcome, {username}!")
            return True
        else:
            messagebox.showinfo("Authentication", "Authentication failed. Invalid username or password.")
            return False

class App:
    file_path = ""

    def init(self, root):
        self.root = root
        self.root.title("Назва дисципліни_Прізвище")

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

        self.tree = ttk.Treeview(table_frame, columns=("Username", "Password", "Strenght"), show="headings")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.heading("Strenght", text="Strenght")
        self.tree.pack()

        delete_user_button = tk.Button(table_frame, text="Видалити користувача", command=self.delete_user)
        delete_user_button.pack(pady=10)
        # Додаємо обробник подій для визначення виділеного рядка
        self.tree.bind("<ButtonRelease-1>", self.on_select)

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            # Отримуємо дані з виділеного рядка (рядок складається з кортежу)
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

        if username and password :
            if self.database.add_user(username, password, self.file_path):
                self.update_table()
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Error", "All fields (username, password) are required.")

    def delete_user(self):
        selected_item = self.tree.selection()
        if selected_item:
            # Отримуємо дані з виділеного рядка (рядок складається з кортежу)
            selected_data = self.tree.item(selected_item)['values']
            if selected_data:
                username = selected_data[0]
                if self.database.delete_user(username, self.file_path):
                    self.update_table()

    def update_table(self):
        # Очищення таблиці перед оновленням
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Оновлення таблиці з даними користувачів
        for username, data in self.database.users.items():
            self.tree.insert("", "end", values=(username, data['password'], "Strong" if self.database.PasswordChecker(data['password']) else "Week"))

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            self.selected_file_label.config(text=f"Обраний файл: {self.file_path}")
            self.database.load_database(self.file_path)
            self.update_table()

    def show_author_info(self):
        messagebox.showinfo("Інформація про автора", "Номер групи: [Номер групи]\nПрізвище, ім'я: [Прізвище Ім'я]")

if name == "main":
    root = tk.Tk()
    app = App(root)
    root.mainloop()