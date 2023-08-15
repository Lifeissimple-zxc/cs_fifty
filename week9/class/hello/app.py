from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
# can be whatever, index is just more common
def index():
    if request.method == "GET":
        # Render template finds file with the name provided in the templates folder
        return render_template("index.html")#, name=name)
    elif request.method == "POST":
        # request.args is for GET, for POST we use request.form
        return render_template("greet.html", name = request.form.get("name", "World"))


# @app.route("/greet", methods=["POST"])
# def greet():
#     return render_template("greet.html", name = request.args.get("name", "World"))

# CONTINUE from minute 58