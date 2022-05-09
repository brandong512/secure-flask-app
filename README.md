# A Secure Flask App

This repo contains code that serves as a good basis for a _secure_ flask app. There are a number of good practices demonstrated in this repo which include:

- Proper password storage through hashing & salting
- Basic authorization which prevents users from accessing accounts that don't belong to them
- Authentication with JWT to keep track of logged in user sessions
- Protecting routes from users that aren't authenticated
- Error handling & validation to prevent the system from continuously running in a compromised state
- Proper use of templating library to prevent XSS attacks
- Usage of prepared SQL statements to prevent SQL injection
- Usage of Flask's built-in CSRF protection to prevent authenticated user sessions from being hijacked

---

## Getting Started

Once you clone the repo create a virtual environment and then activate it. Then install the requirements like so:

```
pip install -r requirements.txt
```

**You may have `deactivate` then `activate` your virtual environment again to access your dependencies**

Next, add the flask environment variables to your shell session.

**on Unix based environment**

```
export FLASK_ENV=development
export FLASK_APP=app
```

**on Windows based OS**
[See here for more info on other CLI's](https://flask.palletsprojects.com/en/2.1.x/cli/)

Finally run,

```
flask run
```

and the server should start up.

The file structure of your folder should look something like this:

```.
├── README.md
├── account_service.py
├── app.py
├── bank.db
├── bin
│   ├── createdb.py
│   └── makeaccounts.py
├── env
│   ├── bin
│   ├── include
│   ├── lib
│   └── pyvenv.cfg
├── requirements.txt
├── static
│   └── styles.css
├── templates
│   ├── base.html
│   ├── dashboard.html
│   ├── details.html
│   ├── login.html
│   └── transfer.html
├── user_service.py
└── validator.py
```
