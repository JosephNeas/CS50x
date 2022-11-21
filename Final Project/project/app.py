import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, random_brewery

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///adopt.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Get breweries information."""
    if request.method == "POST":
        brewery = request.form.get("brewery")
        RPP = request.form.get("number")
        if not brewery:
            return apology("must enter a name")
        try:
            int(RPP)
        except:
            return apology("Must input a number for results per page")
        if int(RPP)<=0:
            return apology("Must enter a number above 0")

        if lookup(brewery, RPP) == None:
            return apology("No such breweries")

        if not RPP:
            return apology("Must input a number for results per page")

        lookup_brewery = lookup(brewery, RPP)
        names = []
        for i in range(len(lookup_brewery)):
            user_id = session["user_id"]
            name = lookup_brewery[i]["brewery"]["name"]
            city = lookup_brewery[i]["brewery"]["city"]
            state = lookup_brewery[i]["brewery"]["state"]
            brewery_id = lookup_brewery[i]["brewery"]["id"]
            brewery_type = lookup_brewery[i]["brewery"]["brewery_type"]
            brewery = {"user_id": user_id, "name": name, "city": city, "state":state, "brewery_id":brewery_id, "brewery_type":brewery_type}
            names.append(brewery)
        return render_template("searched.html", names=names)
    else:
        return render_template("search.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        check = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username was submitted
        if not username:
            return apology("must enter a username")
        # Ensure the username is unique
        elif len(check) != 0:
            return apology("Username already exists")
        # Ensure password was submitted
        elif not password:
            return apology("must enter a password")
        # Ensure the passwords match
        elif password != confirmation:
            return apology("passwords don't match")

        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if not request.form.get("old password") or not check_password_hash(rows[0]["hash"], request.form.get("old password")):
            return apology("must provide current password", 403)

        # Ensure password was submitted
        elif not request.form.get("new password"):
            return apology("must new provide password", 403)
        elif request.form.get("new password") != request.form.get("new confirmation"):
            return apology("passwords didn't match", 403)

        new_password = generate_password_hash(request.form.get("new password"))

        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password, session["user_id"])

        session.clear()

        # Redirect user to login page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")

@app.route("/")
@login_required
def index():
    """Show favorite users favorite breweries"""
    breweries = db.execute("SELECT DISTINCT brewery_name, brewery_type, city, brewery_id, state FROM brewery WHERE user_id = ? GROUP BY user_id, brewery_name", session["user_id"])
    favorites = []

    for brewery in breweries:
        name = brewery["brewery_name"]
        type = brewery["brewery_type"]
        city = brewery["city"]
        state = brewery["state"]
        brewery_id = brewery["brewery_id"]
        favorite = {"name":name, "type":type, "city":city, "state":state, "brewery_id":brewery_id}
        favorites.append(favorite)
    return render_template("index.html", favorites=favorites)

@app.route("/favorite", methods=["POST"])
def favorite():

    id = request.form.get("id")
    name = request.form.get("name")
    brewery_id = request.form.get("brewery_id")
    type = request.form.get("type")
    city = request.form.get("city")
    state = request.form.get("state")
    if id:
        db.execute("INSERT INTO brewery (user_id, brewery_id, brewery_name, brewery_type, city, state) VALUES(?, ?, ?, ?, ?, ?)", id, brewery_id, name, type, city, state)
    return render_template("search.html")

@app.route("/Unfavorite", methods=["POST"])
def Unfavorite():

    id = session["user_id"]
    brewery_id = request.form.get("brewery_id")

    if id:
        db.execute("DELETE FROM brewery WHERE user_id = ? AND brewery_id = ?", id, brewery_id)
    return redirect("/")

@app.route("/random", methods=["GET", "POST"])
def random_brewery_page():

    random_brew = random_brewery()
    if random_brew == None:
        return apology("didn't work")

    name = random_brew["brewery"]["name"]
    type = random_brew["brewery"]["brewery_type"]
    city = random_brew["brewery"]["city"]
    state = random_brew["brewery"]["state"]
    brewery_id = random_brew["brewery"]["id"]
    random = {"name":name, "type":type, "city":city, "state":state, "brewery_id":brewery_id}

    return render_template("random.html", names=random)
