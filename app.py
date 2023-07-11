from flask import Flask, render_template, request, session
import requests
from replit import db
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    # Accessing users' requests
    if request.method == "POST":
        print("LOGIN/SIGNUP CLICKED")  # Listening to the button click
        # Getting user's input
        user_name = request.form["user_name"]
        print(f"Hello, {user_name}")

        # Storing the input in session
        session["user"] = user_name

        # Creating/Updating the user database
        user = create_or_update_user(user_name)
    else:
        user = None

    return render_template(
        "index.html",
        dogs_generated=db["total_dogs_generated"],
        dog_image=db["last_dog"],
        users=enumerate(get_leaderboard(db - "users")),
        user=user,
        logins=user["logins"] if user else 0,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=81)
