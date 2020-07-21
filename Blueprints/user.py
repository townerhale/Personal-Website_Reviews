import time

import flask
from flask import redirect, request, flash, session, url_for, Blueprint

from Blueprints.database_connection import sql_load
from Blueprints.password_hashing import check_encrypted_password, pwd_context
from Blueprints.functions import sql_get_user_by_email, is_human

add_review = Blueprint('add_review', __name__)
user_password = Blueprint('user_password', __name__)
user_add_comment = Blueprint('user_add_comment', __name__)

def CheckPasswordRules( password ):
    return len( password ) >= 8 and any( character.isdigit() for character in password ) and any( character.islower() for character in password ) and any( character.isupper() for character in password )

@add_review.route("/SQL_AddReview", methods=["POST"])
def sql_add_review():
    connection = sql_load()

    title = request.form['inputTitle']
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    rating = request.form['inputRating']
    email = request.form['inputAuthorEmail']
    text = request.form['inputText']
    captcha_response = request.form['g-recaptcha-response']

    if is_human(captcha_response):
        author = sql_get_user_by_email(connection, email)

        cur = connection.cursor()

        cur.execute("INSERT INTO reviews (reviewtitle, reviewdate, reviewrating, reviewauthor, reviewtext) "
                    "VALUES(?, ?, ?, ?, ?)", (title, date, rating, author, text))
        connection.commit()
        flask.session.modified = True
        flash("Post created!", 'success')
        return redirect(url_for("index"))
    else:
        flash('Sorry, bots are not allowed!', 'error')
        return redirect(url_for("index"))


@user_password.route("/SQL_UserPassword", methods=["POST"])
def sql_user_password():
    if not session['logged_in']:
        flash('You are not logged in!', 'error')
        return redirect(url_for("index"))

    connection = sql_load()
    cur = connection.cursor()

    current_password = request.form['CurrentPassword']
    new_password = request.form['NewPassword']
    email = session['sessionEmail']
    encrypt = pwd_context.encrypt(new_password)
    captcha_response = request.form['g-recaptcha-response']

    if not CheckPasswordRules( new_password ):
        flash("Your password did not meet the validation rules!", 'error')
        return redirect(url_for("account"))

    if is_human(captcha_response):
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        data = cur.fetchone()[4]
        flask.session.modified = True
        if check_encrypted_password(current_password, data):
            cur.execute("UPDATE users SET password = ? WHERE email = ?", (encrypt, email))
            connection.commit()

            flash("Password updated!", 'success')
            return redirect(url_for("account"))

        flash("Failed!", 'error')
        return redirect(url_for("account"))
    else:
        flash('Sorry, bots are not allowed!', 'error')
        return redirect(url_for("account"))


@user_add_comment.route("/SQL_AddComment", methods=["POST"])
def sql_add_comment():
    connection = sql_load()

    reviewid = request.form['commentReviewID']
    email = request.form['commentEmail']
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    comment = request.form['comment']

    userid = sql_get_user_by_email(connection, email)

    cur = connection.cursor()

    cur.execute("INSERT INTO comments (commentreviewid, commentuserid, commentdate, comment) "
                "VALUES(?, ?, ?, ?)", (reviewid, userid, date, comment))
    connection.commit()

    flash("Comment added!", 'success')
    return redirect(url_for("index"))


@user_password.route("/SQL_UpdateBio", methods=["POST"])
def sql_update_bio():
    if not session['logged_in']:
        flash('You are not logged in!', 'error')
        return redirect(url_for("index"))

    captcha_response = request.form['g-recaptcha-response']

    if is_human(captcha_response):

        connection = sql_load()
        cur = connection.cursor()

        email = request.form['Email']
        bio = request.form['Bio']

        user_id = sql_get_user_by_email(connection, email)

        cur.execute("UPDATE users SET bio = ? WHERE userid = ?", (bio, user_id))
        connection.commit()

        flask.session.modified = True

        flash("Bio updated!", 'success')
        return redirect(url_for("index"))
    else:
        status = "Sorry ! Bots are not allowed."
        flash(status)
        return redirect(url_for("account"))
