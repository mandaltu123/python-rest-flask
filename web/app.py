"""
This class is going to be little more intense than what we did in math_app.py
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import logging

app = Flask(__name__)
api = Api(app)
logging.basicConfig(level=logging.DEBUG)

# create a mongodb client using pymongo
client = MongoClient("mongodb://db:27017")
# create db
db = client.SentenceDatabase
# create collection
Users = db["Users"]


class Register(Resource):
    """ Class that registers a new user"""

    def post(self):
        app.logger.info("I am in post method ...")
        # 1. get posted data by the user
        postedData = request.get_json()
        # Get the data
        username = postedData['username']
        password = postedData['password']
        # hash(password + salt) = ser23423esrwe345
        hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        app.logger.info(f"the hashed password is = {hashed}")
        # Store the username and password into mongodb
        Users.insert_one({
            "username": username,
            "password": hashed,
            "sentence": ""
        })

        retJson = {
            "status": 200,
            "message": "You have successfully signed up for the api"
        }
        return jsonify(retJson)


class Store(Resource):
    """Class that stores a sentence posted by a user with username and password"""

    def post(self):
        app.logger.info("In post method of Store api")
        # first get the posted data
        postedData = request.get_json()
        app.logger.info(f"The posted data is {postedData}")

        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        # verify username and password with database
        correct_password = _verify_password(username, password)
        app.logger.debug(f"correct_password ? {correct_password}")
        if not correct_password:
            return_json = {
                "status": 302,
                "message": "Invalid username / password"
            }
            jsonify(return_json)

        Users.update_one({
            "username": username,
        }, {
            "$set": {"sentence": sentence}
        })
        return_json = {
            "status": 200,
            "message": "sentence saved successfully"
        }
        return jsonify(return_json)


class ListSentences(Resource):
    def post(self):
        # get the posted data
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        # verify username and password with database
        correct_password = _verify_password(username, password)
        app.logger.debug(f"correct_password ? {correct_password}")
        if not correct_password:
            return_json = {
                "status": 302,
                "message": "Invalid username / password"
            }
            jsonify(return_json)

        sentence = Users.find({
            "username": username
        })[0]["sentence"]
        app.logger.debug(f"got the stored sentence for given user  {username} and the sentence is {sentence}")
        # Finally prepare the response
        return_json = {
            "status": 200,
            "sentence": sentence
        }
        return jsonify(return_json)


def _verify_password(username, password):
    """Helper method that verifies whether the given credentials are valid or not """
    hashed_pw = Users.find({
        "username": username
    })[0]["password"]
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(ListSentences, '/list')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
