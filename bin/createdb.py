import sqlite3
from passlib.hash import (
    pbkdf2_sha256,
)  # pbk_df2_sha256 is used to create salted hashed passwords for storage in our db

con = sqlite3.connect("bank.db")
cur = con.cursor()
cur.execute(
    """
    CREATE TABLE users (
        email text primary key, name text, password text)"""
)

# Use prepared statements/bound-parameters to prevent SQL Injection. NEVER use
# string interpolation to build queries. In actual production environments, it's
# an even better idea to use a programmatic database interface (e.g ORM)
cur.execute(
    "INSERT INTO users VALUES (?, ?, ?)",
    ("alice@example.com", "Alice Xu", pbkdf2_sha256.hash("123456")),
)
cur.execute(
    "INSERT INTO users VALUES (?, ?, ?)",
    ("bob@example.com", "Bobby Tables", pbkdf2_sha256.hash("123456")),
)
con.commit()
con.close()
