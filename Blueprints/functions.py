import json
import requests

from Blueprints.database_connection import sql_load


def sql_get_email_by_id(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE userid = " + str(id))

    result = cur.fetchall()

    if not result:
        return "Removed User"

    return str(result[0][0])


def sql_get_comments(reviewid):
    connection = sql_load()
    cur = connection.cursor()

    cur.execute("SELECT commentuserid, commentdate, comment FROM comments WHERE commentreviewid = " + str(reviewid))

    rows = list(cur)
    list_of_lists = [list(elem) for elem in rows]

    for row in list_of_lists:
        author_id = row[0]
        author_name = sql_get_user_by_id(connection, author_id)

        row[0] = author_name

    return list_of_lists


# returns all of the reviews for the main page
def sql_threads(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews")

    rows = list(cur)
    list_of_lists = [list(elem) for elem in rows]

    for row in list_of_lists:
        author_id = row[4]
        author_name = sql_get_user_by_id(conn, author_id)

        row[4] = author_name
        row[6] = sql_get_comments(row[0])

    return list_of_lists


def sql_get_user_by_id(conn, id):
    if isinstance(id, str):
        return id

    cur = conn.cursor()
    cur.execute("SELECT firstname FROM users WHERE userid = " + str(id))

    result = cur.fetchall()

    if not result:
        return "Removed User"

    return str(result[0][0])


def sql_get_user_by_email(conn, email):
    cur = conn.cursor()
    cur.execute("SELECT userid FROM users WHERE email = ?", (email,))

    result = cur.fetchall()

    return str(result[0][0])


def sql_is_admin(email):
    connection = sql_load()
    cur = connection.cursor()

    id = sql_get_user_by_email(connection, email)

    cur.execute("SELECT adminid FROM admins WHERE adminid = ?", (id))
    result = cur.fetchall()

    if not result:
        return False

    else:
        return True


def sql_check_email(conn, email):
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE email = ?", (email,))

    result = cur.fetchall()

    if not result:
        return False

    else:
        return True


# Validating recaptcha response from google server
# Returns True captcha test passed for submitted form else returns False.
def is_human(captcha_response):

    secret = "6Lcz8XwUAAAAAAF1iTBeKHraFNEUz_AgA6YR-7yX"
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']


def sql_get_public_user_data(userid):
    connection = sql_load()
    cur = connection.cursor()

    cur.execute("SELECT firstname, lastname, bio FROM users WHERE userid = " + str(userid))
    result = cur.fetchall()

    return result


def sql_get_review_author(reviewid):
    connection = sql_load()
    cur = connection.cursor()

    cur.execute("SELECT reviewauthor FROM reviews WHERE reviewid = " + str(reviewid))
    result = cur.fetchall()

    return result[0][0]