# Usage

The application works as part of the network of containers in ass2 network.

To be able to test the app.py we should launch the network of docker containers.

For that refer to the readme.md file in main folder

# Endpoints

GET /me
GET /students
GET /students/<student_id>
POST /students/add/<student_id>
DELETE /students/<student_id> endpoint
GET /takes
GET /takes/<student_id>
POST /takes/add/<student_id>
DELETE /takes/remove/<student_id>
