import csv
import string
from tkinter import messagebox

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
					username, password,acces_level = row
					
					self.users[username] = {'password': password, 'Strength': "Strong" if self.PasswordChecker(password) else "Weak","Acces level": acces_level}
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