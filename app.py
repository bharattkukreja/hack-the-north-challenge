#!flask/bin/python
from flask import Flask, jsonify, abort, request
import json
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Hack the North!"

# Making the dictionary from the sql table
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# fetching all the rows from htn table, adding skills array to it and returning all the rows
def get_rows():
    db = sqlite3.connect('htn.db')
    db.row_factory = dict_factory
    c = db.cursor()
    c.execute("SELECT * from HTN")
    db.commit()
    rows = c.fetchall()
    for row in rows:
        c.execute("SELECT name, rating FROM SKILLS c WHERE c.ID_HTN = " + str(row['ID']))
        db.commit()
        ans = c.fetchall()
        row['SKILLS'] = ans
    c.close()
    return rows

# Note: calling get_rows at the end of each function so as to get the new data

@app.route('/users', methods=['GET'])
def get_data():
    return jsonify(get_rows())

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    rows = get_rows()
    for row in rows:
        if row['ID'] == id:
            return jsonify(row)
    abort(404)

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
     db = sqlite3.connect('htn.db')
     c = db.cursor()
     allowed_keys = ['company', 'email', 'latitude', 'longitude', 'picture', 'name', 'phone']
     for key, val in request.json.iteritems():
         if key in allowed_keys:
             c.execute("UPDATE HTN SET " + str(key) + " = \"" + str(val) + "\" WHERE id = " + str(id))
             db.commit()
     c.close()
     rows = get_rows()
     for row in rows:
        if row['ID'] == id:
            return jsonify(row)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    db = sqlite3.connect('htn.db')
    c = db.cursor()
    c.execute("SELECT id FROM HTN")
    db.commit()
    available_ids = c.fetchall()
    available_ids = [x[0] for x in available_ids]
    if id in available_ids:
        c.execute("DELETE FROM HTN WHERE id = " + str(id))
        db.commit()
        c.execute("DELETE FROM SKILLS WHERE id = " + str(id))
        db.commit()

    c.close()
    return jsonify(get_rows())

if __name__ == '__main__':
    app.run(threaded=True)
