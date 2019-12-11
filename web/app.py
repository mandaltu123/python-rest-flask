from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

# create a mongodb client using pymongo
client = MongoClient("mongodb://db:27017")
# create a db
db = client.aNewDb
UserNum = db["UserNum"]
UserNum.insert({
    'num_of_users': 0
})


class Visit(Resource):
    def get(self):
        print("in Visit resource...")
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update_one({}, {"$set": {"num_of_users": new_num}})
        return str("Hello user " + str(new_num))


def checkPostedData(postedData, functionName):
    print(f"I am in checkPostedData method and the function we are validating is {functionName}")
    if "x" not in postedData or "y" not in postedData:
        return 301
    else:
        print("************In that else condition")
        if functionName == "division":
            if int(postedData["y"]) == 0:
                return 301
        return 200


class Add(Resource):
    def post(self):
        # If I am here, then then the resource Add was requested
        # get posted data
        postedData = request.get_json()
        # validate posted data
        status_code = checkPostedData(postedData, "add")
        print("validation stus code = ", status_code)
        if (status_code != 200):
            ret_json = {
                "Mesasge": "An error has occured",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        result = x + y
        re_map = {
            "Message": result,
            "Status Code": 200
        }
        return jsonify(re_map)


class Subtract(Resource):
    def post(self):
        # If I am here, then then the resource Add was requested
        # get posted data
        postedData = request.get_json()
        # validate posted data
        status_code = checkPostedData(postedData, "subtract")
        print("validation stus code = ", status_code)
        if (status_code != 200):
            ret_json = {
                "Mesasge": "An error has occured",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        result = x - y
        ret_json = {
            "Message": result,
            "Status code": 200
        }
        return jsonify(ret_json)


class Multiplpy(Resource):
    def post(self):
        # If I am here, then then the resource Add was requested
        # get posted data
        postedData = request.get_json()
        # validate posted data
        status_code = checkPostedData(postedData, "multiply")
        print("validation stus code = ", status_code)
        if (status_code != 200):
            ret_json = {
                "Mesasge": "An error has occured",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        result = x * y
        ret_json = {
            "Message": result,
            "Status code": 200
        }
        return jsonify(ret_json)


class Divde(Resource):
    def post(self):
        # If I am here, then then the resource Add was requested
        # get posted data
        postedData = request.get_json()
        # validate posted data
        status_code = checkPostedData(postedData, "division")
        print("validation stus code = ", status_code)
        if (status_code != 200):
            ret_json = {
                "Mesasge": "An error has occured",
                "Status Code": status_code
            }
            return jsonify(ret_json)

        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        # turning into float to get a better looking output
        result = (x * 1.0) / y
        ret_json = {
            "Message": result,
            "Status code": 200
        }
        return jsonify(ret_json)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiplpy, "/multiply")
api.add_resource(Divde, "/division")
api.add_resource(Visit, "/hello")

@app.route('/')
def hello_world():
    return 'hello world'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
