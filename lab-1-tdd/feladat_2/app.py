import sqlite3
from flask import Flask, jsonify, request, g

app = Flask(__name__)
DATABASE = 'todos.db'

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # This allows accessing columns by name
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """
    Initializes the database by creating the necessary table.
    This function should be run from the command line once before
    starting the server for the first time: `python -c 'from app_persistent import init_db; init_db()'`
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return "Welcome"

@app.route('/todos', methods=['GET', 'POST'])
def get_db():
    db = get_db()
    cursor = d.cursor()

    if request.method == 'POST':
        task = request.json('task')
        cursor.execute('INSERT INTO todos (task, done) VALUES (?,?)', (task, False))
        db.commit()

        return "JSON", 201
    
    if request.method == 'GET':
        cursor.execute('SELECT * FROM todos')
        all_todos = [dict(row) for row in cursor.fetchall()]
        return jsonify(all_todos)