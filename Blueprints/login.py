from flask import render_template, redirect, request, flash, session, url_for, Blueprint
import time
from Blueprints.database_connection import sql_load
from Blueprints.functions import sql_is_admin, sql_check_email, is_human
from Blueprints.password_hashing import check_encrypted_password

login_page = Blueprint('login_page', __name__)
review_votes = Blueprint('review_votes', __name__)
increment_votes = Blueprint('increment_votes', __name__)
decrease_votes = Blueprint('decrease_votes', __name__)
@login_page.route('/login', methods=["GET", "POST"])
def login():
    connection = sql_load()
    cur = connection.cursor()
    if request.method == "POST":
        email = request.form['inputEmail']
        captcha_response = request.form['g-recaptcha-response']

        if is_human(captcha_response):
            if sql_check_email(connection, email) == False:
                try:
                    check_encrypted_password(request.form['inputPassword'], "blah") #encrypt password so there's no time difference if username is wrong

                except:
                    flash("Invalid credentials!", 'error')
                    return redirect(url_for("index"))

            cur.execute("SELECT * FROM users WHERE email = ?", (email,))
            data = cur.fetchone()[4]
            if check_encrypted_password(request.form['inputPassword'], data):
                session['logged_in'] = True
                session.permanent = True
                session['sessionEmail'] = request.form['inputEmail']

                if sql_is_admin(session['sessionEmail']):
                    session['admin'] = True
                flash("You are now logged in!", 'success')
                return redirect(url_for("index"))

            else:
                session['login_failures'] =  session['login_failures']  + 1
                login_failures = session['login_failures']
                time.sleep(0.001 * 2 ** login_failures)
                flash("Invalid credentials!", 'error')
        else:
            flash('Sorry, bots are not allowed!', 'error')
            return render_template("login.html")

    return render_template("login.html")
