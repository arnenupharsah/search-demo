import requests
import json
import web
import sqlite3
db = web.database(dbn='sqlite', db='streamz')

def new_user(firstname,lastname,phone,email,username):
    db.insert('user', firstname=firstname, lastname=lastname, email=email, phone=phone, username=username)
    params = {'firstname': firstname,'lastname':lastname,'phone':phone,'email':email,'username':username} 
    #requests.post(url1, data=json.dumps(params))
    return json.dumps(params)