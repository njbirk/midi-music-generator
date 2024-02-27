"""
Insta485 helper function view.

URLs include:
/uploads/<path:name>
"""
import uuid
import hashlib
import pathlib
import flask
from flask import send_from_directory, abort, request, url_for
import insta485


def is_user_logged_in():
    """Check if logged user in."""
    if "username" not in flask.session:
        return False
    return True


def user_logname():
    """Check if logged and return logname."""
    if "username" not in flask.session:
        return ""
    return flask.session["username"]


def setup_log_url():
    """Set up logname, connection, url."""
    logname = user_logname()

    url = request.args.get('target')
    if url is None:
        url = url_for('show_index')
    return [logname, url]


@insta485.app.route('/uploads/<path:name>')
def download_file(name):
    """Return file if valid."""
    if not is_user_logged_in():
        print("not logged in")
        abort(403)
    if not pathlib.Path.exists(insta485.app.config['UPLOAD_FOLDER']/name):
        abort(404)
    return send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                               name, as_attachment=True)


def compute_password(salt, password):
    """Compute password with and without supplied salt."""
    if salt == "":
        salt = uuid.uuid4().hex
    algorithm = 'sha512'
    password_salted = salt + password
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def add_image(request_file):
    """Add image to database."""
    # Unpack flask object
    fileobj = request_file
    filename = fileobj.filename

    # Compute base name (filename without directory).  We use a UUID to avoid
    # clashes with existing files,
    # and ensure that the name is compatible with the
    # filesystem. For best practive, we ensure uniform file extensions (e.g.
    # lowercase).
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename


def delete_photo(photo):
    """Delete photo from database."""
    path = insta485.app.config["UPLOAD_FOLDER"]/photo
    pathlib.Path.unlink(path)
    return True
