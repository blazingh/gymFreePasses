from re import template
from flask import Flask, redirect, url_for, render_template, request
import user_adder
import append_user
import validator

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/submition", methods=["POST", "GET"])
def submition():
    if request.method == "POST":
        mess = user_adder.user_pass(request.form["name"], request.form["phone"], request.form["email"])
        return render_template("message.html", mess=mess)

    return render_template("user_input.html")

@app.route("/append", methods=["POST", "GET"])
def append():
    if request.method == "POST":
        mess = append_user.append_user(request.form["code"], request.form["name"], request.form["phone"])
        return render_template("message.html", mess=mess)

    return render_template("user_append.html")

@app.route("/checkin", methods=["POST", "GET"])
def checkin():

    if request.method == "POST":
        valid = validator.validate(request.form["code"])
        if valid[0]:
            if valid[1]:
                output = (valid[2], valid[3], valid[4])

                return render_template("checkin.html", res=output)

            output = (valid[2], "")

            return render_template("checkin.html", res=output)

        output = (valid[1], "")

        return render_template("checkin.html", res=output)

    return render_template("checkin.html", res=[])


if __name__ == "__main__":
    app.run(debug=True)