#Framework for the Python Web APP
import streamlit as st
# A library for working with data sets
import pandas as pd
# For Security: passlib,hashlib,bcrypt,scrypt
import hashlib
# For database management
import sqlite3 

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
conn = sqlite3.connect('data.db')  # Establishes a connection to the SQLite database stored in the 'data.db' file
c = conn.cursor()  # Creates a cursor object to execute SQL statements

# DB Functions

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
    # Creates a table named 'userstable' if it doesn't exist already in the database.
    # The table has two columns: 'username' (stores usernames as text) and 'password' (stores passwords as text).

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    # Inserts a new user record into the 'userstable' table with the provided username and password.
    # The values are passed as parameters using parameterized queries to prevent SQL injection.
    # The changes are committed to the database.

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data
    # Searches the 'userstable' table for a user record with the provided username and password.
    # If a matching record is found, it returns the data (row) as a list of tuples.
    # If no matching record is found, an empty list is returned.

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data
    # Retrieves all user records from the 'userstable' table.
    # It returns the data (rows) as a list of tuples.


def main():
	"""Espanol"""
	st.title("🇪🇸 Español Interactivo")
	menu = ["Iniciar sesión","Registrarse"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Iniciar sesión":
		st.subheader("Regístrese a través de la barra lateral")
		username = st.sidebar.text_input("Nombre de usuario")
		password = st.sidebar.text_input("Contraseña",type='password')
		if st.sidebar.button("Iniciar sesión"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.success("Conectado como {}".format(username))
			else:
				st.warning("Nombre de usuario/contraseña incorrecto")

	elif choice == "Registrarse":
		st.subheader("Create New Account")
		new_user = st.text_input("Crear una nueva cuenta")
		new_password = st.text_input("Contraseña",type='password')

		if st.button("Registrarse"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("Has creado con éxito una cuenta válida")
			st.info("Vaya al menú de inicio de sesión para iniciar sesión")
        
if __name__ == '__main__':
	main()
