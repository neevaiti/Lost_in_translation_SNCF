import branca
import folium
import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


from streamlit_folium import folium_static


def scatterplot():
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

def histogram():
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

def map():
    # Connexion à la base de données
    connexion = sqlite3.connect("../objets_trouves.db")
    liste_types = pd.read_sql_query("""
        SELECT DISTINCT type 
        FROM objets_trouves
        """, connexion)

    liste_types = ["Tous"] + sorted(liste_types['type'].tolist())

    # Affichage de la carte avec Streamlit
    selected_year = st.selectbox("Sélectionnez l'année :", ['2019', '2020', '2021', '2022'])
    selected_object = st.selectbox("Sélectionnez un type d'objet", liste_types)

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

        # Calculer l'échelle pour la taille des icônes
        scale = np.log(df['nb_total_objets'].astype(float))
        scale_min, scale_max = scale.min(), scale.max()

        # Ajouter un marqueur pour chaque gare dans le DataFrame
        for index, row in df.iterrows():
            # Calculer la taille de l'icône en fonction du nombre d'objets trouvés
            normalized_size = (np.log(row['nb_total_objets']) - scale_min) / (scale_max - scale_min)
            marker_size = 5 + normalized_size * 50

            # Créer une icône personnalisée avec la couleur correspondant à la fréquentation de la gare
            marker_color = get_color(row['frequentation_gare'])
            icon_url = f"https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-{marker_color}.png"
            icon = folium.features.CustomIcon(icon_url, icon_size=(28, 45))

            # Ajouter le marqueur à la carte
            folium.Marker(
                location=(row['latitude'], row['longitude']),
                tooltip=row['gare']+ " - " + str(row['nb_total_objets']) + " objets trouvés",
                icon=icon,
                ).add_to(carte)

        # Ajouter une légende pour la fréquentation des gares
        colormap = branca.colormap.StepColormap(
            colors = ['green','yellow','orange','red'],
            vmin=df['frequentation_gare'].min(),
            vmax=df['frequentation_gare'].max(),
            index=[0,np.percentile(df['frequentation_gare'],25),np.percentile(df['frequentation_gare'],50),np.percentile(df['frequentation_gare'],75)],
            caption = 'Fréquentation de la gare'
        )
        carte.add_child(colormap)
        return folium_static(carte)


    df = requete(selected_year, selected_object)

    show_map(df)
        


def main():
    st.set_page_config(page_title='Brief SNCF - Lost in translation', page_icon=':bar_chart:')
    st.title('Brief SNCF - Lost in translation')

    tabs = ['Nombre d’objets trouvés en fonction de la température - Scatterplot', 'Somme du nombre d’objets trouvés par semaine - Histogramme', 'Carte de Paris avec le nombre d’objets trouvés en fonction de la fréquentation de voyageur de chaque gare - Carte']
    selected_tab = st.radio('Sélectionner un type de graphique', tabs)

    if selected_tab == 'Nombre d’objets trouvés en fonction de la température - Scatterplot':
        scatterplot()
    elif selected_tab == 'Somme du nombre d’objets trouvés par semaine - Histogramme':
        histogram()
    elif selected_tab == 'Carte de Paris avec le nombre d’objets trouvés en fonction de la fréquentation de voyageur de chaque gare - Carte':
        map()

if __name__ == '__main__':
    main()
