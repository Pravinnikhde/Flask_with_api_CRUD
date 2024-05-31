from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    job = db.Column(db.String(80), nullable=False)
    address = db.Column(db.JSON, nullable=True)
    skills = db.Column(db.JSON, nullable=True)
    age = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=True)

with app.app_context():
    db.create_all()


@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    print(data)
    if not data or not 'name' in data or not 'email' in data or not 'job'  in data or not 'age' in data or not 'address' in data or not 'skills' in data:
        abort(400, description="Bad Request: Missing required fields")

    new_employee = Employee(
        name=data['name'],
        email=data['email'],
        job=data['job'],
        address=data.get('address'),
        skills=data.get('skills'),
        age=data['age']
    )

    db.session.add(new_employee)
    db.session.commit()

    external_api_url = "https://reqres.in/api/users"
    payload = {
        "name": new_employee.name,
        "job": new_employee.job,
        "email": new_employee.email,
        "age": new_employee.age,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "zip": "12345"
        },
        "skills": ["JavaScript", "React", "Node.js"]
    }

    response = requests.post(external_api_url, json=payload)
    if response.status_code == 201:
        response_data = response.json()
        new_employee.id = response_data['id']
        new_employee.created_on = datetime.strptime(response_data['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
        db.session.commit()

    return jsonify({"id": new_employee.id,
                    'name': new_employee.name,
                    'email': new_employee.email,
                    'job': new_employee.job,
                    'address': new_employee.address,
                    'skills': new_employee.skills,
                    'age': new_employee.age,
                    'created_on': new_employee.created_on}), 201

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'email': e.email,
        'job': e.job,
        'address': e.address,
        'skills': e.skills,
        
        'age': e.age,
        'created_on': e.created_on
    } for e in employees])

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employee = Employee.query.get_or_404(id)
    return jsonify({
        'id': employee.id,
        'name': employee.name,
        'email': employee.email,
        'job': employee.job,
        'address': employee.address,
        'skills': employee.skills,
        'age': employee.age,
        'created_on': employee.created_on
    })

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get_or_404(id)
    data = request.get_json()
    if not data:
        abort(400, description="Bad Request: No data provided")

    if 'name' in data:
        employee.name = data['name']
    if 'email' in data:
        employee.email = data['email']
    if 'job' in data:
        employee.job = data['job']

    if 'age' in data:
        employee.age = data['age']
    if 'address' in data:
        employee.address = data['address']
    if 'skills' in data:
        employee.skills = data['skills']

    db.session.commit()
    return jsonify({'message': 'Employee updated successfully'})

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
