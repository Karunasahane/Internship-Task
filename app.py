from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL configurations
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="karuna01",
    database="code_snippets"
)

@app.route('/', methods=['GET', 'POST'])
def submit_snippet():
    if request.method == 'POST':
        username = request.form['username']
        language = request.form['language']
        stdin = request.form['stdin']
        code = request.form['code']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor = db.cursor()
        query = "INSERT INTO snippets (username, language, stdin, code, timestamp) VALUES (%s, %s, %s, %s, %s)"
        values = (username, language, stdin, code, timestamp)
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect(url_for('snippets'))
    return render_template('index.html')

@app.route('/snippets')
def snippets():
    cursor = db.cursor()
    cursor.execute("SELECT username, language, stdin, code, timestamp FROM snippets")
    snippets = cursor.fetchall()
    cursor.close()
    return render_template('snippets.html', snippets=snippets)

if __name__ == '__main__':
    app.run(debug=True)