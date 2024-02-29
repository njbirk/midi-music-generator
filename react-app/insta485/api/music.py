"""REST API for likes."""
import flask
import insta485
from insta485.api.helpers import check_basic_auth


@insta485.app.route('/api/v1/midi/')
def get_midi():
    '''
    """Get posts based on size, page, and postid (>=)."""
    # Do user authentication (either sessions or http basic access)
    # Check if user is logged in or has credentials
    basic_ath = check_basic_auth()
    if "username" not in flask.session and not basic_ath:
        return flask.jsonify({"message": "Forbidden", "status_code": 403}), 403
    logname = ""
    if basic_ath is True:
        # user used authorization
        logname = flask.request.authorization['username']
    elif basic_ath is False:
        # user used sessions
        logname = flask.session["username"]

    # Get args
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get('page', default=0, type=int)
    if size <= 0 or page < 0:
        return (flask.jsonify({"message": "Bad Request", "status_code": 400}),
                400)
    offset = page * size
    # get id of most recent post for postid_lte
    connection = insta485.model.get_db()
    most_recent = connection.execute(
        "SELECT postid FROM posts ORDER BY postid DESC LIMIT 1")
    most_recent = most_recent.fetchall()
    postid_lte = flask.request.args.get('postid_lte',
                                        default=most_recent[0]['postid'],
                                        type=int)

    # Get size newest posts
    allposts = connection.execute(
        "SELECT posts.postid "
        "FROM posts "
        "INNER JOIN following "
        "ON ((posts.owner = username2 AND username1 = ?) OR posts.owner = ?) "
        "AND posts.postid <= ?"
        "GROUP BY posts.postid "
        "ORDER BY posts.postid DESC "
        "LIMIT ? OFFSET ?",
        (logname, logname, postid_lte, size, offset)
    )
    allposts = allposts.fetchall()

    posts = []
    for post in allposts:
        # add the url stuff for each post
        url = "/api/v1/posts/" + str(post["postid"]) + "/"
        print(url)
        newpost = {"postid": post["postid"], "url": url}
        posts.append(newpost)  # add to our list
    print(posts)

    # check if there will be a next page & update next url
    nexturl = ""
    if len(allposts) == size:
        page = page + 1
        nexturl = (f"/api/v1/posts/?size={size}&page={page}"
                   f"&postid_lte={postid_lte}")

    # use LIMIT (good) and OFFSET (TODO) for queue
    # url = flask.request.path
    # changed code to below because it would include the "?" even if no args
    url = flask.request.environ['RAW_URI']
    print(url)
    # (TODO) get rid of page size
    context = {"next": nexturl, "results": posts, "url": url}

    return flask.jsonify(**context), 200'''

