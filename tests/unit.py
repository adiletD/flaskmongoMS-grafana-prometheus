import requests
import pytest
from flask import Flask, jsonify, request

app = Flask(__name__)


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


@app.route('/me', methods=['GET'])
def getMe():
    return jsonify({"student_id": "18078666d", "name": "Adilet Daniiarov"}), 200


def test_getMe():
    response = requests.get("localhost:15000/me")
    assert response.status_code == 200


# def test_get_locations_for_us_90210_check_status_code_equals_200():
#     response = requests.get("http://api.zippopotam.us/us/90210")
#     assert response.status_code == 200


# def test_get_locations_for_us_90210_check_content_type_equals_json():
#     response = requests.get("http://api.zippopotam.us/us/90210")
#     assert response.headers['Content-Type'] == "application/json"


# def test_get_locations_for_us_90210_check_country_equals_united_states():
#     response = requests.get("http://api.zippopotam.us/us/90210")
#     response_body = response.json()
#     assert response_body["country"] == "United States"


# def test_get_locations_for_us_90210_check_city_equals_beverly_hills():
#     response = requests.get("http://api.zippopotam.us/us/90210")
#     response_body = response.json()
#     assert response_body["places"][0]["place name"] == "Beverly Hills"


# def test_get_locations_for_us_90210_check_one_place_is_returned():
#     response = requests.get("http://api.zippopotam.us/us/90210")
#     response_body = response.json()
#     assert len(response_body["places"]) == 1
