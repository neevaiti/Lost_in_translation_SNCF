import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sqlite3
import streamlit as st

conn = sqlite3.connect('../objets_trouves.db')
query = "SELECT * FROM objets_trouves"
df = pd.read_sql_query(query, conn)


# Convertir la colonne 'date' en objets datetime
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%dT%H:%M:%S%z', utc=True)

# Extraire la semaine et l'année de chaque date et stocker le résultat dans deux nouvelles colonnes 'year' et 'week'
df['year'] = df['date'].dt.year
df['week'] = df['date'].apply(lambda x: x.week)


result = df.groupby(['year', 'week', 'type']).count()['gare'].rename('nombre_objets')
result = result.to_frame()
result = result.reset_index()

# Créer une figure avec une colonne pour chaque année
fig = px.histogram(result, x='week', y='nombre_objets', nbins=150, color='type', title='Répartition du nombre d\'objets trouvés par semaine entre 2019 et 2022', facet_row='year')

# Mettre à jour les titres des axes
fig.update_xaxes(title_text='Semaine')
fig.update_yaxes(title_text='Nombre d\'objets')
fig.update_layout(height=1000)

# Afficher la figure
st.plotly_chart(fig)


conn.close()

