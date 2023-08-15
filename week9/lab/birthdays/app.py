import os
import sqlite3
from cs50 import SQL
from db_manager import BirthdayDbManager
from flask import Flask, flash, jsonify, redirect, render_template, request, session
# Constants
from const import ERROR_MESSAGES, ALLOWED_DAYS
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
# db = SQL.connect("birthdays.db")
# SQL interactions

# Custom sql class
db = BirthdayDbManager("birthdays.db", "birthdays")

# Get a list of months
MONTHS = list(range(1, 13))

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get data to append to the table & perform some validations
        name = request.form.get("name")
        if not name:
            return render_template("post_error.html", error=ERROR_MESSAGES["NO_NAME"], value=name)

        month_raw = request.form.get("month")
        # Parse to int attempt
        try:
            month = int(month_raw)
        except ValueError:
            return render_template("post_error.html", error=ERROR_MESSAGES["INVALID_MONTH"], value=month_raw)
        # Sanity check
        if month not in ALLOWED_DAYS.keys():
            return render_template("post_error.html", error=ERROR_MESSAGES["INVALID_MONTH"], value=day_raw)

        day_raw = request.form.get("day")
        try:
            day = int(day_raw)
        except ValueError:
            return render_template("post_error.html", error=ERROR_MESSAGES["INVALID_DAY"], value=day_raw)
        if day not in ALLOWED_DAYS[month]:
            return render_template("post_error.html", error=ERROR_MESSAGES["INVALID_DAY"], value=day_raw)

        # If we get here, we should be fine to write to db :)
        db.insert_birthday(name=name, month=month, day=day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        # get bdays data
        bdays = db.get_birthdays()

        return render_template("index.html", bdays = bdays, months = MONTHS)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        # Render a page with search input name
        name = request.form.get("name")
        if not name:
            return render_template("post_error.html", error=ERROR_MESSAGES["NO_NAME"], value=name)
        results = db.search_birthday_by_name(name)
        return render_template("search.html", name=name, results=results)

    else:
        # Render a vanilla search page with empty params
        return render_template("search.html", name="NULL", results="NULL")



