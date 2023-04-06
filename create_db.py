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

# Récupération des données de l'API
url = 'https://ressources.data.sncf.com/api/records/1.0/search/'
params = {'dataset': 'objets-trouves-restitution',
          'rows': 1000,
          'refine.gc_obo_gare_origine_r_name': 'Paris',
          'refine.date': '2019-01-01+TO+2022-12-31'}
response = requests.get(url, params=params)
data = response.json()

# Stockage des données dans la base de données
for record in data['records']:
    gare = record['fields']['gc_obo_gare_origine_r_name']
    type = record['fields']['gc_obo_type_c']
    nature = record['fields']['gc_obo_nature_c']
    date = record['fields']['date']
    cursor.execute("INSERT INTO objets_trouves VALUES (?, ?, ?, ?)", (gare, type, nature, date))

# Enregistrement des changements
conn.commit()

# Fermeture de la connexion
conn.close()
