import sqlite3
import requests

# Création de la base de données
conn = sqlite3.connect('objets_trouves.db')
cursor = conn.cursor()

# Création de la table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS objets_trouves
    (gare TEXT, type TEXT, nature TEXT, date TEXT)
''')

# Récupération des données de l'API pour chaque année
for year in range(2019, 2023):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    url = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=gc_obo_gare_origine_r_name+%3D+%22Paris%22+AND+date%3E%3D%22{start_date}%22+AND+date%3C%3D%22{end_date}%22&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&timezone=Europe%2FParis&rows=10000"
    response = requests.get(url)

    if response.ok:
        data = response.json()
        records = data['records']
    else:
        print('Erreur lors de la requête :', response.status_code)
        continue

    # Stockage des données dans la base de données
    for record in records:
        gare = record['fields']['gc_obo_gare_origine_r_name']
        type = record['fields']['gc_obo_type_c']
        nature = record['fields']['gc_obo_nature_c']
        date = record['fields']['date']
        cursor.execute("INSERT INTO objets_trouves VALUES (?, ?, ?, ?)", (gare, type, nature, date))

# Enregistrement des changements
conn.commit()

# Fermeture de la connexion
conn.close()