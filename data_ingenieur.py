import sqlite3
from datetime import datetime
import requests

conn = sqlite3.connect('objets_trouves.db')
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS objets_trouves(
        gare TEXT,
        type TEXT,
        nature TEXT,
        date TEXT
        )
''')

def update_objets_trouves(start_date, end_date):
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('objets_trouves.db')
    cursor = conn.cursor()
    
    # Nettoyer la table pour supprimer les données jusqu'à aujourd'hui
    cursor.execute("DELETE FROM objets_trouves")

    # Liste des gares à récupérer
    gares = ["Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", 
            "Paris Saint-Lazare", "Paris Est", "Paris Austerlitz", "Paris Bercy"]

    # Récupération des données de l'API pour chaque année et chaque gare
    for year in range(int(start_date[:4]), int(end_date[:4])+1):
        start_date_year = f"{year}-01-01"
        end_date_year = f"{year}-12-31"
        if year == int(start_date[:4]):
            start_date_year = start_date
        if year == int(end_date[:4]):
            end_date_year = end_date
            
        for gare in gares:
            # Construction de l'URL de l'API pour récupérer les données des objets trouvés pour une gare donnée et une année donnée
            url = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=gc_obo_gare_origine_r_name+%3D+%22{gare}%22+AND+date%3E%3D%22{start_date_year}%22+AND+date%3C%3D%22{end_date_year}%22&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&timezone=Europe%2FParis&rows=-1"

            # Envoi d'une requête à l'API et traitement de la réponse
            response = requests.get(url)

            if response.ok:
                data = response.json()
                records = data['records']
            else:
                print(f'Erreur lors de la requête pour la gare {gare} en {year} :', response.status_code)
                continue

            # Stockage des données dans la base de données
            for record in records:
                gare = record['fields']['gc_obo_gare_origine_r_name']
                type = record['fields']['gc_obo_type_c']
                nature = record['fields']['gc_obo_nature_c']
                date = record['fields']['date']
                cursor.execute("INSERT INTO objets_trouves VALUES (?, ?, ?, ?)", (gare, type, nature, date))

    # Enregistrement des changements dans la base de données et fermeture de la connexion
    conn.commit()
    conn.close()


update_objets_trouves("2019-01-01", "2022-12-31")

