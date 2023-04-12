import pandas as pd
import sqlite3
import plotly.express as px
import streamlit as st

# Charger les données des objets trouvés et des gares depuis la base de données SQLite
conn = sqlite3.connect('../objets_trouves.db')
query_objets_trouves = "SELECT * FROM objets_trouves"
query_temperature = "SELECT * FROM temperature"
df_objets_trouves = pd.read_sql_query(query_objets_trouves, conn)
df_temperature = pd.read_sql_query(query_temperature, conn)

df_objets_trouves['date'] = df_objets_trouves['date'].apply(lambda x: pd.to_datetime(x).date() if pd.notnull(x) else x)
df_temperature['date'] = df_temperature['date'].apply(lambda x: pd.to_datetime(x).date() if pd.notnull(x) else x)

df_objets_trouves=df_objets_trouves.groupby(['date']).count()['gare'].rename('nombre_objets').to_frame().reset_index()

df = pd.merge(df_objets_trouves, df_temperature, on='date')

# Création du scatterplot
fig = px.scatter(df, x='temperature', y='nombre_objets', 
                 title='Relation entre la température et le nombre d\'objets trouvés')

# Affichage du graphique avec Streamlit
st.plotly_chart(fig)
