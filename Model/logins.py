###page pour gerer les logins###

import sqlite3

# Connect to the database
conn = sqlite3.connect("login.db")
c = conn.cursor()

# Create the login table if it doesn't exist
c.execute("""
    CREATE TABLE IF NOT EXISTS login (
        username TEXT PRIMARY KEY,
        password TEXT
    )
""")

# Prompt the user to enter a username and password
username = input("Enter a username: ")
password = input("Enter a password: ")

# Insert the user's login information into the database
c.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))
conn.commit()

# Close the database connection
conn.close()
