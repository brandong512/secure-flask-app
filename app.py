from flask import (
    Flask,
    request,
    make_response,
    redirect,
    render_template,
    g,
    abort,
)
from user_service import get_user_with_credentials, logged_in
from account_service import get_balance, get_owner_accounts, do_transfer
from flask_wtf.csrf import CSRFProtect
from validator import Validation

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

app = Flask(__name__)
app.config["SECRET_KEY"] = "0X41v4FK8A2cbw1hHFFJCwTGZXvuxM592QRrmCzh"
csrf = CSRFProtect(app)


@app.route("/", methods=["GET"])
def home():
    # Templates are the way to go. Even though you can import `escape` from the `markupsafe` package,
    # always opt to use templating languages, because they're safe by always automatically escaping input field.
    # This increases our protection from XSS attacks.

    # If we're not logged in just show the login page, otherwise show the person's dashboard
    if not logged_in():
        return render_template("login.html")
    return redirect("/dashboard")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user_with_credentials(email, password)
    if not user:
        return render_template(
            "login.html",
            error="Invalid credentials",
        )
    response = make_response(redirect("/dashboard"))
    # This steps is important as it sets the cookie in the client that let's us know
    # the person is authenticated
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
    owned_accounts = get_owner_accounts(g.user)
    owned_accounts = [account[0] for account in owned_accounts]
    return render_template(
        "dashboard.html", logged_in=logged_in(), user=g.user, accounts=owned_accounts
    )


@app.route("/details", methods=["GET"])
def details():
    if not logged_in():
        return render_template("login.html")
    account_number = request.args["account"]

    if get_balance(account_number, g.user) is None:
        abort(404, "Account not found")

    return render_template(
        "details.html",
        user=g.user,
        account_number=account_number,
        balance=get_balance(account_number, g.user),
        logged_in=logged_in(),
    )


""" Transfer feature

During a transfer there are many areas that need to be validated. Here are the following scenarios
that we've added some validation against:

1. Transfer amount negative (to prevent withdrawing from other accounts)
2. No transfers greater than $1000
3. Transfering money out of other people's accounts
4. Transferring more money than you actually have
6. Empty strings protection
7. Protection against non-numbers
    
"""


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if not logged_in():
        return render_template("login.html")
    elif logged_in() and request.method == "GET":
        return render_template("transfer.html", logged_in=logged_in(), user=g.user)

    source = request.form.get("from")
    target = request.form.get("to")
    amount = request.form.get("amount")

    if (
        Validation.isBlank(source)
        or Validation.isBlank(target)
        or Validation.isBlank(amount)
    ):
        abort(400, "No blank fields")

    if (
        not Validation.isNumericString(source)
        or not Validation.isNumericString(target)
        or not Validation.isNumericString(amount)
    ):
        abort(400, "Only numbers allowed in fields")

    amount = int(amount)

    if amount < 0:
        abort(400, "NO STEALING")
    if amount > 1000:
        abort(400, "WOAH THERE TAKE IT EASY")

    available_balance = get_balance(source, g.user)
    if available_balance is None:
        abort(404, "Account not found")
    if amount > available_balance:
        abort(400, "You don't have that much")

    transfer_success = do_transfer(source, target, amount)

    if transfer_success:
        return render_template(
            "transfer.html",
            transfer_status="success",
            logged_in=logged_in(),
            user=g.user,
        )
    if not transfer_success:
        return render_template(
            "transfer.html",
            transfer_status="failed",
            logged_in=logged_in(),
            user=g.user,
        )
    else:
        abort(400, "Something bad happened")

    response = make_response(redirect("/dashboard"))
    return response, 303
