import random
import time

import flask
import requests
from flask import redirect, request, flash, session, url_for, Blueprint

from Blueprints.database_connection import sql_load
from Blueprints.functions import sql_is_admin, sql_check_email, sql_get_user_by_email, sql_get_email_by_id, is_human

delete_user = Blueprint('delete_user', __name__)
delete_user_id = Blueprint('delete_user_id', __name__)
add_admin = Blueprint('add_admin', __name__)
delete_admin = Blueprint('delete_admin', __name__)
get_users = Blueprint('get_users', __name__)
get_admins = Blueprint('get_admins', __name__)
delete_review = Blueprint('delete_review', __name__)
trump_review = Blueprint('trump_review', __name__)


@delete_user.route("/SQL_DeleteUser", methods=["POST"])
def sql_delete_user():
    if not session['logged_in']:
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    if not sql_is_admin(session['sessionEmail']):
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    connection = sql_load()

    email = request.form['inputEmailDelete']
    captcha_response = request.form['g-recaptcha-response']

    if session['sessionEmail'] == email:
        flash('You can not delete an account you are currently logged in with!', 'error')
        return redirect(url_for("index"))

    if is_human(captcha_response):

        cur = connection.cursor()

        if sql_check_email(connection, email) == False:
            flash("Invalid email!", 'error')
            return redirect(url_for("index"))

        cur.execute("DELETE FROM users WHERE email = ?", (email,))
        connection.commit()
        flask.session.modified = True
        flash("Deleted user " + email + "!", 'success')
        return redirect(url_for("admin"))
    else:
        status = "Sorry ! Bots are not allowed."
        flash(status)
        return redirect(url_for("admin"))


@delete_user_id.route("/SQL_DeleteUserByID", methods=["POST"])
def sql_delete_user_by_id():
    if not session['logged_in']:
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    if not sql_is_admin(session['sessionEmail']):
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    captcha_response = request.form['g-recaptcha-response']

    if is_human(captcha_response):
        connection = sql_load()

        id = request.form['inputIDDelete']

        if session['sessionEmail'] == sql_get_email_by_id( connection,id ):
            flash('You can not delete an account you are currently logged in with!', 'error')
            return redirect(url_for("index"))

        cur = connection.cursor()

        cur.execute("DELETE FROM users WHERE userid = ?", (id,))
        connection.commit()
        flask.session.modified = True
        flash("Deleted user id " + id + "!", 'success')
        return redirect(url_for("admin"))
    else:
        status = "Sorry ! Bots are not allowed."
        flash(status)
        return redirect(url_for("admin"))


@add_admin.route("/SQL_AddAdmin", methods=["POST"])
def sql_add_admin():
    if not session['logged_in']:
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    if not sql_is_admin(session['sessionEmail']):
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    captcha_response = request.form['g-recaptcha-response']

    if is_human(captcha_response):

        connection = sql_load()

        email = request.form['inputEmailAdmin']

        cur = connection.cursor()

        if sql_check_email(connection, email) == False:
            flash("Invalid email!", 'error')
            return redirect(url_for("index"))

        id = sql_get_user_by_email(connection, email)

        cur.execute("INSERT INTO admins (adminid) VALUES(?)", id)
        connection.commit()
        flask.session.modified = True
        flash("User " + email + " is now an admin!", 'success')
        return redirect(url_for("admin"))

    else:
        status = "Sorry ! Bots are not allowed."
        flash(status)
        return redirect(url_for("admin"))


@delete_admin.route("/SQL_DeleteAdminByID", methods=["POST"])
def sql_delete_admin_by_id():
    if not session['logged_in']:
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    if not sql_is_admin(session['sessionEmail']):
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    captcha_response = request.form['g-recaptcha-response']

    if is_human(captcha_response):

        connection = sql_load()

        id = request.form['inputIDDeleteAdmin']

        cur = connection.cursor()

        cur.execute("DELETE FROM admins WHERE adminid = ?", (id,))
        connection.commit()
        flask.session.modified = True
        flash("Deleted admin id " + id + "!", 'success')
        return redirect(url_for("admin"))
    else:
        status = "Sorry ! Bots are not allowed."
        flash(status)
        return redirect(url_for("admin"))


@get_users.route("/SQL_GetUsers", methods=["POST"])
def sql_get_users():
    if not session['logged_in']:
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    if not sql_is_admin(session['sessionEmail']):
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    connection = sql_load()
    cur = connection.cursor()

    cur.execute("SELECT userid, email FROM users")
    rows = cur.fetchall()
    flask.session.modified = True
    for row in rows:
        flash('ID: ' + str(row[0]) + ' | Email: ' + ' ' + str(row[1]), 'success')

    return redirect(url_for("admin"))


@get_admins.route("/SQL_GetAdmins", methods=["POST"])
def sql_get_admins():
    if not session['logged_in']:
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    if not sql_is_admin(session['sessionEmail']):
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    connection = sql_load()
    cur = connection.cursor()

    cur.execute("SELECT adminid FROM admins")
    rows = cur.fetchall()
    flask.session.modified = True
    for row in rows:
        email = sql_get_email_by_id(connection, row[0])
        flash('ID: ' + str(row[0]) + ' | Email: ' + ' ' + email, 'success')

    return redirect(url_for("admin"))


@delete_review.route("/SQL_DeleteReview", methods=["POST"])
def sql_delete_review():
    if not session['logged_in']:
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    if not sql_is_admin(session['sessionEmail']):
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    captcha_response = request.form['g-recaptcha-response']

    if is_human(captcha_response):

        connection = sql_load()

        reviewid = request.form['reviewID']

        cur = connection.cursor()

        cur.execute("DELETE FROM reviews WHERE reviewid = ?", (reviewid,))
        connection.commit()
        flask.session.modified = True
        flash("Deleted review with ID of " + reviewid + "!", 'success')
        return redirect(url_for("index"))
    else:
        status = "Sorry ! Bots are not allowed."
        flash(status)
        return redirect(url_for("index"))


@trump_review.route("/SQL_TrumpReview", methods=["POST"])
def sql_trump_review():
    if not session['logged_in']:
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    if not sql_is_admin(session['sessionEmail']):
        flash('You are not an admin!', 'error')
        return redirect(url_for("index"))

    quotes = requests.get('https://api.whatdoestrumpthink.com/api/v1/quotes/random')
    quotes.json()

    trump = quotes.json()['message']
    connection = sql_load()

    title = 'Donald Trump'
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    rating = random.randint(1, 5)
    text = trump
    author = sql_get_user_by_email(connection, session['sessionEmail'])

    cur = connection.cursor()

    cur.execute("INSERT INTO reviews (reviewtitle, reviewdate, reviewrating, reviewauthor, reviewtext) "
                "VALUES(?, ?, ?, ?, ?)", (title, date, rating, author, text))
    connection.commit()
    flask.session.modified = True
    flash("Added Trump review!", 'success')
    return redirect(url_for("admin"))
