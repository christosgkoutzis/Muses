import os
import sys
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from datetime import datetime
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

# Create a Flask instance
app = Flask (__name__)

# Enabling debug mode for live changes while developing
app.debug = True

# Add Exhibitions Database
db = SQL("sqlite:///exhibitions.db")

# Create a route decorator
@app.route('/')

def index():
  return render_template('index.html')

# Create error pages
@app.errorhandler(404)

def page_not_found(e):
  return render_template('404.html'), 404

@app.errorhandler(500)

def page_not_found(e):
  return render_template('500.html'), 500

# Helpers function that demands login in admin page
def login_required(f):
  @wraps(f)

  def decorated_function(*args, **kwargs):
    if session.get("admin_id") is None:
        return redirect("/admin")
    return f(*args, **kwargs)
  return decorated_function

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/new_exhibition', methods=["GET", "POST"])
@login_required
# Adds a new exhibition to the website through a form
def new_exhibition():
  if request.method == "POST":
    title = request.form.get("title")
    featured_image = request.form.get("featured_image")
    description = request.form.get("description")
    exhibition_date = request.form.get("exhibition_date")
    slug = request.form.get("slug")
    db.execute("INSERT INTO exhibitions (title, featured_image, description, exhibition_date, slug) VALUES (?, ?, ?, ?, ?)", title, featured_image, description, exhibition_date, slug)
    return redirect("/")
  else:
    return render_template("new_exhibition.html")

@app.route("/admin", methods=["GET", "POST"])
def login():
    # Forget any id
    session.clear()

    # Admin reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template('500.html'), 500

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('500.html'), 500

        # Query database for admin's username
        rows = db.execute(
            "SELECT * FROM admin_credentials WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return render_template('500.html'), 500

        # Remember which user has logged in
        session["admin_id"] = rows[0]["id"]

        # Redirect admin to new exhibitions form
        return redirect("/new_exhibition")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("admin.html")


@app.route("/logout")
def logout():
    
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Generates a hash of the inputed password
        password = request.form.get("password")
        hash_password = generate_password_hash(password)

        # Adds a new row in users table of the database
        db.execute(
            "INSERT INTO admin_credentials (username, password) VALUES (?, ?)",
            request.form.get("username"),
            hash_password,
        )

        # Remember which user has logged in
        session_dict = db.execute(
            "SELECT * FROM admin_credentials WHERE username = ?", request.form.get("username")
        )
        session["admin_id"] = session_dict[0]["id"]

        # Redirect user to home page
        return redirect("/admin")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
