import sqlite3
import requests

# Connexion à la base de données SQLite et création de la table 'objets_trouves'
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

# Liste des gares à récupérer
gares = ["Paris Gare de Lyon", "Paris Montparnasse", "Paris Gare du Nord", 
         "Paris Saint-Lazare", "Paris Est", "Paris Austerlitz", "Paris Bercy"]

# Récupération des données de l'API pour chaque année et chaque gare
for year in range(2019, 2023):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    
    for gare in gares:
        # Construction de l'URL de l'API pour récupérer les données des objets trouvés pour une gare donnée et une année donnée
        url = f"https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=gc_obo_gare_origine_r_name+%3D+%22{gare}%22+AND+date%3E%3D%22{start_date}%22+AND+date%3C%3D%22{end_date}%22&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&timezone=Europe%2FParis&rows=-1"
        
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
