"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485
from insta485.views.helpers import is_user_logged_in


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if not is_user_logged_in():
        return flask.redirect(flask.url_for('show_login'))
    logname = flask.session["username"]

    context = {"logname": logname}
    return flask.render_template("index.html", **context)
