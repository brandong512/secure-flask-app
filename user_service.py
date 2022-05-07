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
    """Checking for a user in the database
    1. Check the database for a user with the email requested
        2. If there is no such email --> Display error message
        3. If there is, use hashing function to check and see if inputted password has
           matches the stored & salted password hash
        4. If they match, create token, and send back to the user
        5. If they don't match --> Display error message
    """

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
        # We use pbkdf2_sha256 to check the password (automatically salted)
        if not pbkdf2_sha256.verify(password, hash):
            return None
        return {"email": email, "name": name, "token": create_token(email)}
    finally:
        con.close()


def logged_in():
    # We can see if this person is logged in by checking to see if in
    # their cookies they have the auth_token parameter set
    token = request.cookies.get("auth_token")
    try:
        # If we're able to decode the JWT with our secret successfully we're good
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        g.user = data["sub"]
        return True
    except jwt.InvalidTokenError:  # Otherwise, that's an invalid token
        return False


def create_token(email):
    # This is the standard formot for JWT's, and we can use the handy jwt library to make our own with a secret
    now = datetime.utcnow()
    payload = {"sub": email, "iat": now, "exp": now + timedelta(minutes=60)}
    token = jwt.encode(payload, SECRET, algorithm="HS256")
    return token
