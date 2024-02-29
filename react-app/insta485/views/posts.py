"""
Insta485 index (main) view.

URLs include:
/posts/<postid_url_slug>/
/posts/
"""
import flask
from flask import request, abort, url_for
import arrow
import insta485
from insta485.views.helpers import user_logname, add_image, delete_photo


@insta485.app.route('/posts/<postid_url_slug>/')
def show_post(postid_url_slug):
    """Display /posts/<postid_url_slug>/ route."""
    logname = user_logname()
    if logname == "":
        return flask.redirect(flask.url_for('show_login'))
    context = {"logname": logname}

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT postid, filename AS img_url, owner, created "
        "FROM posts WHERE postid = ?",
        (postid_url_slug, )
    )
    cur = cur.fetchall()
    cur[0]['created'] = arrow.get(cur[0]['created'], 'YYYY-MM-DD HH:mm:ss')
    cur[0]['created'] = cur[0]['created'].humanize()

    # gets owner's profile pic
    cur2 = connection.execute(
        "SELECT filename AS owner_img_url FROM users WHERE username = ?",
        (cur[0]['owner'], )
    )
    cur2 = cur2.fetchall()

    # gets whether image liked or not by logname
    cur3 = connection.execute(
        "SELECT COUNT(1) FROM likes WHERE owner = ? AND postid = ?",
        (logname, postid_url_slug)
    )
    cur3 = cur3.fetchall()
    if cur3[0]['COUNT(1)'] == 1:
        cur3 = {'liked': True}
    else:
        cur3 = {'liked': False}

    # gets comments
    cur4 = connection.execute(
        "SELECT owner, text, commentid FROM comments "
        "WHERE postid = ? ORDER BY commentid ASC",
        (postid_url_slug, )
    )
    cur4 = cur4.fetchall()
    cur4 = {'comments': cur4}

    # gets num likes
    cur5 = connection.execute(
            "SELECT COUNT(*) FROM likes WHERE postid = ?",
            (postid_url_slug, )
        )
    cur5 = cur5.fetchall()
    cur5 = {'likes': cur5[0]['COUNT(*)']}

    context = context | cur[0] | cur2[0] | cur3 | cur4 | cur5
    return flask.render_template("posts.html", **context)


@insta485.app.route('/posts/', methods=['POST'])
def post():
    """Post /posts/ route."""
    logname = user_logname()
    if logname == "":
        return flask.redirect(flask.url_for('show_login'))

    url = request.args.get('target')
    if url is None:
        url = url_for('show_user', user_url_slug=logname)

    connection = insta485.model.get_db()

    if "create" in flask.request.form['operation']:
        print("creating a file")
        # User tried posting empty file
        if flask.request.files["file"] is None:
            print("user tried posting empty file")
            abort(400)

        uuid_basename = add_image(flask.request.files["file"])
        cur = connection.execute(
            "INSERT INTO posts (filename, owner, created) "
            "VALUES (?, ?, CURRENT_TIMESTAMP)",
            (uuid_basename, logname)
        )
    elif "delete" in flask.request.form['operation']:
        cur = connection.execute(
            "SELECT COUNT(1) FROM posts WHERE postid = ? AND owner = ?",
            (flask.request.form['postid'], logname)
        )
        cur = cur.fetchall()
        if cur[0]['COUNT(1)'] == 0:
            abort(403)

        # Delete photo from filesystem
        photo = connection.execute(
            "SELECT filename FROM posts WHERE postid = ? AND owner = ?",
            (flask.request.form['postid'], logname)
        )
        photo = photo.fetchall()
        delete_photo(photo[0]['filename'])

        cur = connection.execute(
            "DELETE FROM posts WHERE postid = ?",
            (flask.request.form['postid'],)
        )
    return flask.redirect(url)
