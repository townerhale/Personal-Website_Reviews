import flask
from flask import render_template, redirect, request, flash, url_for, Blueprint

from Blueprints.database_connection import sql_load
from Blueprints.functions import sql_get_user_by_id

search_funct = Blueprint('search_funct', __name__)


@search_funct.route("/search", methods=["GET", "POST"])
def search():
    connection = sql_load()
    cur = connection.cursor()
    term = request.form['inputSearch'].lower()  # holds what is entered in the search bar

    cur.execute("SELECT * FROM reviews")
    results = sql_search_threads(term, cur.fetchall())  # fetchall holds all reviews, term is what is sent in
    # the search bar
    flask.session.modified = True
    if not results or results == None:
        flash("No results", 'error')
        return redirect(url_for("index"))
    else:
        return render_template("search.html", reviews=results)


## searches reviews for the term entered in the search bar
def sql_search_threads(term, reviews):
    connection = sql_load()

    rows = list(reviews)  # holds all reviews
    list_of_lists = [list(elem) for elem in rows]

    relevant = []

    for row2 in list_of_lists:
        # print(str(row2))
        get_name = row2[4]
        get_rating = row2[3]

        author_name = sql_get_user_by_id(connection, get_name)

        if term in row2[5].lower():  # if search is found in row[5] that holds review text
            author_id = row2[4]

            # print("test: " + str(test))
            author_name = sql_get_user_by_id(connection, author_id)

            row2[4] = author_name

            relevant.append(row2)  # add to empty list newly modified row
        elif term in row2[1].lower():
            author_id = row2[4]

            author_name = sql_get_user_by_id(connection, author_id)

            row2[4] = author_name

            relevant.append(row2)  # add to empty list newly modified row
        elif term in str(author_name).lower():
            author_id = row2[4]

            author_name = sql_get_user_by_id(connection, author_id)

            row2[4] = author_name

            relevant.append(row2)  # add to empty list newly modified row
        elif term in str(get_rating):
            author_id = row2[4]

            author_name = sql_get_user_by_id(connection, author_id)

            row2[4] = author_name

            relevant.append(row2)  # add to empty list newly modified row

    return relevant
