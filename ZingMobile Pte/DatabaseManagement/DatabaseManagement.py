from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
colleges_data = {
    "Sri Chaitanya": {
        "Telangana": {
            "Hyderabad": {
                "KPHB": {
                    "A": {
                        "students": [
                            {"id": 1, "name": "John Doe", "section": "A", "marks": {"Math": 90, "Science": 85}},
                            {"id": 2, "name": "Alice Smith", "section": "A", "marks": {"Math": 88, "Science": 82}}
                        ]
                    },
                    "B": {
                        "students": [
                            {"id": 3, "name": "Bob Johnson", "section": "B", "marks": {"Math": 85, "Science": 80}},
                            {"id": 4, "name": "Emily Davis", "section": "B", "marks": {"Math": 87, "Science": 84}}
                        ]
                    }
                }
            }
        }
    }
}

# Define roles
ROLES = ["Super admin", "Admin", "Teacher", "Student"]

# Helper function to check if the user has permission
def has_permission(role, college=None, section=None):
    if role == "Super admin":
        return True
    elif role == "Admin" and college in colleges_data:
        return True
    elif role == "Teacher" and college in colleges_data and section in colleges_data[college]:
        return True
    elif role == "Student":
        return True
    return False

# Get all data
@app.route('/api/data', methods=['GET'])
def get_all_data():
    role = request.headers.get('Role')
    if role not in ROLES:
        return jsonify({"message": "Invalid role"}), 403

    if not has_permission(role):
        return jsonify({"message": "Permission denied"}), 403

    return jsonify(colleges_data)

# Get data for a specific college
@app.route('/api/data/college/<college_name>', methods=['GET'])
def get_college_data(college_name):
    role = request.headers.get('Role')
    if role not in ROLES:
        return jsonify({"message": "Invalid role"}), 403

    if not has_permission(role, college=college_name):
        return jsonify({"message": "Permission denied"}), 403

    if college_name not in colleges_data:
        return jsonify({"message": "College not found"}), 404

    return jsonify(colleges_data[college_name])

# Get data for a specific section within a college
@app.route('/api/data/college/<college_name>/section/<section_name>', methods=['GET'])
def get_section_data(college_name, section_name):
    role = request.headers.get('Role')
    if role not in ROLES:
        return jsonify({"message": "Invalid role"}), 403

    if not has_permission(role, college=college_name, section=section_name):
        return jsonify({"message": "Permission denied"}), 403

    if college_name not in colleges_data or section_name not in colleges_data[college_name]:
        return jsonify({"message": "College or section not found"}), 404

    return jsonify(colleges_data[college_name][section_name])

# Get data for a specific student within a section of a college
@app.route('/api/data/college/<college_name>/section/<section_name>/student/<int:student_id>', methods=['GET'])
def get_student_data(college_name, section_name, student_id):
    role = request.headers.get('Role')
    if role not in ROLES:
        return jsonify({"message": "Invalid role"}), 403

    if not has_permission(role, college=college_name, section=section_name):
        return jsonify({"message": "Permission denied"}), 403

    if college_name not in colleges_data or section_name not in colleges_data[college_name]:
        return jsonify({"message": "College or section not found"}), 404

    students = colleges_data[college_name][section_name]["students"]
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    return jsonify(student)

if __name__ == '__main__':
    app.run(debug=True)
