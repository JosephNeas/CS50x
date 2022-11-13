import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime, date


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
db.execute("CREATE TABLE IF NOT EXISTS transactions (id INTEGER, user_id NUMERIC NOT NULL, symbol TEXT NOT NULL, shares NUMERIC NOT NULL, \
    time DEFAULT CURRENT_TIMESTAMP NOT NULL, price_paid NUMERIC NOT NULL, PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users(id))")
db.execute("CREATE INDEX IF NOT EXISTS transaction_user_id ON transactions (user_id)")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    transaction_list = []
    tot = 0

    users = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])
    user_cash = users[0]["cash"]

    transactions = db.execute(
        "SELECT user_id, symbol, SUM(shares) as sum_shares FROM transactions WHERE user_id = ? GROUP BY user_id, symbol", session["user_id"])

    for transaction in transactions:
        symbol = transaction["symbol"]
        shares = int(transaction["sum_shares"])
        price = round(float(lookup(symbol)["price"]*int(shares)), 2)
        current = round(float(lookup(symbol)["price"]), 2)
        user = {"user_id": session["user_id"], "symbol": symbol, "shares": shares, "price": usd(price), "current": usd(current)}
        tot += price
        transaction_list.append(user)
    total = user_cash + tot

    return render_template("index.html", cash=usd(user_cash), user=transaction_list, total=usd(total))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        id = session["user_id"]
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("number must be a whole number")

        if not symbol:
            return apology("must enter a stock symbol")
        elif (lookup(symbol) == None):
            return apology("no such symbol")
        elif (shares < 0):
            return apology("must enter number greater than 0")

        price = round(float(lookup(symbol)["price"]*int(shares)),2)
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", id)
        user_cash = user_cash[0]["cash"]
        cash = user_cash - float(price)

        if (cash < 0):
            return apology("you don't have enough money")

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, id)
        db.execute("INSERT INTO transactions (symbol, shares, price_paid, user_id, time) VALUES(?, ?, ?, ?, ?)",
        symbol, shares, price, id, datetime.now())

        flash("Bought!")

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must enter a stock symbol")
        if lookup(symbol) == None:
            return apology("symbol does not exist")
        price = usd(lookup(symbol)["price"])
        return render_template("qutoed.html", price=price)
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    transactions = db.execute(
        "SELECT symbol, sum(shares) as sum_shares FROM transactions WHERE user_id = ? GROUP BY user_id, symbol", session["user_id"])

    if request.method == "POST":
        id = session["user_id"]
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol:
            return apology("must enter a stock symbol")
        elif (lookup(symbol) == None):
            return apology("no such symbol")
        if(shares <= 0):
            return apology("must enter a valid number of shares")

        symbols_list = []
        for transaction in transactions:
            trans_symbol = transaction["symbol"]
            trans_shares = int(transaction["sum_shares"])
            symbols = {"symbol": trans_symbol, "shares": trans_shares}
            symbols_list.append(symbols)

        for sym in symbols_list:
            if (symbol == sym["symbol"] and shares > int(sym["shares"])):
                return apology("Don't have that many shares")

        price = round(float(lookup(symbol)["price"]*int(shares)),2)
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", id)[0]["cash"]
        cash = user_cash + float(price)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, id)
        db.execute("INSERT INTO transactions (symbol, shares, price_paid, user_id, time) VALUES(?, ?, ?, ?, ?)",
        symbol, -(shares), price,  id, datetime.now())

        flash("Sold!")

        return redirect("/")
    else:
        return render_template("sell.html", symbols=transactions)


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

# export API_KEY=pk_01bccc4f974e47219e9a86bb1290b338