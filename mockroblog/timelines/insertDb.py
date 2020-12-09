import sqlite3
import json

def insertQueue(data):
    final_data = json.loads(data)
    user_id = final_data['user_id']
    text = final_data['text']
    db = sqlite3.connect('../mockroblog.db')
    sql= 'INSERT INTO posts(user_id,text) VALUES(?,?)'
    cur = db.cursor()
    cur.execute(sql,(user_id,text))
    db.commit()
    db.close() 
