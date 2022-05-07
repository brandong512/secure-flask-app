import sqlite3
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from flask import request, g
import jwt

SECRET = "bfg28y7efg238re7r6t32gfo23vfy7237yibdyo238do2v3"

""" User authentication flow

The flow of authenticating a user looks something like this

1. Look up user name *and* password in database
    2. If it's found in the database, return relevant information and an authentication token
    3. If it's not found give vague error message about invalid credentials
        - Do not give any specific information about (wrong password, email does not exist, etc...)
4. Every time a user visits a route, check to see if they're logged in (check for a jwt in cookies)
    5. If they have one, allow for access & store email in the Flask session variable (variable g)
    6. If they don't have one, reject access (again with a vague message)
"""


def get_user_with_credentials(email, password):
    try:
        con = sqlite3.connect("bank.db")
        cur = con.cursor()
        cur.execute(
            """
            SELECT email, name, password FROM users where email=?""",
            (email,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        email, name, hash = row
        if not pbkdf2_sha256.verify(password, hash):
            return None
        return {"email": email, "name": name, "token": create_token(email)}
    finally:
        con.close()


def logged_in():
    token = request.cookies.get("auth_token")
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        g.user = data["sub"]
        return True
    except jwt.InvalidTokenError:
        return False


def create_token(email):
    now = datetime.utcnow()
    payload = {"sub": email, "iat": now, "exp": now + timedelta(minutes=60)}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token
