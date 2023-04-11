import folium
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import branca
from streamlit_folium import folium_static

# Connexion à la base de données
connexion = sqlite3.connect("../objets_trouves.db")

def requete(selected_year, selected_object):
    if selected_object == "Tous":
        df = pd.read_sql_query(f"""SELECT gare, latitude, longitude, COUNT (*) AS nb_total_objets,
                                        SUM(frequentation_{selected_year}) AS frequentation_gare
                                FROM objets_trouves 
                                JOIN gares ON objets_trouves.gare = gares.nom_des_gares
                                WHERE objets_trouves.date LIKE "{selected_year}%"
                                GROUP BY gare
                            """, connexion)
    else : 
        df = pd.read_sql_query(f"""SELECT gare, latitude, longitude, COUNT (*) AS nb_total_objets,
                                        frequentation_{selected_year} AS frequentation_gare
                                FROM objets_trouves 
                                JOIN gares ON objets_trouves.gare = gares.nom_des_gares
                                WHERE type = "{selected_object}" AND objets_trouves.date LIKE "{selected_year}%"
                                GROUP BY gare
                            """, connexion)
    return df


def get_color(frequentation):
    df = requete(selected_year, selected_object)
    if frequentation < np.percentile(df['frequentation_gare'],25):
        return "green"
    elif frequentation < np.percentile(df['frequentation_gare'],50):
        return "yellow"
    elif frequentation < np.percentile(df['frequentation_gare'],75):
        return "orange"
    else :
        return "red"

def show_map(df):
    carte = folium.Map(location=[48.864716, 2.349014], zoom_start=12)
    scale = np.log(df['nb_total_objets'].astype(float))
    scale_min, scale_max = scale.min(), scale.max()
    for index, row in df.iterrows():
        normalized_size = (np.log(row['nb_total_objets']) - scale_min) / (scale_max - scale_min)
        taille_marqueur = 5 + normalized_size * 50
        folium.CircleMarker(location=(row['latitude'], row['longitude']),
                    tooltip=row['gare']+ " - " + str(row['nb_total_objets']) + " objets trouvés",
                    icon=folium.Icon(icon='train', prefix='fa'),
                    radius=taille_marqueur,
                    color = get_color(row['frequentation_gare'])
                    ).add_to(carte)
    
    colormap = branca.colormap.StepColormap(
    colors = ['green','yellow','orange','red'],
    vmin=df['frequentation_gare'].min(),
    vmax=df['frequentation_gare'].max(),
    index=[0,np.percentile(df['frequentation_gare'],25),np.percentile(df['frequentation_gare'],50),np.percentile(df['frequentation_gare'],75)],
    caption = 'Fréquentation de la gare')

    carte.add_child(colormap)  
    
    return folium_static(carte)




liste_types = pd.read_sql_query("""
SELECT DISTINCT type 
FROM objets_trouves
""", connexion)

liste_types = ["Tous"] + sorted(liste_types['type'].tolist())

# Affichage de la carte avec Streamlit
selected_year = st.selectbox("Sélectionnez l'année :", ['2019', '2020', '2021', '2022'])
selected_object = st.selectbox("Sélectionnez un type d'objet", liste_types)

df = requete(selected_year, selected_object)

show_map(df)