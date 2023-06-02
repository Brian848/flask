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


@app.route('/get_max_touchdowns', methods=['GET'])
def get_max_touchdowns():
    player = mongo.db.player_data.find().sort("touchdown_passes", -1).limit(1)
    return dumps(player)


@app.route('/get_max_rushing_yards', methods=['GET'])
def get_max_rushing_yards():
    player = mongo.db.player_data.find().sort("rushing_yards", -1).limit(1)
    return dumps(player)


@app.route('/get_min_rushing_yards', methods=['GET'])
def get_min_rushing_yards():
    player = mongo.db.player_data.find().sort("rushing_yards", 1).limit(1)
    return dumps(player)


@app.route('/get_field_goals', methods=['GET'])
def get_field_goals():
    players = mongo.db.player_data.find().sort("field_goals", -1)
    return dumps(players)


@app.route('/get_max_sacks', methods=['GET'])
def get_max_sacks():
    player = mongo.db.player_data.find().sort("sacks", -1).limit(1)
    return dumps(player)


if __name__ == '__main__':
    app.run(debug=True)
