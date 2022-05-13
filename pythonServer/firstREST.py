import json
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

jedis = [
    {"name": 'Yoda', "id": 1},
    {"name": 'Luke', "id": 2},
    {"name": 'Obi wan', "id": 3}
]

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/jedis',methods=['GET'])
def getJedi():
    return jsonify( jedis )

@app.route('/api/jedis',methods=['POST'])
def createJedi():
    request_data = request.get_json()
    jedis.append(request_data)
    return jsonify( request_data )

@app.route('/api/jedis', methods=['PUT'])
def update_jedi():
    request_data = request.get_json()
    for jedi in jedis:
        if jedi["id"] == request_data['id']:
            jedi.update(request_data)
            return jsonify(jedis)
    return json.dumps({'message': 'jedi id not found'})

@app.route('/api/jedis', methods=['DELETE'])
def remove_jedi():
    request_data = request.get_json()
    for jedi in jedis:
        if jedi["id"] == request_data['id']:
            jedis.remove(jedi)
            return jsonify(jedis)
    return json.dumps({'message': 'jedi id not found'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)