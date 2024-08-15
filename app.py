from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# Route principale pour afficher les données
@app.route('/')
def index():
    # Récupérer le terme de recherche depuis la requête GET
    search_term = request.args.get('search', '')

    # Connexion à la base de données SQLite
    conn = sqlite3.connect('politicians.db')
    cursor = conn.cursor()

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

    # Rendre le template HTML avec les données
    return render_template('index.html', politicians=politicians)


if __name__ == '__main__':
    app.run(debug=True)
