from collections import defaultdict
from datetime import datetime

from flask import Flask,jsonify, request
from flask_restplus import Api, Resource, fields
from flask_pymongo import PyMongo

app = Flask(__name__)
api = Api(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/employees"
mongo = PyMongo(app)
employee = mongo.db.user
ns_emp = api.namespace("Employees", description = "Methods")

emp_data = []
for data in employee.find():
    emp_data.append(data) 


# @ns_emp.route('/')
# class Employee(Resource):
#     def get(self):
#         query = employee.find().limit(3)
#         result = []
#         for data in query:
#             result.append(data)
#         print(result)
#         return jsonify(result)


@ns_emp.route('/get_emp')
class get_employee(Resource):
    def get(self):
        try:
            users = []
            emp_data = employee.find()
            for data in emp_data:
                users.append(data["name"])
            print("users:",users)
            return jsonify({"List of Employees": users})
        except Exception as e:
            print("47")
            print("exception:",e)


@ns_emp.route('/create_emp', methods=["POST"])
class create_employee(Resource):
    def post(self):
        # emp_data = employee.find()
        # result = []
        # for data in emp_data:
        #     x = data["salaries"][-1]
        #     if x["from_date"] <= datetime.now() <= x["to_date"]:
        #         result.append({"emp_id" : data["_id"], "first name" : data["first_name"], "last name" : data["last_name"], "salary" : x["salary"]})
        #
        # top10 = sorted(result, key = lambda x: x["salary"], reverse = True)[0:10]
        #
        # return jsonify({"The top 10 highest paid presently working employees are" : top10})
        try:
            content = request.get_json()
            name = content["name"]
            age = content["age"]
            response = 1#employee.save({"name":name, "age":age})
            if response:
                return jsonify({"message": "Employee data added successfully"},201)
            else:
                return jsonify({"message": "Employee data failed to add"}, 401)
        except Exception as e:
            return e

@ns_emp.route('/query3')
class Query3(Resource):   
    def get(self):
        # emp_data = employee.find()
        result = []
        for data in emp_data:
            x = data["titles"][-1]
            if x["from_date"] <= datetime.now() <= x["to_date"] and x["title"] == "Senior Engineer":
                result.append({"emp_id" : data["_id"], "first name" : data["first_name"], "last name" : data["last_name"], "dept" : data["dept"][0]["dept"]})
        return jsonify({"List of Senior Engineers presently working ": result, "count": len(result)}) 


@ns_emp.route('/query4')
class Query4(Resource):   
    def get(self):
        # emp_data = employee.find()
        result = defaultdict(lambda: defaultdict(int))
        for data in emp_data:
            title = data["titles"][-1]
            dept = data["dept"][0]
            if title["from_date"] <= datetime.now() <= title["to_date"]:
                result[dept["dept"]][title["title"]] += 1
        return jsonify({"Count of employees by dept. titles:" : result}) 


# @ns_emp.route('/query4')
# class Query4(Resource):   
#     def get(self):
#         emp_data = employee.find()
#         result = defaultdict(int)
#         for data in emp_data:
#             x = data["dept"][0]
#             if x["from_date"] <= datetime.now() <= x["to_date"]:
#                 result[x["dept"]] += 1
#         return jsonify({"Count of employees by department" : result}) 


@ns_emp.route('/query5')
class Query5(Resource):   
    def get(self):
        # emp_data = employee.find()
        result = []
        hire_date = datetime(1800, 1, 1)
        for data in emp_data:
            if data["hire_date"] > hire_date:
                hire_date = data["hire_date"] 
                result = []
                result.append({"emp_id" : data["_id"], "first name" : data["first_name"], "last name" : data["last_name"], "dept" : data["dept"][0]["dept"], "title" : data["titles"][-1]["title"]})

            elif data["hire_date"] == hire_date:
                result.append({"emp_id" : data["_id"], "first name" : data["first_name"], "last name" : data["last_name"], "dept" : data["dept"][0]["dept"], "title" : data["titles"][-1]["title"]})

        return jsonify({"hire date" : hire_date, "Last hired employees": result})



if __name__ == '__main__':
    app.run(debug = True)


# Sourcr: https://github.com/SnehaChebrolu27/Employees_flaskrestplus