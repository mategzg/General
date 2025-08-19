from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'workers.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT,
                performance REAL,
                date TEXT
            )
        ''')
        conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    init_db()
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        performance = request.form['performance']
        date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO workers (name, role, performance, date) VALUES (?, ?, ?, ?)',
                      (name, role, performance, date))
            conn.commit()
        return redirect('/')

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT name, role, performance, date FROM workers')
        workers = c.fetchall()
    return render_template('index.html', workers=workers)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
