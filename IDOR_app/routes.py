import os
import functools
from textwrap import indent
from flask import (
                    Flask,
                    Blueprint,
                    render_template,
                    session,
                    abort,
                    request,
                    flash,
                    redirect,
                    url_for,
                    current_app
)
from IDOR_app.modules.mongo import User
from passlib.hash import pbkdf2_sha256


pages = Blueprint(
    "pages", __name__, template_folder="templates", static_folder="static"
)


# Index page
@pages.route("/")
def index():
    return render_template("index.html", title="PasswordApp - Home", email=session.get("email"))


# Login page
@pages.route("/login", methods=["GET", "POST"])
def login():

    email = ""

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        
        # creates object from class if email is found in DB
        # if user isn't created app crashes. Added to list for dev
        user = User.from_mongo_email(email)
    
        # checks password against hashed version in DB w/ same hashing parameters to see if its matched
        if pbkdf2_sha256.verify(password, user.password):

            # If yes, starts a session in browser & redirects to successful sign in
            session["email"] = email
            return redirect(url_for("pages.protected"))

            # abort(401) if false
            # or just flash message
        else:
            flash("Incorrect User or Password. Please try again.")
            return redirect(url_for('pages.login'))
        
    return render_template("login.html", title="PasswordApp - Login", email=email)


# Signup page
@pages.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        # Hashing password for storage in DB
        password = pbkdf2_sha256.hash(request.form.get("password"))

        # Horrible incrementing kickstart for _id generation. 
        # Just bumps up 1 each time an account is added.
        id = 1
        for entry in current_app.db.AccountsSaved.find({}):
            id += 1     
     
        user = User(id, email, password)
        user.save_to_mongo()
        session["email"] = email

        flash("Successfully signed up")
        return redirect(url_for('pages.login'))
    return render_template("signup.html", title="PasswordApp - Sign Up")


# Successful login page
@pages.get("/protected")
def protected():
    return render_template("protected.html", title="PasswordApp - Success")


# Account details page
@pages.route("/account", methods=["GET", "POST"])
def account():
    _id = request.args.get("user_id")
    user = User.from_mongo_email(session['email'])

    if _id == None:
        _id = user._id

    if request.method == "POST":
        username = request.form.get("username")
        password__add = request.form.get("password__add")
        url = request.form.get("url")

        formatted_account = {
            "user_id": user._id,
            "username": username,
            "password__add": password__add,
            "url": url
        }
        
        current_app.db.PasswordsSaved.insert_one(formatted_account)
        
        flash("Successfully added account!")
        return redirect(url_for('pages.account', user_id=_id))
       
    passwords = current_app.db.PasswordsSaved.find({"user_id": int(_id)})

    return request.url, render_template("account.html", 
                            email=session.get("email"), 
                            title="PasswordApp - Account Home",
                            passwords=passwords,
                        )
                            

# Simple log out
@pages.route("/logout")
def logout():
    session.clear()
    return render_template("index.html", title="PasswordApp - Home")