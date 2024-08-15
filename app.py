"""
App index
"""
import sqlite3

from flask import Flask, render_template, request

from main import retrieve_csv_data

app = Flask(__name__)


@app.route('/')
def index():
    """Index route"""
    search_term = request.args.get('search', '')

    # Connexion à la base de données SQLite
    conn = sqlite3.connect('politicians.db')
    cursor = conn.cursor()
    # Création de la table Politician
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Politician (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birthdate DATE NOT NULL
    )
    ''')
    retrieve_csv_data(conn, cursor)

    # Construire la requête SQL avec un filtre si un terme de recherche est fourni
    if search_term:
        cursor.execute('''
        SELECT first_name, last_name, birthdate FROM Politician
        WHERE first_name LIKE ? OR last_name LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%'))
    else:
        cursor.execute('SELECT first_name, last_name, birthdate FROM Politician')

    politicians = cursor.fetchall()

    # Fermer la connexion
    conn.close()

    return render_template('index.html', politicians=politicians)


if __name__ == '__main__':
    app.run(debug=True)
