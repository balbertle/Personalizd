import os
import sqlite3

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import getmovieposter, get_trending_movie_ids, get_movie_details, get_movie_id_by_name, get_movie_backdrop


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///personalizd.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

connection = sqlite3.connect("personalizd.db", check_same_thread=False)

crsr = connection.cursor()

def generate_html_page(poster_path):
    base_url = "https://image.tmdb.org/t/p/original"
    poster_url = base_url + poster_path
    return poster_url

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("apology.html")

        if not password:
            return render_template("apology.html")

        # Ensure username exists and password is correct

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return render_template("apology.html")
        hash = generate_password_hash(password);

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html")
    
@app.route("/")
def index():
    poster_links=[]
    movie_ids = get_trending_movie_ids()
    for i in range(8):
        poster = getmovieposter(movie_ids[i])
        poster_links.append(poster)
    if "user_id" not in session:
        return render_template("index.html", poster_url1 = poster_links[0], poster_url2 = poster_links[1], poster_url3 = poster_links[2], poster_url4 = poster_links[3], poster_url5 = poster_links[4], poster_url6 = poster_links[5], poster_url7 = poster_links[6], poster_url8 = poster_links[7])
    user_id = session["user_id"]
    return render_template("layout.html") 

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/movies", methods=["GET", "POST"])
def movies():
    if request.method== "GET":
        return render_template("movies.html") 
    if request.method== "POST":
        return render_template("movies.html") 


@app.route('/movie/<movie_name>', methods=["GET", "POST"])
def movie_page(movie_name):
    if request.method == "GET":
        movie_id = get_movie_id_by_name(movie_name)
        if movie_id:
            movie_details = get_movie_details(movie_id)
            backdrop = get_movie_backdrop(movie_id)
            return render_template('movie.html', movie_details=movie_details, backdrop = backdrop)
        else:
            return render_template('error_page.html')
    if request.method == "POST":
        selected_rating = request.form.get('rating')
    
        if selected_rating:
            # Connect to the movie ratings database and insert the rating
            conn = sqlite3.connect('ratings.db')
            cursor = conn.cursor()

            movie_id = 123  # Replace with the actual movie ID
            user_id = 456   # Replace with the actual user ID

            cursor.execute('''
                INSERT INTO movie_ratings (movie_id, user_id, rating)
                VALUES (?, ?, ?)
            ''', (movie_id, user_id, selected_rating))

            conn.commit()
            conn.close()

            return f"Thank you for rating the movie with {selected_rating} stars!"
        else:
            return "Please select a rating before submitting."
if __name__ == '__main__':
    app.run(debug=True)