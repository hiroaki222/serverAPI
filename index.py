#import chromedriver_binary
from flask import Flask, jsonify, render_template, request
import json

with open('config.json') as f:
    di = json.load(f)

def data():
    with open('data.json') as f:
        data = json.load(f)
    return data

app = Flask(__name__)
app.json.ensure_ascii = False

@app.route('/')
def index():
    return "<p>Hello, World!</p>"
    #return render_template('index.html')

""" @app.route('/info', methods = ['GET'])
def info():
    return data()

@app.route('/detect', methods = ['GET'])
def detect():
    with open('config.json') as f:
        conf = json.load(f)
    return jsonify({"flag" : conf['flag']})

@app.route('/detecter', methods = ['PUT'])
def detecter():
    req = request.args
    flag = req.get("flag")
    print(flag)
    with open('config.json') as f:
        j = json.load(f)
    if flag == '1':
        j['flag'] = '1'
    elif flag == '0':
        j['flag'] = '0'
    else:
        return jsonify({'Status' : 'error'})
    with open('config.json', 'w') as f:
        json.dump(j, f, indent=2, ensure_ascii=False)
    return jsonify({'Status' : 'Success'}) """

""" if __name__=='__main__':
    app.debug=True
    app.run(host=di['ip'], port=di['port']) """