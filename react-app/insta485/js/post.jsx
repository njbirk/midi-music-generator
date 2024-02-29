import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import InfiniteScroll from "react-infinite-scroll-component";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

export default function App({ url }) {
  // url: /api/v1/posts/
  const [totalPosts, setTotalPosts] = useState([]);
  const [next, setNext] = useState("");

  const fetchData = React.useCallback(() => {
    // TODO: we may or may not need to use useEffect
    fetch(next, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        // next, results, curUrl maybe???
        setNext(data.next);
        setTotalPosts([...totalPosts, ...data.results]);
      })
      .catch((error) => console.log(error));
  }, [next, totalPosts]);

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          // next, results, curUrl maybe???
          setNext(data.next);
          setTotalPosts(data.results);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

  return (
    <InfiniteScroll
      dataLength={totalPosts.length} // This is important field to render the next data
      next={fetchData}
      hasMore={next !== ""}
      loader={<h4>Loading...</h4>}
      endMessage={
        <p style={{ textAlign: "center" }}>
          <b>Yay! You have seen it all</b>
        </p>
      }
    >
      <Feed allposts={totalPosts} />
    </InfiniteScroll>
  );
}

function Feed({ allposts }) {
  // /api/v1/posts/
  const listItems = allposts.map((aPost) => (
    <li key={aPost.postid}>
      <Post url={aPost.url} postid={aPost.postid} />
    </li>
  ));

  // Render post image and post owner
  return <ul className="no-bullets">{listItems}</ul>;
}

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
function Post({ url, postid }) {
  /* Display image and post owner of a single post */

  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [created, setCreated] = useState("");
  const [numLikes, setNumLikes] = useState(0); // TODO: should be null?
  const [lognameLikesThis, setLognameLikesThis] = useState(null); // change to bool later
  const [likesUrl, setLikesUrl] = useState("");
  const [comments, setComments] = useState([]);

  function doubleClickImage() {
    if (!lognameLikesThis) {
      // logname likes post
      setLognameLikesThis(!lognameLikesThis);
      setNumLikes(numLikes + 1);
      // POST /api/v1/likes/?postid=<postid>
      // "/api/v1/posts/<postid>/"
      const newurl = `/api/v1/likes/?postid=${postid}`;
      fetch(newurl, { credentials: "same-origin", method: "POST" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => setLikesUrl(data.url))
        .catch((error) => console.log(error));
    }
  }

  const ToggleLogname = React.useCallback(() => {
    if (lognameLikesThis) {
      // logname unlikes post
      setNumLikes(numLikes - 1);
      // DELETE /api/v1/likes/<likeid>/
      fetch(likesUrl, { credentials: "same-origin", method: "DELETE" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
        })
        .catch((error) => console.log(error));
    } else {
      // logname likes post
      setNumLikes(numLikes + 1);
      // POST /api/v1/likes/?postid=<postid>
      // "/api/v1/posts/<postid>/"
      const newurl = `/api/v1/likes/?postid=${postid}`;
      fetch(newurl, { credentials: "same-origin", method: "POST" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => setLikesUrl(data.url))
        .catch((error) => console.log(error));
    }
    setLognameLikesThis(!lognameLikesThis);
  }, [likesUrl, lognameLikesThis, numLikes, postid]);

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setImgUrl(data.imgUrl);
          setOwner(data.owner);
          const time = dayjs(data.created)
            .utc(true)
            .local()
            .format("YYYY-MM-DD HH:mm:ss");
          console.log(dayjs(time).fromNow());
          setCreated(dayjs(time).fromNow());
          setLognameLikesThis(data.likes.lognameLikesThis);
          setNumLikes(data.likes.numLikes);
          setLikesUrl(data.likes.url);
          setComments(data.comments);
          setOwnerImgUrl(data.ownerImgUrl);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);

  // Render post image and post owner
  // TODO: do we need the links (<a> tags)?
  return (
    <div className="post">
      <p>
        {owner !== "" && ownerImgUrl !== "" && (
          <a href={`/users/${owner}/`}>
            <img src={ownerImgUrl} alt="owner pfp" className="pfp" />
            <b> {owner}</b>
          </a>
        )}
        {created !== "" && (
          <span className="rightside">
            <a href={url.replace("/api/v1", "")}>{created}</a>
          </span>
        )}
      </p>
      {imgUrl !== "" ? (
        <img
          className="post"
          src={imgUrl}
          alt="post_image"
          onDoubleClick={doubleClickImage}
        />
      ) : (
        <p>loading</p>
      )}

      {lognameLikesThis !== null ? (
        <Likes
          numLikes={numLikes}
          lognameLikesThis={lognameLikesThis}
          ToggleLogname={ToggleLogname}
        />
      ) : (
        <p>loading</p>
      )}
      {owner !== "" && (
        <Comments
          postid={postid}
          setComments={setComments}
          comments={comments}
        />
      )}
    </div>
  );
}

function Likes({ numLikes, lognameLikesThis, ToggleLogname }) {
  return (
    <>
      <p>
        {numLikes} {numLikes === 1 ? "like" : "likes"}{" "}
      </p>
      <button
        className="like"
        data-testid="like-unlike-button"
        type="button"
        onClick={ToggleLogname}
      >
        {lognameLikesThis ? "unlike" : "like"}
      </button>
    </>
  );
}

function Comments({ postid, setComments, comments }) {
  const [textEntry, setTextEntry] = useState("");
  // const [name, setName] = useState(null);

  // Thanks for the lab help :)
  const handleChange = (event) => {
    setTextEntry(event.target.value);
    console.log(event.target.value);
  };

  const handleSubmit = (event) => {
    // prevents website from refreshing (default action of form submission)
    event.preventDefault();

    // fetch post request for comments
    // POST /api/v1/comments/?postid=<postid>
    const newurl = `/api/v1/comments/?postid=${postid}`;
    fetch(newurl, {
      credentials: "same-origin",
      method: "POST",
      body: JSON.stringify({ text: textEntry }),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => setComments([...comments, data]))
      .catch((error) => console.log(error));
    setTextEntry("");
  };

  const removeComment = React.useCallback(
    (commentid) => {
      const newList = comments.filter(
        (comment) => comment.commentid !== commentid,
      );
      setComments(newList);
    },
    [comments, setComments],
  );

  const listItems = comments.map((comment) => (
    <li key={comment.commentid}>
      <p>
        <a href={`/users/${comment.owner}/`}>
          <b>{comment.owner}</b>
        </a>{" "}
        <span data-testid="comment-text">{comment.text}</span>
        {comment.lognameOwnsThis && (
          <DeleteButton
            url={comment.url}
            removeComment={removeComment}
            commentid={comment.commentid}
          />
        )}
      </p>
    </li>
  ));

  return (
    <>
      <ul className="no-bullets">{listItems}</ul>
      <form
        className="comment"
        data-testid="comment-form"
        onSubmit={handleSubmit}
      >
        <input type="text" value={textEntry} onChange={handleChange} />
      </form>
    </>
  );
}

function DeleteButton({ url, removeComment, commentid }) {
  function handleDelete() {
    fetch(url, { credentials: "same-origin", method: "DELETE" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
      })
      .catch((error) => console.log(error));
    // remove the comment from comments state
    removeComment(commentid);
  }

  return (
    <button
      className="inline"
      type="button"
      data-testid="delete-comment-button"
      onClick={handleDelete}
    >
      Delete comment{" "}
    </button>
  );
}

App.propTypes = {
  url: PropTypes.string.isRequired,
};

Feed.propTypes = {
  allposts: PropTypes.arrayOf(PropTypes.oneOfType([PropTypes.object]))
    .isRequired,
};

Post.propTypes = {
  url: PropTypes.string.isRequired,
  postid: PropTypes.number.isRequired,
};

Likes.propTypes = {
  numLikes: PropTypes.number.isRequired,
  lognameLikesThis: PropTypes.bool.isRequired,
  ToggleLogname: PropTypes.func.isRequired,
};

Comments.propTypes = {
  setComments: PropTypes.func.isRequired,
  comments: PropTypes.arrayOf(
    PropTypes.shape({
      commentid: PropTypes.number,
      owner: PropTypes.string,
      text: PropTypes.string,
      lognameOwnsThis: PropTypes.bool,
      ownerShowUrl: PropTypes.string,
      url: PropTypes.string,
    }),
  ).isRequired,
  postid: PropTypes.number.isRequired,
};

DeleteButton.propTypes = {
  url: PropTypes.string.isRequired,
  commentid: PropTypes.number.isRequired,
  removeComment: PropTypes.func.isRequired,
};
