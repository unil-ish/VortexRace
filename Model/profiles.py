### Page pour les profils, contenant le dashboard, les statistiques, videos favorites, et la currente equipe. ###

import sqlite3
from werkzeug.security import generate_password_hash

# Connect to the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user information
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, 
                                 username TEXT NOT NULL UNIQUE, 
                                 password TEXT NOT NULL,
                                 admin BOOLEAN NOT NULL)''')

# Insert a user into the table
username = 'user1'
password = generate_password_hash('password1')
admin = False
c.execute('''INSERT INTO users (username, password, admin)
             VALUES (?, ?, ?)''', (username, password, admin))

# Save changes and close the connection
conn.commit()
conn.close()
print(3)