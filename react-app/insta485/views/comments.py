"""
Insta485 index (main) view.

URLs include:
/comments/
"""
import flask
import insta485
from insta485.views.helpers import setup_log_url


@insta485.app.route('/comments/', methods=['POST'])
def comments():
    """Post /comments route."""
    setup = setup_log_url()
    if setup[0] == "":
        return flask.redirect(flask.url_for('show_login'))
    logname, url = setup
    connection = insta485.model.get_db()

    if 'delete' in flask.request.form['operation']:
        cur = connection.execute(
            "SELECT owner FROM comments WHERE commentid = ?",
            (flask.request.form['commentid'],)
        )
        cur = cur.fetchall()
        print(cur)
        if cur[0]['owner'] != logname:
            flask.abort(403)

        cur = connection.execute(
            "DELETE FROM comments WHERE owner = ? AND commentid = ?",
            (logname, flask.request.form['commentid'])
        )
    elif 'create' in flask.request.form['operation']:
        if flask.request.form['text'] == "":
            flask.abort(400)
        cur = connection.execute(
            "INSERT INTO comments (owner, postid, text, created) "
            "VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            (logname, flask.request.form['postid'], flask.request.form['text'])
        )

    return flask.redirect(url)
