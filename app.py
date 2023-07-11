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


@app.route("/get_dog")
def get_dog():
    # requesting for the random dog API
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    dog_image = data["message"]
    print(db["total_dogs_generated"])

    # Storing the most recent dog image
    db["last_dog"] = dog_image

    # Checking if the user is in session
    if session["user"]:
        user = user = get_user_from_database(session["user"])
        user["dogs_generated"] += 1

    # Incrementing the number of dogs generated in the database
    db["total_dogs_generated"] += 1

    return render_template(
        "index.html",
        dog_image=dog_image,
        users=enumerate(get_leaderboard(db["users"])),
        user=user,
        dogs_generated=db["total_dogs_generated"],
    )


# LOGOUT FUNCTIONALITY
@app.route("/logout")
def logout():
    session["user"] = None
    return render_template("index.html", dogs_generated=["total_dogs_generated"])


# ___FUNCTIONS___#
def create_or_update_user(user_name):
  # Filtering
  user = get_user_from_database(user_name)

  # Checking if user exists in the database
  if user:
      print("USER EXISTS!")  # In the console
      user["logins"] += 1
      print(user)
  else:
      print("NEW USER!")  # In the console

      # Adding new user
      db["users"].append({"user_name": user_name, "logins": 1, "dogs_generated": 0})
    user = get_user_from_database(user_name)

  return user


def get_user_from_database(user_name):
  # Filtering
  user = [user for user in db["users"] if user["user_name"] == user_name]

  # Redefining --> either {} or None
  user = user[0] if user else None

  return user


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=81)
