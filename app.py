import os
from flask import Flask, redirect, render_template, request
from cs50 import SQL
from datetime import datetime

# Create a Flask instance
app = Flask (__name__)

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

@app.route('/new_exhibition', methods=["GET", "POST"])

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