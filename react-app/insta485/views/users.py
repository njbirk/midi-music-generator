"""
Insta485 index (main) view.

URLs include:
/users/<user_url_slug>/
"""
import flask
from flask import abort, request
import insta485
from insta485.views.helpers import user_logname


@insta485.app.route('/users/<user_url_slug>/')
def show_user(user_url_slug):
    """Display /users/<user_url_slug>/ route."""
    logname = user_logname()
    if logname == "":
        return flask.redirect(flask.url_for('show_login'))

    # Connect to database
    connection = insta485.model.get_db()

    # Check if user_url_slug exists
    cur = connection.execute(
        "SELECT COUNT(1) FROM users WHERE username = ?",
        (user_url_slug, )
    )
    cur = cur.fetchall()
    if cur[0]['COUNT(1)'] == 0:
        abort(404)

    # Query database
    context = {"logname": logname, "username": user_url_slug}

    # if logname_follows_username = true or false
    cur = connection.execute(
        "SELECT COUNT(1) FROM following WHERE username1 = ? AND username2 = ?",
        (logname, user_url_slug)
    )
    cur = cur.fetchall()
    if cur[0]['COUNT(1)'] == 1:
        print("logname follows user_url_slug")
        context['logname_follows_username'] = True
    else:
        print("logname doesn't follow user_url_slug")
        context['logname_follows_username'] = False

    # number of posts
    cur = connection.execute(
        "SELECT COUNT(*) FROM posts WHERE owner = ?",
        (user_url_slug, )
    )
    cur = cur.fetchall()
    context['total_posts'] = cur[0]["COUNT(*)"]

    # number of followers
    cur = connection.execute(
        "SELECT COUNT(*) FROM following WHERE username2 = ?",
        (user_url_slug, )
    )
    cur = cur.fetchall()
    context['followers'] = cur[0]["COUNT(*)"]

    # number following
    cur = connection.execute(
        "SELECT COUNT(*) FROM following WHERE username1 = ?",
        (user_url_slug, )
    )
    cur = cur.fetchall()
    context['following'] = cur[0]["COUNT(*)"]

    # fullname
    cur = connection.execute(
        "SELECT fullname FROM users WHERE username = ?",
        (user_url_slug, )
    )
    cur = cur.fetchall()
    context['fullname'] = cur[0]['fullname']

    # small image for each post
    cur = connection.execute(
        "SELECT filename, postid FROM posts WHERE owner = ? "
        "ORDER BY postid ASC",
        (user_url_slug, )
    )
    cur = cur.fetchall()
    context['posts'] = cur
    return flask.render_template("users.html", **context)


@insta485.app.route('/users/<user_url_slug>/followers/')
def show_followers(user_url_slug):
    """Display /users/<user_url_slug>/followers/ route."""
    logname = user_logname()
    if logname == "":
        return flask.redirect(flask.url_for('show_login'))

    # Connect to database
    connection = insta485.model.get_db()

    # Check if user_url_slug exists
    cur = connection.execute(
        "SELECT COUNT(1) FROM users WHERE username = ?",
        (user_url_slug, )
    )
    cur = cur.fetchall()
    if cur[0]['COUNT(1)'] == 0:
        abort(404)

    # Query database
    # Retrieve user's followers
    cur = connection.execute(
        "SELECT users.filename, users.username "
        "FROM users INNER JOIN following "
        "ON (users.username = username1 AND username2 = ?)",
        (user_url_slug, )
    )
    cur = cur.fetchall()

    # Retrieve relationship between logname and followers
    followerscontext = []
    for follower in cur:
        cur2 = connection.execute(
            "SELECT COUNT(1) FROM following "
            "WHERE username1 = ? AND username2 = ?",
            (logname, follower['username'])
        )
        cur2 = cur2.fetchall()
        print(cur2)
        if cur2[0]['COUNT(1)'] == 1:
            print("logname follows user")
            cur2 = {'logname_follows_user': True}
        else:
            print("logname doesn't follow user")
            cur2 = {'logname_follows_user': False}
        print(cur2)
        newfollower = follower | cur2
        followerscontext.append(newfollower)

    context = {"logname": logname, "username": user_url_slug,
               "followers": followerscontext}
    print(context)
    return flask.render_template("followers.html", **context)


@insta485.app.route('/users/<user_url_slug>/following/')
def show_following(user_url_slug):
    """Display /users/<user_url_slug>/following/ route."""
    logname = user_logname()
    if logname == "":
        return flask.redirect(flask.url_for('show_login'))

    # Connect to database
    connection = insta485.model.get_db()

    # Check if user_url_slug exists
    cur = connection.execute(
        "SELECT COUNT(1) FROM users WHERE username = ?",
        (user_url_slug, )
    )
    cur = cur.fetchall()
    if cur[0]['COUNT(1)'] == 0:
        abort(404)

    # Retrieve user's following
    cur = connection.execute(
        "SELECT users.filename, users.username "
        "FROM users INNER JOIN following "
        "ON (users.username = username2 AND username1 = ?)",
        (user_url_slug, )
    )
    cur = cur.fetchall()

    # Retrieve relationship between logname and following
    followingcontext = []
    for follow in cur:
        cur2 = connection.execute(
            "SELECT COUNT(1) FROM following "
            "WHERE username1 = ? AND username2 = ?",
            (logname, follow['username'])
        )
        cur2 = cur2.fetchall()
        print(cur2)
        if cur2[0]['COUNT(1)'] == 1:
            print("logname follows user")
            cur2 = {'logname_follows_user': True}
        else:
            print("logname doesn't follow user")
            cur2 = {'logname_follows_user': False}
        print(cur2)
        newfollowing = follow | cur2
        followingcontext.append(newfollowing)

    context = {"logname": logname, "username": user_url_slug,
               "following": followingcontext}
    print(context)
    return flask.render_template("following.html", **context)


@insta485.app.route('/following/', methods=['POST'])
def following():
    """Post /following/ route."""
    logname = user_logname()
    if logname == "":
        return flask.redirect(flask.url_for('show_login'))

    url = request.args.get('target')
    print(url)

    if url is None:
        url = "/"

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT COUNT(1) FROM following "
        "WHERE (username1 = ? AND username2 = ?)",
        (logname, flask.request.form['username'])
    )
    cur = cur.fetchall()
    followed = False
    print(cur)
    print(cur[0]['COUNT(1)'])
    if cur[0]['COUNT(1)'] == 1:
        followed = True

    if 'unfollow' in flask.request.form['operation']:
        if followed is False:
            print("you can't unfollow if u not followin")
            abort(409)
        cur = connection.execute(
            "DELETE FROM following WHERE username1 = ? AND username2 = ?",
            (logname, flask.request.form['username'])
        )
    elif 'follow' in flask.request.form['operation']:
        if followed:
            print("you can't refollow someone!")
            abort(409)
        cur = connection.execute(
            "INSERT INTO following (username1, username2, created) "
            "VALUES (?, ?, CURRENT_TIMESTAMP)",
            (logname, flask.request.form['username'])
        )

    return flask.redirect(url)
