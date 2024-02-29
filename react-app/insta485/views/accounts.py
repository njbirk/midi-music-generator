"""
Insta485 index (main) view.

URLs include:
/accounts/login
/accounts/logout/
/accounts/create/
/accounts/delete/
/accounts/edit/
/accounts/password/
/accounts/auth/
/accounts/
"""
import flask
from flask import abort, request
import insta485
from insta485.views.helpers import (is_user_logged_in, compute_password,
                                    add_image, delete_photo)


@insta485.app.route('/accounts/login/')
def show_login():
    """Display /accounts/login/ route."""
    if "username" in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    return flask.render_template("login.html")


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout():
    """Post /accounts/logout/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    flask.session.clear()
    return flask.redirect(flask.url_for('show_login'))


@insta485.app.route('/accounts/create/')
def show_create():
    """Display /accounts/create/ route."""
    if "username" in flask.session:
        return flask.redirect(flask.url_for('show_edit'))
    return flask.render_template("create.html")


@insta485.app.route('/accounts/delete/')
def show_delete():
    """Display /accounts/delete/ route."""
    if "username" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))
    context = {"logname": flask.session["username"]}
    return flask.render_template("delete.html", **context)


@insta485.app.route('/accounts/edit/')
def show_edit():
    """Display /accounts/edit/ route."""
    if "username" not in flask.session:
        return flask.redirect(flask.url_for('show_login'))

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    logname = flask.session['username']
    cur = connection.execute(
        "SELECT username, fullname, email, filename "
        "FROM users WHERE username = ?",
        (logname, )
    )
    cur = cur.fetchall()
    cur = cur[0]

    return flask.render_template("edit.html", **cur)


@insta485.app.route('/accounts/password/')
def show_password():
    """Display /accounts/password/ route."""
    if not is_user_logged_in():
        return flask.redirect(flask.url_for('show_login'))
    context = {"logname": flask.session["username"]}
    return flask.render_template("password.html", **context)


@insta485.app.route('/accounts/auth/')
def auth():
    """Display account auth."""
    if 'username' not in flask.session:
        flask.abort(403)
    return ('', 200)


def account_login():
    """Help login account."""
    username = flask.request.form["username"]
    password = flask.request.form["password"]

    if not username or not password:
        # print("emptyy")
        flask.abort(400)

    connection = insta485.model.get_db()
    # Get salt of password associated with username
    cur = connection.execute(
        "SELECT password FROM users WHERE username = ?",
        (flask.request.form["username"],)
    )
    cur = cur.fetchall()
    if cur == []:
        abort(403)
    password = cur[0]['password'].split("$")
    password = compute_password(password[1],
                                flask.request.form['password'])

    # Check if user & pass match with database
    cur = connection.execute(
        "SELECT COUNT(1) FROM users WHERE username = ? AND password = ?",
        (flask.request.form['username'], password)
    )
    cur = cur.fetchall()
    if cur[0]['COUNT(1)'] == 0:
        abort(403)
    flask.session['username'] = flask.request.form['username']


def account_create():
    """Help create account."""
    # if any fields are empty, abort
    if not all(flask.request.form.values()):
        abort(400)
    # Check if username already exists in database
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT COUNT(1) FROM users WHERE username = ?",
        (flask.request.form['username'],)
    )
    cur = cur.fetchall()
    if cur[0]['COUNT(1)'] == 1:
        abort(409)
    password = compute_password("", flask.request.form['password'])
    uuid_basename = add_image(flask.request.files["file"])
    cur = connection.execute(
        "INSERT INTO "
        "users (username, fullname, email, filename, password, created) "
        "VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
        (flask.request.form['username'], flask.request.form['fullname'],
            flask.request.form['email'], uuid_basename, password)
    )
    flask.session['username'] = flask.request.form['username']


def account_delete():
    """Help delete account."""
    if not is_user_logged_in():
        abort(403)
    connection = insta485.model.get_db()
    logname = flask.session["username"]
    # delete all posts from filesystem
    # delete profile pic from filesystem
    cur = connection.execute(
        "SELECT filename FROM users WHERE username = ?",
        (logname, )
    )
    cur = cur.fetchall()
    delete_photo(cur[0]['filename'])
    cur = connection.execute(
        "SELECT filename FROM posts WHERE owner = ?",
        (logname, )
    )
    cur = cur.fetchall()
    for pic in cur:
        delete_photo(pic['filename'])

    # delete user
    cur = connection.execute(
        "DELETE FROM users WHERE username = ?",
        (logname, )
    )
    flask.session.clear()


def account_edit():
    """Help edit account."""
    requestform = flask.request.form
    if not is_user_logged_in():
        flask.abort(403)
    # if fullname or email empty, abort(400)
    if (not requestform['fullname'] or not requestform['email']):
        flask.abort(400)

    connection = insta485.model.get_db()
    # If no photo file is included, update only the user’s name and email.
    newphoto = flask.request.files
    if 'file' not in newphoto or not newphoto['file'].filename:
        cur = connection.execute(
            "UPDATE users SET fullname = ?, email = ? WHERE username = ?",
            (flask.request.form['fullname'], flask.request.form['email'],
                flask.session["username"])
        )
    else:
        # If photo file included, server update user's photo, name, email.
        # Delete the old photo from the filesystem.
        cur = connection.execute(
            "SELECT filename from users WHERE username = ?",
            (flask.session["username"],)
        )
        cur = cur.fetchall()
        delete_photo(cur[0]["filename"])
        uuid_basename = add_image(newphoto['file'])
        cur = connection.execute(
            "UPDATE users SET fullname = ?, email = ?, filename = ? "
            "WHERE username = ?",
            (flask.request.form['fullname'], flask.request.form['email'],
                uuid_basename, flask.session["username"])
        )


def account_updatepw():
    """Help account update password."""
    if not is_user_logged_in():
        flask.abort(403)

    # If any of the above fields are empty, abort(400).
    # fix this syntax
    if not (flask.request.form['password']
            or flask.request.form['new_password1']
            or flask.request.form['new_password2']):
        flask.abort(400)

    # Check if both passwords match
    newpassword = flask.request.form['new_password2']
    if flask.request.form['new_password1'] != newpassword:
        flask.abort(401)

    # Get salt of password associated with username
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password FROM users WHERE username = ?",
        (flask.session["username"],)
    )
    cur = cur.fetchall()
    password = cur[0]['password'].split("$")
    password = compute_password(password[1],
                                flask.request.form['password'])

    # Check if user & pass match with database
    cur = connection.execute(
        "SELECT COUNT(1) FROM users WHERE username = ? AND password = ?",
        (flask.session['username'], password)
    )
    cur = cur.fetchall()
    if cur[0]['COUNT(1)'] == 0:
        abort(403)

    # Compute new password and update to database
    password = compute_password("", newpassword)
    cur = connection.execute(
        "UPDATE users SET password = ? WHERE username = ?",
        (password, flask.session["username"])
    )


@insta485.app.route('/accounts/', methods=['POST'])
def account():
    """Post /accounts/ route."""
    url = request.args.get('target')
    if url is None:
        url = "/"

    if "login" in flask.request.form['operation']:
        account_login()
    elif "create" in flask.request.form['operation']:
        account_create()
    elif "delete" in flask.request.form['operation']:
        account_delete()
    elif "edit_account" in flask.request.form['operation']:
        account_edit()
    elif "update_password" in flask.request.form['operation']:
        account_updatepw()

    return flask.redirect(url)
