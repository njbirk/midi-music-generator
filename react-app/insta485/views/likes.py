"""
Insta485 index (main) view.

URLs include:
/likes/
"""
import flask
from flask import abort
import insta485
from insta485.views.helpers import setup_log_url


@insta485.app.route('/likes/', methods=['POST'])
def likes():
    """Post /likes/ route."""
    setup = setup_log_url()
    if setup[0] == "":
        return flask.redirect(flask.url_for('show_login'))
    # Connect to database
    connection = insta485.model.get_db()
    logname, url = setup

    cur = connection.execute(
        "SELECT COUNT(owner) FROM likes WHERE (owner = ? AND postid = ?)",
        (logname, flask.request.form['postid'])
    )
    cur = cur.fetchall()
    liked = False
    if cur[0]['COUNT(owner)'] == 1:
        liked = True
    # do we have to check if the post exists..?
    # check whether post is liked or unliked
    if 'unlike' in flask.request.form['operation']:
        # check if post is already unliked
        if liked is False:
            print("you already unliked it")
            abort(409)
        connection.execute(
            "DELETE FROM likes WHERE owner = ? AND postid = ?",
            (logname, flask.request.form['postid'])
        )
        print("remove a like")
    elif 'like' in flask.request.form['operation']:
        # check if post is already liked
        if liked is True:
            print("you already liked it")
            abort(409)
        connection.execute(
            "INSERT INTO likes (owner, postid, created) "
            "VALUES (?, ?, CURRENT_TIMESTAMP)",
            (logname, flask.request.form['postid'])
        )
        print("added a like")

    return flask.redirect(url)
