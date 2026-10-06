import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from bs4 import BeautifulSoup
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from urllib.parse import quote_plus
import jeya, sarasavi,jeya, mdgunasena,json
from helpers import apology
app = Flask(__name__)

db = SQL("sqlite:///book.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST","GET"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        sort = request.form.get("sort")
        books = (jeya.scrape_jeya(query) + sarasavi.scrape_sarasavi(query) + mdgunasena.scrape_md(query))
        query = query.lower()
        
        if sort == "low":
            books.sort(key=lambda x: x["price"])
        if sort == "high":
            books.sort(key=lambda x:x["price"],reverse=True)
        return render_template("search.html",books=books,query=query)  
    else:
        return redirect("/")
  
@app.route("/wishlist", methods=["GET","POST"])
def wishlist():
    if request.method == "POST":
        data = request.get_json()
        title = data.get("title")
        store = data.get("store")
        price = data.get("price")
        image = data.get("img")

        if title and store and price and image:
            db.execute("INSERT INTO wishlist (user_id,book,store,price,image) VALUES (?,?,?,?,?)",session["user_id"],title,store,price,image)
        items = db.execute("SELECT * FROM wishlist WHERE user_id = ?",session["user_id"])
        return jsonify(success=True)
    else:
        items = db.execute("SELECT * FROM wishlist WHERE user_id = ?",session["user_id"])
        return render_template("wishlist.html",items=items)
        
@app.route("/wishlist-rm", methods=["POST"])
def wishlist_rm():
    if request.method == "POST":
        data = request.get_json()
        wishlist_id = data.get("wishlist_id")
        db.execute("DELETE FROM wishlist WHERE wishlist_id = ?", wishlist_id)
        return jsonify(success=True)

      
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if not username:
            return apology("No username entered",403)
        if not password:
            return apology("No password entered",403)
        if not confirm_password:
            return apology("Password not confirmed",403)
        if password != confirm_password:
            return apology("Passwords do not match",403)
        usernames = db.execute("SELECT * FROM users WHERE username =?",username)
        if usernames:
            return apology("username taken",403)
        
        db.execute("INSERT INTO users (username,hash) VALUES(?,?)",username,generate_password_hash(password))
        return render_template("login.html")


        
    else:
        return render_template("register.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"],password):
            return apology("invalid username and/or password",403)
        session["user_id"] = rows[0]["id"]
        return render_template("index.html")
    else:
        return render_template("login.html")
        
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")

    
    

