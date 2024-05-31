# Employee API

This is a simple RESTful API for managing employee records using Flask and SQLAlchemy. It supports CRUD operations and integrates with an external API for additional data processing.

## Features

- Add a new employee
- Retrieve all employees
- Retrieve a single employee by ID
- Update an existing employee
- Delete an employee

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Requests


2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```sh
    python app.py
    ```

## API Endpoints

### Add a New Employee

- **URL**: `/employees`
- **Method**: `POST`
- **Payload**:
    ```json
    {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "job": "Developer",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "zip": "12345"
        },
        "skills": ["JavaScript", "React", "Node.js"],
        "age": 30
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "job": "Developer",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "zip": "12345"
        },
        "skills": ["JavaScript", "React", "Node.js"],
        "age": 30,
        "created_on": "2023-05-23T10:15:30Z"
    }
    ```

### Retrieve All Employees

- **URL**: `/employees`
- **Method**: `GET`
- **Response**:
    ```json
    [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "job": "Developer",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "zip": "12345"
            },
            "skills": ["JavaScript", "React", "Node.js"],
            "age": 30,
            "created_on": "2023-05-23T10:15:30Z"
        },
        ...
    ]
    ```

### Retrieve a Single Employee by ID

- **URL**: `/employees/<int:id>`
- **Method**: `GET`
- **Response**:
    ```json
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "job": "Developer",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "zip": "12345"
        },
        "skills": ["JavaScript", "React", "Node.js"],
        "age": 30,
        "created_on": "2023-05-23T10:15:30Z"
    }
    ```

### Update an Employee

- **URL**: `/employees/<int:id>`
- **Method**: `PUT`
- **Payload**:
    ```json
    {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "job": "Senior Developer",
        "address": {
            "street": "456 Elm St",
            "city": "Othertown",
            "zip": "67890"
        },
        "skills": ["Python", "Flask", "SQLAlchemy"],
        "age": 35
    }
    ```
- **Response**:
    ```json
    {
        "message": "Employee updated successfully"
    }
    ```

### Delete an Employee

- **URL**: `/employees/<int:id>`
- **Method**: `DELETE`
- **Response**:
    ```json
    {
        "message": "Employee deleted successfully"
    }
    ```

## External API Integration

When a new employee is added, their information is also sent to an external API (https://reqres.in/api/users) for additional processing.

## Running the Application

To run the application, simply execute:

```sh
python app.py
