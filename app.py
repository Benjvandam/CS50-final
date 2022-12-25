import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///final.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/",methods=["GET", "POST"])
@login_required
def index():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        return redirect("/create")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        alljobs = db.execute("SELECT * FROM jobs")
        for i in range(len(alljobs)):
            alljobs[i]["worker_name"] = db.execute("SELECT * FROM users WHERE id = ?", alljobs[i]["worker_id"])[0]["username"]
            alljobs[i]["creator_name"] = db.execute("SELECT * FROM users WHERE id = ?", alljobs[i]["creator_id"])[0]["username"]
        return render_template("index.html",alljobs=alljobs)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")



    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password matches with second password
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Passwords don't match", 400)

        # Add username and password to the database
        username = request.form.get("username")
        hashed_password = generate_password_hash(request.form.get("password"))

        # Ensure the user doesn't exist yet and update the database
        check = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(check) == 1:
            return apology("The username already exists", 400)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashed_password)

        # Redirect user to home page
        return redirect("/")

        # User reached route via GET (as by clicking a link or via redirect)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/jobs", methods=["GET", "POST"])
@login_required
def jobs():

    #Save the user id of the user that logged in

    #rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
    # user_id = rows[0]["id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        return redirect("/jobs")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        alljobs = db.execute("SELECT * FROM jobs WHERE worker_id = ?", session["user_id"])
        for i in range(len(alljobs)):
            alljobs[i]["worker_name"] = db.execute("SELECT * FROM users WHERE id = ?", alljobs[i]["worker_id"])[0]["username"]
            alljobs[i]["creator_name"] = db.execute("SELECT * FROM users WHERE id = ?", alljobs[i]["creator_id"])[0]["username"]
        return render_template("jobs.html",alljobs=alljobs)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check if the user selected a date
        date = request.form.get("date")

        if not date:
            return apology("must provide a date", 400)

        # Add the description
        description = request.form.get("description")

        # Add the worker
        worker = request.form.get("worker")
        worker_id = db.execute("SELECT * FROM users WHERE username = ?", worker)[0]["id"]

        if not worker:
            return apology("must provide a worker", 400)

        db.execute("INSERT INTO jobs (creator_id, date, status, description, worker_id) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], date, "Open" , description, worker_id)

        return redirect("/jobs")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Provide the number of available workers
        workers = db.execute("SELECT * FROM users")

        return render_template("create.html",workers=workers)


@app.route('/changeJobStatus/<string:jobID>', methods=["POST"])
def changeJobStatus(jobID):
    jobID = json.loads(jobID)
    copyJobID = jobID
    print("TEST TEST TEST TEST")
    print(copyJobID[0])
    if (copyJobID[1] == "Delete"):
        db.execute("DELETE from jobs WHERE job_id = ?", copyJobID[0])
    else:
        db.execute("UPDATE jobs SET status = ? WHERE job_id = ?", copyJobID[1],copyJobID[0])
    return('/')