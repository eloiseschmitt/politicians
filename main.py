"""
First tests
"""
import datetime

import pandas as pd


class Politician:
    """
    Politician
    """
    def __init__(self, first_name: str, last_name: str, birthdate: datetime.date):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate


def retrieve_csv_data(conn, cursor):
    """Search for a csv file and create politician object"""
    csv_data = pd.read_csv(filepath_or_buffer="data_source/elus-deputes.csv", sep=";")
    politicians = []
    for _, row in csv_data.iterrows():
        politician = Politician(first_name=row["Nom de l'élu"], last_name=row["Prénom de l'élu"],
                                birthdate=row["Date de naissance"])
        politicians.append(politician)
        cursor.execute('''
            INSERT INTO Politician (first_name, last_name, birthdate) VALUES (?, ?, ?)
            ''', (politician.first_name, politician.last_name, politician.birthdate))

    # Valider (commit) les transactions
    conn.commit()

