###Fichier pour s'incrire, peut-etre deplacer la partie CREATE TABLE de logins.py ###

import sqlite3

# Connect to the database
conn = sqlite3.connect("../Visual/app/login.db")
c = conn.cursor()

# Prompt the user to enter a username and password
username = input("Enter your username: ")
password = input("Enter your password: ")

# Query the database for the username and password
c.execute("SELECT * FROM login WHERE username = ? AND password = ?", (username, password))
result = c.fetchone()

# Check if a matching username and password were found
if result:
    print("Login successful!")
else:
    print("Invalid username or password.")

# Close the database connection
conn.close()
