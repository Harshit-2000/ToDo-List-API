# wobot.ai Assignment

This is a simple REST API for creating, reading, updating and deleting todo items. It is built using FastAPI and SQLAlchemy, and includes user authentication.

## Features

- User authentication using JWT tokens.
- Adding, reading, updating and deleting todo items

## Setup

Clone the repo on your system using

```bash
git clone https://github.com/Harshit-2000/wobot.ai.git
```

Create a virtual environment

```bash
pip install virtualenv
python -m venv env
```

Activate a virtual env

```bash
.\env\script\activate
```

Installing Requirements

```bash
pip install -r requirements.txt
```

Setup a MySQL Server.

## Usage

Run the development server

```bash
uvicorn main:app --reload
```

## Endpoints

The API has the following endpoints:
- POST /signup: Sign up a new user
- POST /login: Login a user
- POST /todos: Create a new task
- GET /todos: Retrieve a list of tasks
- PUT /todos/{id}: Update an existing task
- DELETE /todos/{id}: Delete a task
