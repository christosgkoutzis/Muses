from flask import Flask, redirect, render_template, request, session, url_for
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

# Exhibitions archive route
@app.route('/exhibitions')
def exhibitions():
  archive = db.execute("SELECT * FROM exhibitions")
  return render_template("exhibitions.html", archive=archive)

# Single exhibition route
@app.route('/exhibitions/<int:id>')
def single(id):
   # Each query is declared as a variable for debugging reasons
   exhibition = db.execute("SELECT * FROM exhibitions WHERE id = ?", id)
   title = exhibition[0]["title"]
   description = exhibition[0]["description"]
   featured_image = exhibition[0]["featured_image"]
   exhibition_date = exhibition[0]["exhibition_date"]
   if len(exhibition) != 1:
      return render_template("404.html"), 404
   return render_template("exhibition.html",id=id, title=title, description=description, featured_image=featured_image, exhibition_date=exhibition_date)

# Route to edit exhibitions
@app.route('/exhibitions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
  exhibition = db.execute("SELECT * FROM exhibitions WHERE id = ?", id)
  if len(exhibition) != 1:
    return render_template("404.html"), 404
  if request.method == "POST":
    title = request.form.get("title")
    featured_image = request.form.get("featured_image")
    description = request.form.get("description")
    exhibition_date = request.form.get("exhibition_date")
    slug = request.form.get("slug")
    db.execute("UPDATE exhibitions SET title = ?, description = ?, featured_image = ?, exhibition_date = ?, slug = ? WHERE id = ?", title, description, featured_image, exhibition_date, slug, id)
    return redirect(url_for('single', id=id))
  else:
    title = exhibition[0]["title"]
    description = exhibition[0]["description"]
    featured_image = exhibition[0]["featured_image"]
    exhibition_date = exhibition[0]["exhibition_date"]
    slug = exhibition[0]["slug"]
    return render_template("edit.html", title=title, description=description, featured_image=featured_image, exhibition_date=exhibition_date, slug=slug, id=id)
   
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
      if not request.form.get("Username") or not request.form.get("Password"):
        return render_template('admin.html')
      # Query database for admin's username
      rows = db.execute(
          "SELECT * FROM admin_credentials WHERE username = ?", request.form.get("Username")
      )

      # Ensure username exists and password is correct
      if len(rows) != 1 or not check_password_hash(
          rows[0]["password"], request.form.get("Password")
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