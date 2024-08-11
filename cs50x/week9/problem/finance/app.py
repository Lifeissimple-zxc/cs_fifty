# https://cs50.harvard.edu/x/2023/psets/9/finance/
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from time import time
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from finance_tools import (
    DbManager,
    DB_TABLES, CONSTANTS
)
from helpers import (
    apology, login_required, lookup, usd, parse_dt,
)
# https://github.com/cs50/checks/blob/master/cs50/2019/x/finance/check50/__init__.py#L19
# https://cs50.stackexchange.com/questions/30068/pset7-finance-check50-doesnt-detect-a-valid-sale-despite-portfolio-updating-cor/30084#30084
# The above seems to be an issue :(
# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
cs50_db = SQL("sqlite:///finance.db")
# Configure custom db for SQL operations
db = DbManager("finance.db")

# Set API_KEY env variable
os.environ["API_KEY"] = CONSTANTS["API_KEY"]

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


####################### Helpers #######################
def fetch_account_data(user_id: int):
    """
    Pulls account data from the DB and API
    """
    summary = db.get_transactions_summary(user_id)
    updated_data = []
    total_value = 0

    for stock in summary:
        entry = stock.copy()  # Not to edit what I am iterating over
        stock_data = lookup(entry["stock"])

        entry["current_price"] = stock_data["price"]
        total_stock_value = entry["current_price"] * entry["shares"]
        entry["total_stock_value"] = total_stock_value

        total_value = total_value + total_stock_value

        updated_data.append(entry)
    del summary

    return updated_data, total_value


def parse_transaction_input(request: request):
    """
    Parses shares and symbol inputs for buy & sell operations
    """
    # Get symbol input
    symbol = request.form.get("symbol")
    if not symbol:
        return apology("Symbol was not provided :(", 400)
    symbol = symbol.upper()

    # Get shares input
    shares = request.form.get("shares")
    if not shares:
        return apology("# of shares was not provided :(", 400)

    # Truncate to two decimals
    try:
        shares = int(shares)
    except ValueError:
        return apology("# of shares provided is not numeric :(", 400)

    # Check for negative number
    if shares < 0:
        return apology("Shares number cannot be negative", 400)

    return symbol, shares


def fetch_stock_data(symbol: str):
    """
    Fetches stock data from the API and handles some errors
    """
    # Get stock data from API
    stock_data = lookup(symbol)
    if stock_data is None:
        return apology("Failed to fetch stock data, try again :(", 503)
    return stock_data


def parse_stock_price(stock_data: dict):
    """
    Extracts price from stock_data
    """
    try:
        stock_price = float(stock_data["price"])
        return stock_price
    except ValueError:
        return apology("Got non-numeric stock price :(", 503)


def perform_transaction(user_id: int, transaction_type: str,
                        symbol: str, shares: float, total_price: float,
                        payment_method: int = None,
                        transactions_table: str = None):
    """
    Handles buy / sell transactions by adding data to the database
    """
    # Default name for transactions table
    if transactions_table is None:
        transactions_table = "transactions"
    # Mapper of transaction types
    transaction_types = {"buy": 1, "sell": 2, "topup": 3}
    transaction_type_id = transaction_types[transaction_type]
    # Prepare data row to insert
    transaction = {
        "transaction_ts": int(time() * 1000),
        "user_id": user_id,
        "transaction_type": transaction_type_id,
        "symbol": symbol,
        "shares": shares,
        "total_price": total_price
    }
    # Add payment method data if provided
    if payment_method is None:
        payment_method = 5

    transaction["payment_method_id"] = payment_method
    print(transaction)
    # Insert data
    db.insert_row(transactions_table, transaction)


def parse_datetime_filters(start: str, end: str,
                           tz_offset: int) -> tuple:
    """
    Parses client's inputs for period start / end  (history page)
    """
    start_utc = parse_dt(dt_string=start, tz_offset=tz_offset,
                         dt_format=CONSTANTS["DATETIME_FORMAT_EXPECTED"])
    start_utc = int(start_utc.timestamp() * 1000)
    end_utc = parse_dt(dt_string=end, tz_offset=tz_offset,
                       dt_format=CONSTANTS["DATETIME_FORMAT_EXPECTED"])
    end_utc = int(end_utc.timestamp() * 1000)
    return start_utc, end_utc


def add_funds(payment_methods: list):
    """
    Powers add funds section in the account page
    """
    # Data manipulation for easier check later in code
    payment_methods_map = {
        entry["paymment_method_name"]: entry["payment_method_id"]
        for entry in payment_methods
    }
    # Parse input
    amount = request.form.get("add_cash_amount")
    payment_method = request.form.get("payment_method")
    if amount is None or payment_method is None:
        return apology("Wrong input:( Try again.", 409)
    # Check that amount is numeric
    try:
        amount = float(amount)
    except ValueError:
        return apology("Amount is not numeric.", 409)
    # Check thhat payment method is supported
    if payment_method not in payment_methods_map:
        return apology("Invalid payment method", 409)
    # Add transaction so that user could see it in historu
    user_id = session["user_id"]
    perform_transaction(user_id=user_id, transaction_type="topup",
                        symbol="cash", shares=amount, total_price=amount,
                        payment_method=payment_methods_map[payment_method])
    # Update balance
    db.increment_user_balance(user_id=user_id, increment=amount)


####################### Routes #######################
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""
    # Get Stock summary
    user_id = session["user_id"]
    stock_summary, stock_value = fetch_account_data(user_id)
    # Get Balance
    user_balance = db.get_data(table="users", id=user_id,
                               cols_needed=["cash"])[0]
    cash = user_balance["cash"]
    user_balance["cash"] = cash
    user_balance["net_worth"] = stock_value + cash
    # Render page with two args (theaders, account_data)
    # Work a JS script to show description of the fields when user hovers over them!
    return render_template("index.html", user_balance=user_balance,
                           stock_summary=stock_summary,
                           account_summary=CONSTANTS["ACCOUNT_SUMMARY"],
                           table_headers=CONSTANTS["INDEX_STOCK_TABLE_HEADERS"])


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    # Handle POST request type
    symbol, shares = parse_transaction_input(request=request)

    # Get stock data from API & parse price
    stock_data = lookup(symbol)
    if stock_data is None:
        return apology(f"Invalid ticker: {symbol}", 400)

    stock_price = parse_stock_price(stock_data)

    # Compute total cost for user
    total_price = shares * stock_price
    # Get user's balance
    user_id = session["user_id"]
    data = db.get_data(cols_needed=["id", "cash"], table="users", id=user_id)
    balance = data[0]["cash"]

    # Check that user has enough before transacting
    if total_price > balance:
        return apology("Not enough cash on balance :(", 409)

    # Handle purchase db-wise
    perform_transaction(user_id=user_id, transaction_type="buy",
                        symbol=symbol, shares=shares, total_price=total_price)
    # Update user's balance
    new_balance = balance - total_price
    db.update_user_balance(user_id, new_balance)
    # Redirect user to home page
    return redirect("/")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    # Read user stocks: user it to render options in GET
    stock_summary, stock_value = fetch_account_data(session["user_id"])
    tickers = [entry["stock"] for entry in stock_summary]
    # Also use it to validate POST filter setup
    if request.method == "GET":
        return render_template("history.html", history_data='NULL',
                               table_headers=CONSTANTS["HISTORY_TABLE_HEADERS"],
                               stock_summary=stock_summary)
    # Parse inputs
    start = request.form.get("period_start")
    end = request.form.get("period_end")
    # Name for the element should probably come form config?
    tz_offset = int(request.form[CONSTANTS["CLIENT_TZ_ELEMENT_NAME"]])
    symbol = request.form.get("symbol")
    # Handle scenario for all stocks
    if symbol == "*":
        symbol = None

    # If start or end are none, apologize and prompt to reenter
    if (start is None) or (end is None):
        return apology("Provided filter dates are invalid:( Try again.", 409)
    # Parse start and end to datetime
    start_utc, end_utc = parse_datetime_filters(start, end, tz_offset)
    if end_utc <= start_utc:
        return apology("Wrong setup: Period end should be greater than start.", 409)
    # Run SQL
    history_data = db.fetch_history(start_utc=start_utc, end_utc=end_utc,
                                    user_id=session["user_id"], symbol=symbol)
    return render_template("history.html", history_data=history_data,
                           table_headers=CONSTANTS["HISTORY_TABLE_HEADERS"],
                           stock_summary=stock_summary)


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
        # rows = cs50_db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        rows = db.get_data("users", username=request.form.get("username"))

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
    if request.method == "GET":
        return render_template("quote.html", stock_data='NULL')

    # Validate input
    symbol = request.form.get("symbol")
    if not symbol:
        return apology("Symbol was not provided :(", 400)
    symbol = symbol.upper()
    # Get stock data from API
    stock_data = lookup(symbol)
    # Check for None
    if stock_data is None:
        return apology("Failed to fetch stock data, try again :(", 400)
    # Successful flow
    return render_template("quoted.html", stock_data=stock_data)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get form data to variables
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)
        # Ensure the password is confirmed
        elif not confirmation:
            return apology("must confirm password", 400)
        # Check that password and confirmation match (should be done on front end)
        elif password != confirmation:
            return apology("confirmation and password are different", 400)

        # At this point the input is validated, but we are not sure if the username is unique
        # Query for username
        duplicates = db.get_data(table=DB_TABLES["users"], username=username)
        # Return error if we get data from db
        if len(duplicates) > 0:
            return apology("Username is already taken", 400)
        # With this check completed, should be fine to send to db
        hash = generate_password_hash(password)
        db.register_new_user(username=username, hashed_password=hash)
        # Regirect to "/"
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stock_summary, stock_value = fetch_account_data(session["user_id"])
    tickers = [entry["stock"] for entry in stock_summary]
    if request.method == "GET":
        return render_template("sell.html", stock_summary=stock_summary)

    # Handle POST request type
    symbol, shares = parse_transaction_input(request=request)
    if symbol not in tickers:
        return apology(f"Account does not have {symbol} :(", 400)

    # Get stock data from API & parse price
    stock_data = lookup(symbol)
    stock_price = parse_stock_price(stock_data)

    # Compute total cost for user
    total_price = shares * stock_price
    # Get user's balance
    user_id = session["user_id"]
    data = db.get_data(cols_needed=["id", "cash"], table="users", id=user_id)
    balance = data[0]["cash"]

    # Check that user has enough shares to sell
    stock_balance_rows = db.get_stock_balance(user_id, symbol)
    if len(stock_balance_rows) > 1:
        return apology("Error reading data from the db", 503)
    stock_balance = stock_balance_rows[0]
    if stock_balance["shares"] < shares:
        return apology(f"Not enough shares of {symbol} :(", 400)

    # Handle purchase db-wise
    perform_transaction(user_id=user_id, transaction_type="sell",
                        symbol=symbol, shares=shares, total_price=total_price)
    # Update user's balance
    new_balance = balance + total_price
    db.update_user_balance(user_id, new_balance)
    # Redirect user to home page
    return redirect("/")


# Extra
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Account page for adding more cash and (potentially) other account features"""
    # Get username from SQL
    user_id = session["user_id"]
    user_data = db.get_data(table="users", cols_needed=["username"], id=user_id)
    # Get payment method data from db
    payment_methods = db.get_data(table="payment_methods")
    if len(user_data) > 1:
        return apology("Database Error", 500)
    user_data = user_data[0]
    if (username := user_data.get("username")) is None:
        return apology("Database Error", 500)

    if request.method == "GET":
        return render_template("account.html", username=username,
                               payment_methods=payment_methods)
    # This handles different posts

    if (operation_type := request.form.get("operation_type")) == "add_cash":
        add_funds(payment_methods)

    return redirect("/")

