from flask import Flask, request, render_template

app = Flask(__name__)

SPORTS = ["Basketball", "Soccer", "Ultimate Frisbee"]
REGISTRATIONS = {} # Here we store people who register!

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    if not name:
        return render_template("failure.html")
    sport = request.form.get("sport")
    if sport not in SPORTS:
        return render_template("failure.html")
    REGISTRATIONS[name] = sport
    return render_template("success.html")


@app.route("/registrations")
def registrations():
    return render_template("registrations.html", registrations=REGISTRATIONS)