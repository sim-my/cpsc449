# Mockroblog - Mock APIs for Microblogging

**Q.** What's the minimum amount of code needed to mock up a miniature
       clone of Twitter?

**A.** How comfortable are you with SQL?

## Getting started

Use the following commands to get up and running:

```shell-session
$ python3 -m pip install sandman2 datasette   # install utilities
$ make                                        # create database
$ foreman start                               # start services
```

## Tools

See the following references for more information:

* [sandman2](https://github.com/jeffknupp/sandman2)
* [datasette](https://github.com/simonw/datasette)
* [make](https://en.wikipedia.org/wiki/Makefile)
* [sqlite3](https://sqlite.org/cli.html)
* [foreman](https://ddollar.github.io/foreman/)
* [http](https://httpie.org/)
* [jq](https://stedolan.github.io/jq/)

## API Implementations

As a reminder, here is the API we were originally hoping to implement:

API call                                     | Action
-------------------------------------------- | -----------------------------------------------------------------------------------------------------------
`createUser(username, email, password)`      | Registers a new user account.
`authenticateUser(username, password)`       | Returns true if the supplied password matches the hashed password stored for that username in the database.
`addFollower(username, usernameToFollow)`    | Start following a new user.
`removeFollower(username, usernameToRemove)` | Stop following a user.
`getUserTimeline(username)`                  | Returns recent tweets from a user.
`getPublicTimeline()`                        | Returns recent tweets from all users.
`getHomeTimeline(username)`                  | Returns recent tweets from all users that this user follows.
`postTweet(username, text)`                  | Post a new tweet.

### Our mock API

The effect of each of these API calls can be duplicated by connecting
`sandman2` and Datasette to `mockroblog.db` and calling those APIs.

Note that this is *not* as nice an experience as using a well-designed
custom API. There are multiple cases where `sandman2` requires a
primary key (e.g. user ID) where a different key (e.g. username) would
be preferable.

**`createUser(username, email, password)`**

> ```shell-session
> $ http localhost:5000/users/ username=tester email=test@example.com password=testing
> ```

**`authenticateUser(username, password)`**

> ```shell-session
> $ http 'localhost:5000/users/?username=ProfAvery&password=password'
> ```

**`addFollower(username, usernameToFollow)`**

> ```shell-session
> $ http POST localhost:5000/followers/ follower_id=4 following_id=2
> ```

**`removeFollower(username, usernameToRemove)`**

> ```shell-session
> $ id=$(http 'localhost:5000/followers/?follower_id=4&following_id=2' | jq .resources[0].id)
> $ http DELETE localhost:5000/followers/$id
> ```

**`getUserTimeline(username)`**

> ```shell-session
> $ http 'localhost:5100/mockroblog/posts.json?_facet=user_id&user_id=1&_sort_desc=timestamp&_labels=on&_shape=array'
> ```

**`getPublicTimeline()`**

> ```shell-session
> $ http localhost:5000/posts/?sort=-timestamp
> ```

**`getHomeTimeline(username)`**

> ```shell-session
> $ http 'localhost:5100/mockroblog/home.json?_facet=username&username=ProfAvery&_shape=array'
> ```

**`postTweet(username, text)`**

> ```shell-session
> $ http POST localhost:5000/posts/ user_id=4 text='This is a test.'
> ```

### Skeleton code for the Timelines API

Alternatively, if you wish to implement the Timelines API yourself
in Python, the `timelines/` directory contains skeleton code for a
microservice that exposes the original API.

The skeleton code:

* includes the [Flask SQLite 3 helper
  routines](https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/)

* sets the database to `mockroblog.db`

* provides routes and API functions for all methods in the original
  Timelines API

* hard-codes all methods to return an empty JSON object or list

