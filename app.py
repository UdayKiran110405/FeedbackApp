from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    message TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feedback', methods=['POST'])
def feedback():
    name = request.form['name']
    email = request.form['email']
    rating = request.form['rating']
    message = request.form['message']

    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('INSERT INTO feedback (name, email, rating, message) VALUES (?, ?, ?, ?)',
              (name, email, rating, message))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()
    c.execute('SELECT * FROM feedback')
    data = c.fetchall()
    conn.close()
    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
