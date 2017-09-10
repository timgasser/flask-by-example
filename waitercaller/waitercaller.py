from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

# Login imports
from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user

from mockdbhelper import MockDBHelper as DBHelper
from user import User
from passwordhelper import PasswordHelper

DB = DBHelper()
PH = PasswordHelper()

app = Flask(__name__)
app.secret_key = '06tTaJ6UfpN+GETf2FUWiV/HH4Hr/YJEHCziZkOlj9/1rPmPOcaFdelknO6Gu5L94ZUI4vOq/qKFyKzWzsn/T+kkjsZ6aAIm3xKx'
login_manager = LoginManager(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if password != password2:
        return redirect(url_for('home'))
    if DB.get_user(email):
        return redirect(url_for('home'))
    salt = PH.get_salt()
    hashed = PH.get_hash(password + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for('home'))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = DB.get_user(email)
    user_password = DB.get_user(email)
    if stored_user is not None and PH.validate_password(password, 
                                                        stored_user['salt'], 
                                                        stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return home()

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route("/account")
@login_required
def account():
    return "You are logged in"

if __name__ == '__main__':
    app.run(port=5000, debug=True)