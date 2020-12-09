import flask
from flask import request, jsonify, abort, g
import sqlite3
import redis
from rq import Queue
import json
from insertDb import insertQueue
from analysis import hashtagAnalysis

q = Queue(connection=redis.Redis())

rdb = redis.Redis(host='localhost', port=6379, db=0)

app = flask.Flask(__name__)
#app.config.from_envvar('APP_CONFIG')

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('../mockroblog.db')
        db.row_factory = make_dicts
    return db

@app.route('/trending')
def trendingHashtag():
    result = {}  
    for key, score in rdb.zrevrange('hashtag', 0, 24, 'withscores'):
        result[str(key,encoding='UTF-8')] = score
    return result

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/<string:username>/home')
def getHomeTimeline(username):
    app.logger.debug(f'getHomeTimeline(%r)', username)
    return jsonify([])


@app.route('/', methods=['GET'])
def getPublicTimeline():
    app.logger.debug('getPublicTimeline()')
    return jsonify([])

def getUserTimeline(username):
    app.logger.debug(f'getUserTimeline(%r)', username)

@app.route('/post_tweet', methods=['POST'])
def postTweet(username,text):
    data = request.data
    q.enqueue(insertQueue, data)      
    q.enqueue(hashtagAnalysis, data)
    
@app.route('/<string:username>/', methods=['GET', 'POST'])
def userTimeline(username):
    if request.method == 'GET':
        getUserTimeline(username)
        return jsonify([]), 200
    elif request.method == 'POST':
        json = request.get_json()
        if json and 'text' in json:
            postTweet(username, json['text'])
            return jsonify(), 201
        else:
            return jsonify(), 400

if __name__ == '__main__':
    app.run(debug=True)

