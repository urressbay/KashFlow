from flask import Flask, jsonify, request
from sqlalchemy import create_engine

app = Flask(__name__)

# Define database connection string
engine = create_engine('mysql+pymysql://user:password@localhost/kashflow')

@app.route('/api/create-user', methods=['POST'])
def create_user():
    username = request.json['username']
    
    # Create user in SQL database
    conn = engine.connect()
    query = "INSERT INTO users (username) VALUES (:username)"
    conn.execute(query, {'username': username})
    conn.close()
    
    # Establish budget tracking table for new user
    query = "CREATE TABLE IF NOT EXISTS budgets_{0} (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), amount 
DECIMAL(10,2))"
    conn = engine.connect()
    conn.execute(query.format(username))
    conn.close()
    
    return jsonify({'message': 'User created successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
```
**`routes.py` (updated to include route for handling GET requests)**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/budgets/<username>', methods=['GET'])
def get_budgets(username):
    # Retrieve budgets from database
    conn = engine.connect()
    query = "SELECT * FROM budgets_{0}".format(username)
    results = conn.execute(query).fetchall()
    conn.close()
    
    return jsonify([{'id': row[0], 'name': row[1], 'amount': row[2]} for row in results])
