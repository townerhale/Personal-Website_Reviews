from flask import render_template, redirect, request, flash, session, url_for, Blueprint

from Blueprints.database_connection import sql_load
from Blueprints.password_hashing import pwd_context
from Blueprints.functions import is_human

register_page = Blueprint('register_page', __name__)


def CheckPasswordRules( password ):
    return len( password ) >= 8 and any( character.isdigit() for character in password ) and any( character.islower() for character in password ) and any( character.isupper() for character in password )

@register_page.route("/SQL_AddUser", methods=["POST"])
def sql_add_user():
    connection = sql_load()
    first = request.form['inputName']
    last = request.form['inputSurname']
    email = request.form['inputEmail']
    password_original = request.form['inputPassword']
    password = pwd_context.encrypt(password_original)
    captcha_response = request.form['g-recaptcha-response']

    if not CheckPasswordRules( password ):
        flash("Your password did not meet the validation rules!", 'error')
        return render_template("register.html")

    cur = connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))

    if is_human(captcha_response):
        if cur.fetchone() == None:
            cur.execute("INSERT INTO users (firstname, lastname, email, password) VALUES(?, ?, ?, ?)",
                        (first, last, email, password))
            connection.commit()
            session['logged_in'] = True
            session.permanent = True
            session['sessionEmail'] = email

            flash("Registration successful!", 'success')
            return redirect(url_for("index"))
        else:
            flash("Email address already in use!", 'error')
            return render_template("register.html")
    else:
        flash("Sorry, bots are not allowed!", 'error')
        return render_template("register.html")
