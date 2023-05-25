from flask import Flask, jsonify, render_template, request
import sqlite3

with open('ip-port.json') as f:
    di = json.load(f)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/GetItem', methods=['GET'])
def get():
    con = sqlite3.connect('TestDB.db')
    cur = con.cursor()
    number = request.args['number']
    cur.execute('select * from players where number = ?', (number,))
    data = cur.fetchall()
    con.commit()
    con.close()
    
    return jsonify(data)

# curl -X POST -d "number=26&name=mahrez" http://172.18.134.60:5000/UpdateItem
@app.route('/UpdateItem', methods=['POST'])
def update():
    con = sqlite3.connect('TestDB.db')
    cur = con.cursor()
    name = request.form['name']
    number = request.form['number']
    cur.execute('update players set name = ? where number = ?', (name, number))
    cur.execute('select * from players where number = ?', (number,))
    data = cur.fetchall()
    con.commit()
    con.close()

    return jsonify(data)

@app.route('/AddItem', methods=['POST'])
def add():
    con = sqlite3.connect('TestDB.db')
    cur = con.cursor()
    number = request.form['number']
    name = request.form['name']
    cur.execute('insert into players values(?, ?)', (number, name))
    cur.execute('select * from players')
    data = cur.fetchall()
    con.commit()
    con.close()

    return jsonify(data)

@app.route('/ShowAll', methods=['GET'])
def all():
    con = sqlite3.connect('TestDB.db')
    cur = con.cursor()
    cur.execute('select * from players')
    data = cur.fetchall()
    con.commit()
    con.close()

    return jsonify(data)

# curl -X GET -H "header: {\"key\":\"value\"}" http://172.18.134.60:5000/GetJson
@app.route('/GetJson')
def get_json_header():
    json_header = request.headers.get('header')
    return json_header

if __name__=='__main__':
    app.debug=True
    app.run(host=di['ip'], port=di['port'])