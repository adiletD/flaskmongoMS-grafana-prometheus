# importing required modules
import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from prometheus_flask_exporter import PrometheusMetrics


# init our app
app = Flask(__name__)

# init prometheus metrics
metrics = PrometheusMetrics(app)


metrics.info("app_info", "App Info", version="1.0.0")


# the status codes

ERR_CODE_NOT_FOUND = {
    "error": "not found"
}

ERR_CODE_CONFLICT = {
    "error": "conflict"
}

SUCCESS_CODE = {
    "success"
}

# script for openning access to the database


def get_db():
    client = MongoClient(host=os.environ['MONGO_SERVER_HOST'],
                         # convert the port number to make sure its an integer
                         port=int(os.environ['MONGO_SERVER_PORT']),
                         username=os.environ['MONGO_USERNAME'],
                         password=os.environ['MONGO_PASSWORD'],
                         )
    if client:
        db = client["university"]
        return db
    else:
        return ERR_CODE, 404   # if cant connect then return error


@app.route('/')
def hello():
    return "Hello bro!"

# GET /me endpoint - returns my name


@app.route('/me', methods=['GET'])
def getMe():
    return jsonify({"student_id": "18078666d", "name": "Adilet Daniiarov"}), 200

# Every route below will:
# 1. initialize the database access
# 2. make a query to the db
# 3. ensure we get a proper query result, if not return an error response message
# 4. convert the query into the format we need
# 5. return the jsonified response


# GET /students endpoint - returns info of all the students in the database
@app.route('/students', methods=['GET'])
def get_students():
    db = get_db()
    _students = db.student.find().sort("student_id", 1)
    students = [{"dept_name": student["dept_name"], "gpa": student["gpa"],
                 "name": student["name"], "student_id": student["student_id"]} for student in _students]
    return jsonify(students), 200


# GET /students/<student_id> endpoint - returns the info about an indicated student
@app.route('/students/<student_id>', methods=['GET'])
def getStudentById(student_id):
    db = get_db()
    student = db.student.find_one({'student_id': student_id})
    if student:
        result = [{"dept_name": student["dept_name"], "gpa": student["gpa"],
                   "name": student["name"], "student_id": student["student_id"]}]
    else:
        return jsonify(ERR_CODE), 404
    return jsonify(result), 200

# POST /students/add/<student_id> endpoint - adds a student specified in the request body


@app.route('/students/add', methods=['POST'])
def addStudent():
    db = get_db()
    # check if the student already exists
    student_id = request.get_json().get('student_id')
    student = db.student.find_one({'student_id': student_id})
    if student:
        return jsonify("Student already exists"), 409
    # if the stud does not exist then add him
    else:
        dept_name = request.get_json().get("dept_name")
        gpa = request.get_json().get("gpa")
        name = request.get_json().get("name")
        student_id = request.get_json().get("student_id")

        result = [{"dept_name": dept_name, "gpa": gpa,
                  "name": name, "student_id": student_id}]

        db.student.insert_one(result[0])

    return jsonify("Success!"), 200

# DELETE /students/<student_id> endpoint - returns the info about an indicated student


@app.route('/students/remove/<student_id>', methods=['DELETE'])
def removeStudent(student_id):
    db = get_db()
    student = db.student.find_one({'student_id': student_id})
    if student:
        db.student.delete_one({"student_id": student_id})
        return jsonify("Student deleted!"), 200
    else:
        return jsonify(ERR_CODE), 404
    return jsonify("Success!"), 200


@app.route('/takes', methods=['GET'])
def getStudentsCourses():
    db = get_db()
    # sort the students by the student_id parameter in ascending order
    _students = db.student.find().sort("student_id", 1)
    if _students:
        students = []
        for student in _students:
            _courses = db.takes.find(
                {'student_id': student["student_id"]}).sort('course_id', 1)
            courses = [{"course_id": course["course_id"],
                        "credits":course["credits"]} for course in _courses]
            students.append({"dept_name": student["dept_name"], "gpa": student["gpa"],
                            "name": student["name"], "student_id": student["student_id"], "student_takes": courses})
        return jsonify(students), 200
    else:
        return jsonify(ERR_CODE), 404


@app.route('/takes/<student_id>', methods=['GET'])
def getStudentsCoursesById(student_id):
    db = get_db()
    student = db.student.find_one({'student_id': student_id})
    if student:
        _courses = db.takes.find(
            {'student_id': student["student_id"]}).sort('course_id', 1)
        courses = [{"course_id": course["course_id"],
                    "credits":course["credits"]} for course in _courses]
        result = [{"dept_name": student["dept_name"], "gpa": student["gpa"],
                   "name": student["name"], "student_id": student["student_id"], "student_takes": courses}]
        return jsonify(result), 200
    else:
        return jsonify(ERR_CODE), 404

# GET /takes/<student_id> endpoint - returns the indicated student and the courses he/she takes


@app.route('/takes/add/<student_id>', methods=['POST'])
def addStudentsCourses(student_id):
    db = get_db()
    student = db.student.find_one({'student_id': student_id})
    course_id = request.get_json().get("course_id")
    if student:
        course = db.takes.find_one(
            {'student_id': student["student_id"], 'course_id': course_id})

        if course:
            return jsonify("The course is already registered"), 409
        else:
            course_id = request.get_json().get("course_id")
            credits = request.get_json().get("credits")

            db.takes.insert_one(
                {'student_id': student_id, 'course_id': course_id, 'credits': credits})
        return jsonify("Success!"), 200
    else:
        return jsonify(ERR_CODE), 404


@app.route('/takes/remove/<student_id>', methods=['DELETE'])
def removeStudentsCourses(student_id):
    db = get_db()
    student = db.student.find_one({'student_id': student_id})
    course_id = request.get_json().get("course_id")
    if student:
        course = db.takes.find_one(
            {'student_id': student["student_id"], "course_id": course_id})
        if course:
            db.takes.delete_one(
                {'student_id': student_id, 'course_id': course_id})
        else:
            return jsonify(ERR_CODE), 404

        return jsonify("Success!"), 200
    else:
        return jsonify(ERR_CODE), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=15000, debug=False)
