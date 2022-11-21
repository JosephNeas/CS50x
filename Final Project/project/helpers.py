import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(brewery, RPP):
    """Look up brewery."""
    # Contact API
    try:
        url = f"https://api.openbrewerydb.org/breweries?by_name={brewery}&per_page={RPP}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        quote = response.json()
    except (KeyError, TypeError, ValueError):
        return None

    RPP = int(RPP)
    names_list = []
    i = 0
    if RPP > len(quote):
        RPP = len(quote)
        while i < RPP:
            names = {"brewery": quote[i]}
            names_list.append(names)
            i += 1
    else:
        while i < RPP:
            names = {"brewery": quote[i]}
            names_list.append(names)
            i += 1

    if names_list:
        return names_list
    else:
        return None

def random_brewery():
    """Look up random brewery."""
    # Contact API
    try:
        url = "https://api.openbrewerydb.org/breweries/random"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    try:
        quote = response.json()
        return {
            "brewery": quote[0]
        }
    except (KeyError, TypeError, ValueError):
        return None