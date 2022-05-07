from flask import Flask, request, make_response, redirect, render_template
from user_service import get_user_with_credentials, logged_in


app = Flask(__name__)

""" Authentication route flow

Notice how for each route that *DOES* require authentication, we've added the necessary protection
to guard those routes. The process looks something like this:

Authenticated Route:
1. Check to see if user is logged in
    2. If they are, allow them to access route
    3. If they are NOT, redirect them to some page unprotected route (/login in this e.g)

Unauthenticated Route:
**Routes that do not require authentication, are exempt from this process

"""


@app.route("/", methods=["GET"])
def home():
    # Templates are the way to go. Even though you can import `escape` from the `markupsafe` package,
    # always opt to use templating languages, because they're safe by always automatically escaping input field.
    if not logged_in():
        return render_template("login.html")
    return redirect("/dashboard")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user_with_credentials(email, password)
    if not user:
        return render_template("login.html", error="Invalid credentials")
    response = make_response(redirect("/dashboard"))
    response.set_cookie("auth_token", user["token"])
    return response, 303


@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect("/dashboard"))
    response.delete_cookie("auth_token")
    return response, 303


@app.route("/dashboard", methods=["GET"])
def dashboard():
    # e.g of a protected route that requires auth
    if not logged_in():
        return render_template("login.html")
    return render_template("dashboard.html", email=g.user)


@app.route("/details", methods=["GET", "POST"])
def details():
    if not logged_in():
        return render_template("login.html")
    account_number = request.args["account"]
    return render_template("details.html", account_number=account_number)


@app.route("/transfer", methods=["GET"])
def transfer():
    if not logged_in():
        return render_template("login.html")
    return render_template("transfer.html")
