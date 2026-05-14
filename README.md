# KashFlow
This is a budgeting app, that allows user to track budgets on a bi-weekly pay cycle.
**Project Structure:**

1. **`kashflow/`**: This directory will hold your Python application code.
	* `__init__.py`: An empty file that makes this directory a package.
	* `app.py`: The main entry point of your Python application, which will handle budget tracking logic.
	* `models.py`: Define database models for budgets using SQLAlchemy or another ORM library.
	* `schemas.py`: Define JSON schemas for API requests and responses using Marshmallow or another library.
	* `routes.py`: Define routes for your Flask application that interact with the database.
2. **`kashflow_db/`**: This directory will hold your MySQL database schema and data.

**Container Structure:**

1. **`kashflow/`**:
	* Python 3.x (e.g., python:3-alpine) as a service, running `python app.py`.
2. **`kashflow_db/`**:
	* MySQL (e.g., mysql:8) as a service, serving the KashFlow database.
3. **`nginx/`**:
	* Nginx (e.g., nginx:latest) as a service, proxying requests to your Python application.

**docker-compose.yml**
```yaml
version: '3'

services:
  app:
    build: ./kashflow
    environment:
      - DATABASE_URL=mysql://user:password@db/kashflow
    depends_on:
      - db

  db:
    image: mysql:8
    environment:
      - MYSQL_ROOT_PASSWORD=password
      - MYSQL_DATABASE=kashflow
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    depends_on:
      - app
```
**`kashflow/Dockerfile`**
```dockerfile
FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```
**`requirements.txt`** (example)
```markdown
Flask==2.0.1
SQLAlchemy==1.4.26
mysqlclient==1.4.6.post2
marshmallow==3.13.0
```
**Database Setup:**

Create the `kashflow` database and user in MySQL:
```sql
CREATE DATABASE kashflow;
GRANT ALL PRIVILEGES ON kashflow.* TO 'user'@'%' IDENTIFIED BY 'password';
```
In your Python application (`app.py`), import the necessary libraries, create a SQLAlchemy engine to connect to the 
database, and define models for budgets.

Here's some example code:
```python
from flask import Flask, jsonify
from marshmallow import Schema, fields
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

app = Flask(__name__)

Base = declarative_base()

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)

class Schema(BudgetSchema):
    class Meta:
        fields = ('id', 'name', 'amount')

@app.route('/budgets', methods=['GET'])
def get_budgets():
    budgets = Budget.query.all()
    return jsonify([schema.dump(b) for b in budgets])

if __name__ == '__main__':
    app.run(debug=True)
```
This code defines a `Budget` model, creates a SQLAlchemy engine to connect to the database, and defines a `/budgets` 
route that returns a JSON list of all budgets.

Note: This is just an example code snippet. You'll need to replace it with your actual application logic. Additionally, 
make sure to install any additional dependencies required by your application.
