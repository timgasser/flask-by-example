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
from flask.ext.login import current_user

import config

from mockdbhelper import MockDBHelper as DBHelper
from user import User
from passwordhelper import PasswordHelper
from bitlyhelper import BitlyHelper 

import datetime

DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()

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

@app.route("/dashboard")
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    for req in requests:
        deltaseconds = (now - req['time']).seconds
        req['wait_minutes'] = "{}.{}".format((deltaseconds/60),
                                             str(deltaseconds % 60).zfill(2))
    return render_template("dashboard.html", requests=requests)

@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)

@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    tablename = request.form.get("tablenumber")
    tableid = DB.add_table(tablename, current_user.get_id())
    new_url = config.base_url + "newrequest/" + tableid
    short_url = BH.shorten_url(new_url)
    DB.update_table(tableid, short_url)
    return redirect(url_for('account'))

@app.route("/account/deletetable")
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for("account"))

@app.route("/newrequest/<tid>")
def new_request(tid):
    DB.add_request(tid, datetime.datetime.now())
    return "Your request is logged and a waiter will be with you shortly"

@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
    request_id = request_args.get("request_id")
    DB.delete_request(request_id)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)