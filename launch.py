from datetime import timedelta

import flask
from flask import Flask, render_template, redirect, flash, session, url_for, request
from flask_wtf.csrf import CSRFProtect

from Blueprints.admin import delete_review, delete_user_id, delete_admin, delete_user, add_admin, get_admins, \
    get_users, trump_review
from Blueprints.database_connection import sql_load
from Blueprints.functions import sql_threads, sql_get_public_user_data, sql_get_review_author
from Blueprints.login import login_page, review_votes, decrease_votes, increment_votes
from Blueprints.register import register_page
from Blueprints.search import search_funct
from Blueprints.user import add_review, user_password, user_add_comment

app = Flask(__name__)
app.register_blueprint(search_funct)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(delete_user)
app.register_blueprint(delete_admin)
app.register_blueprint(delete_user_id)
app.register_blueprint(delete_review)
app.register_blueprint(add_admin)
app.register_blueprint(get_users)
app.register_blueprint(get_admins)
app.register_blueprint(trump_review)
app.register_blueprint(add_review)
app.register_blueprint(user_password)
app.register_blueprint(review_votes)
app.register_blueprint(decrease_votes)
app.register_blueprint(increment_votes)
app.register_blueprint(user_add_comment)

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

CSRFProtect(app)
app.secret_key = "super secret key"
SESSION_COOKIE_SECURE = True


@app.route('/index')
@app.route("/")
def index():
    connection = sql_load()
    load_reviews = sql_threads(connection)
    flask.session.modified = True

    return render_template("index.html", reviews=load_reviews)


@app.route('/register')
def register():
    flask.session.modified = True
    return render_template("register.html")


@app.route('/post')
def post():
    flask.session.modified = True
    return render_template("post.html")


@app.route("/logout/")
def logout():
    flask.session.modified = True
    if 'logged_in' in session:
        session.clear()
        flash("You have been logged out!", 'success')
        return redirect(url_for('index'))
    else:
        flash("You need to login first", 'error')
        return redirect(url_for('login'))


@app.route('/admin')
def admin():
    flask.session.modified = True
    sql_load()

    return render_template("admin.html")


@app.route('/user', methods=["POST"])
def user():
    flask.session.modified = True

    user_review_id = request.form['UserReviewID']
    user_id = sql_get_review_author(user_review_id)

    data = sql_get_public_user_data(user_id)

    return render_template("user.html", data=data)


@app.route('/account')
def account():
    flask.session.modified = True
    return render_template("account.html")


if __name__ == "__main__":
    app.debug = True
    app.run(ssl_context=('cert.pem', 'key.pem'))
