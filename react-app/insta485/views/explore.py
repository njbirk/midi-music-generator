"""
Insta485 index (main) view.

URLs include:
/explore/
"""
import flask
import insta485
from insta485.views.helpers import setup_log_url


@insta485.app.route('/explore/')
def show_explore():
    """Display /explore/ route."""
    setup = setup_log_url()
    if setup[0] == "":
        return flask.redirect(flask.url_for('show_login'))
    logname = setup[0]

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    cur = connection.execute(
        "SELECT username FROM users WHERE username != ? "
        "EXCEPT SELECT username2 FROM following WHERE username1 = ?",
        (logname, logname)
    )
    not_following = cur.fetchall()
    print(not_following)
    users = ""
    for user in not_following:
        if users != "":
            users += ", "
        print(user)
        users += "\'"
        users += user['username']
        users += "\'"
    print(users)

    cur2 = connection.execute(
        f"SELECT username, filename FROM users WHERE username IN ({users})",
    )
    cur2 = cur2.fetchall()
    not_following = cur2

    context = {"not_following": not_following, "logname": logname}
    # {'not_following': [{'username': 'jag'}]}
    print(context)
    return flask.render_template("explore.html", **context)
