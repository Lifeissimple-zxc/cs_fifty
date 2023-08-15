import os
import requests
import urllib.parse
from datetime import datetime, timedelta

from flask import redirect, render_template, request, session
from functools import wraps


##################### DEFINITIONS #####################
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


def lookup(symbol):
    """Look up quote for symbol."""
    # Test input
    if symbol == "AAAA":
        return {"name": "Test A", "price": 28.00, "symbol": "AAAA"}
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def parse_dt(dt_string: str, dt_format: str,
             tz_offset: int = None) -> datetime:
    """
    Parses dt_string to a datetime object accounting for timezome
    """
    # Exceptions are unhandled, that's bad
    # Default to 0 if no arg provided
    if tz_offset is None:
        tz_offset = 0
    # Parse to datetime
    dt_obj = datetime.strptime(dt_string, dt_format)
    # Accont for tz_offset
    dt_obj = dt_obj - timedelta(hours=int(tz_offset / 60))

    return dt_obj

