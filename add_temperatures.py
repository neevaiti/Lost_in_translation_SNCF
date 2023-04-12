import requests
import sqlite3

# Créer la base de données SQLite
conn = sqlite3.connect("objets_trouves.db")
cursor = conn.cursor()

# Créer la table pour les données de température
cursor.execute("""
    CREATE TABLE IF NOT EXISTS temperature (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        temperature FLOAT NOT NULL
    )
""")

# Endpoint de l'API
URL = "https://public.opendatasoft.com/api/records/1.0/search/"
ressource = "?dataset=donnees-synop-essentielles-omm&q="
station = f"&refine.nom=ORLY"

# Définir les dates de début et de fin de la plage de données à récupérer
start_date = "2019-01-01"
end_date = "2022-12-31"

# Créer l'URL de l'API à partir des dates de début et de fin
date_fork = f"date%3A%5B{start_date}+TO+{end_date}%5D"
row_limit = "&rows=10000"
endpoint = URL + ressource + date_fork + row_limit + station

# Effectuer la requête GET à l'API
response = requests.get(endpoint)

# Calculer la moyenne des températures pour chaque jour
daily_temperatures = {}
for record in response.json()["records"]:
    date = record["fields"]["date"][:10]  # Extraire la date du format YYYY-MM-DD HH:MM:SS
    if "tc" not in record["fields"]:
        continue  # passer à l'itération suivante si la clé "tc" n'est pas présente
    temperature = record["fields"]["tc"]
    if date in daily_temperatures:
        daily_temperatures[date].append(temperature)
    else:
        daily_temperatures[date] = [temperature]


# Insérer les moyennes des températures dans la table SQLite
for date, temperatures in daily_temperatures.items():
    temperature_mean = sum(temperatures) / len(temperatures)
    cursor.execute("INSERT INTO temperature (date, temperature) VALUES (?, ?)", (date, temperature_mean))

# Enregistrer les modifications et fermer la connexion
conn.commit()
conn.close()
