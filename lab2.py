import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from authentication_window import AuthenticationWindow
from user_database import UserDatabase

import tkinter as tk
from file_picker import FilePickerWindow
from tkinter import filedialog, ttk, messagebox
from authentication_window import AuthenticationWindow
from user_database import UserDatabase

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

		file_menu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="File", menu=file_menu)
		
		file_menu.add_command(label="Open File Picker", command=self.open_file_picker)
		file_menu.add_command(label="Exit", command=self.root.quit)

		login_menu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Login", menu=login_menu)
		login_menu.add_command(label="Authenticate", command=self.show_authentication_window)
	
	def open_file_picker(self):
		file_picker_window = FilePickerWindow(self.root, self.database)

	def create_file_selection(self):
		file_frame = tk.Frame(self.root)
		file_frame.pack(pady=10)

		self.selected_file_label = tk.Label(file_frame, text="Selected File: None")
		self.selected_file_label.pack()

		if file_path:
			self.selected_file_label.config(text=f"Selected File: {file_path}")
			self.file_path = file_path


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
			#print(selected_data)

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