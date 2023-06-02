
from flask import Flask, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/players"
mongo = PyMongo(app)


@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.json
    db_response = mongo.db.player_data.insert_one(data)
    return dumps({'message': 'Player added successfully', 'id': str(db_response.inserted_id)})


@app.route('/get_players', methods=['GET'])
def get_players():
    players = mongo.db.player_data.find()
    return dumps(players)


@app.route('/get_player/<id>', methods=['GET'])
def get_player(id):
    player = mongo.db.player_data.find_one({'_id': ObjectId(id)})
    return dumps(player)


@app.route('/update_player/<id>', methods=['PUT'])
def update_player(id):
    data = request.json
    mongo.db.player_data.update_one({'_id': ObjectId(id)}, {"$set": data})
    return dumps({'message': 'Player updated successfully'})


@app.route('/delete_player/<id>', methods=['DELETE'])
def delete_player(id):
    mongo.db.player_data.delete_one({'_id': ObjectId(id)})
    return dumps({'message': 'Player deleted successfully'})


if __name__ == '__main__':
    app.run(debug=True)
