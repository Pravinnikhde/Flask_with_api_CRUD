import unittest
import json
from app import app, db, Employee

class EmployeeTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        with app.app_context():
            db.create_all()
            # Add some initial data
            employee = Employee(
                name='Test User',
                email='testuser@example.com',
                job='Developer',
                address={'city': 'Test City'},
                skills=['Python', 'Flask'],
                age=30
            )
            db.session.add(employee)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            
            db.drop_all()

    def test_add_employee(self):
        new_employee = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'job': 'Engineer',
            'address': {'city': 'New York'},
            'skills': ['Java', 'Spring'],
            'age': 35
        }
        response = self.app.post('/employees', data=json.dumps(new_employee), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['name'], new_employee['name'])
        self.assertEqual(response.json['email'], new_employee['email'])
        self.assertEqual(response.json['job'], new_employee['job'])
        self.assertEqual(response.json['address'], new_employee['address'])
        self.assertEqual(response.json['skills'], new_employee['skills'])
        self.assertEqual(response.json['age'], new_employee['age'])

    def test_get_employees(self):
        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_employee(self):
        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Test User')
        self.assertEqual(response.json['email'], 'testuser@example.com')

    def test_update_employee(self):
        updated_employee = {
            'name': 'Updated User',
            'email': 'updateduser@example.com',
            'job': 'Senior Developer',
            'address': {'city': 'Updated City'},
            'skills': ['Django'],
            'age': 40
        }
        response = self.app.put('/employees/1', data=json.dumps(updated_employee), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Employee updated successfully')

        # Verify the update
        response = self.app.get('/employees/1')
        self.assertEqual(response.json['name'], updated_employee['name'])
        self.assertEqual(response.json['email'], updated_employee['email'])
        self.assertEqual(response.json['job'], updated_employee['job'])
        self.assertEqual(response.json['address'], updated_employee['address'])
        self.assertEqual(response.json['skills'], updated_employee['skills'])
        self.assertEqual(response.json['age'], updated_employee['age'])

    def test_delete_employee(self):
        response = self.app.delete('/employees/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Employee deleted successfully')

        # Verify deletion
        response = self.app.get('/employees/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
