import branca
import folium
import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from streamlit_folium import folium_static


def scatterplot():
    """Afficher un scatterplot avec la température et le nombre d'objets trouvés"""
    
    conn = sqlite3.connect('objets_trouves.db')
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
    """Afficher un histogramme avec le nombre d'objets trouvés par semaine"""
    
    conn = sqlite3.connect('objets_trouves.db')
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


 
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def boxplot_number_objects_per_season():
    def get_season(month):
        if month in [12, 1, 2]:
            return "hiver"
        elif month in [3, 4, 5]:
            return "printemps"
        elif month in [6, 7, 8]:
            return "été"
        else:
            return "automne"
    
    conn = sqlite3.connect('objets_trouves.db')
    query_objets_trouves = "SELECT * FROM objets_trouves"
    df = pd.read_sql_query(query_objets_trouves, conn)

    df['date'] = df['date'].apply(lambda x: pd.to_datetime(x).date() if pd.notnull(x) else x)
    df = df.groupby(['date']).count()['gare'].rename('nombre_objets').to_frame().reset_index()

    # Convertir la colonne 'date' en type datetime et ajouter une colonne pour la saison
    df["saison"] = pd.to_datetime(df["date"]).dt.month.apply(get_season)
    df['année'] = pd.DatetimeIndex(df['date']).year

    def plot_box(df, year):
        sub_df = df[df['année'] == year]
        # Création d'un box plot pour chaque saison
        fig, ax = plt.subplots()
        sns.boxplot(x='saison', y='nombre_objets', data=sub_df)
        plt.title(f'Boxplot par saison pour {year}')
        st.pyplot(fig)
        
    # Création du sélecteur d'année
    year = st.selectbox('Sélectionnez une année', df['année'].unique())

    # Appel de la fonction plot_box avec l'année sélectionnée
    plot_box(df, year)
    st.set_option('deprecation.showPyplotGlobalUse', False)



import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def barplot_type_season():
    
    def get_season(month):
        if month in [12, 1, 2]:
            return "hiver"
        elif month in [3, 4, 5]:
            return "printemps"
        elif month in [6, 7, 8]:
            return "été"
        else:
            return "automne"
    
    # Charger les données depuis la base de données SQLite   
    conn = sqlite3.connect('objets_trouves.db')
    query_objets_trouves = "SELECT * FROM objets_trouves"
    df = pd.read_sql_query(query_objets_trouves, conn)

    df['date'] = df['date'].apply(lambda x: pd.to_datetime(x).date() if pd.notnull(x) else x)
    df = df.groupby(['date']).count()['gare'].rename('nombre_objets').to_frame().reset_index()

    # Convertir la colonne 'date' en type datetime et ajouter une colonne pour la saison
    df["saison"] = pd.to_datetime(df["date"]).dt.month.apply(get_season)
    df['année'] = pd.DatetimeIndex(df['date']).year
    query_objets_trouves = "SELECT * FROM objets_trouves"
    df_objets_trouves = pd.read_sql_query(query_objets_trouves, conn)
    df_objets_trouves['date'] = df_objets_trouves['date'].apply(lambda x: pd.to_datetime(x).date())
    df = pd.merge(df_objets_trouves, df, on='date')

    # Création d'un sous-ensemble de données pour chaque année
    def plot_bar(df, year, object_type):
        sub_df = df[(df['année'] == year) & (df['type'] == object_type)]

        # Création d'un countplot pour chaque saison
        fig, ax = plt.subplots()
        sns.countplot(x='saison', data=sub_df, ax=ax)
        ax.set_title(f"Nombre d'objets trouvés de type '{object_type}' en {year} par saison")

        st.pyplot(fig)

    # Créer une liste de toutes les années et tous les types d'objets disponibles dans le dataframe
    annees = sorted(df['année'].unique())
    types_objets = sorted(df['type'].unique())

    # Sélecteur de l'année et du type d'objet
    year_selected = st.selectbox("Sélectionner une année :", options=annees)
    object_selected = st.selectbox("Sélectionner un type d'objet :", options=types_objets)
    
    plot_bar(df, year_selected, object_selected)


def map():
    """Afficher une carte avec les gares et les objets trouvés"""
    
    # Connexion à la base de données
    connexion = sqlite3.connect('objets_trouves.db')
    liste_types = pd.read_sql_query("""
        SELECT DISTINCT type 
        FROM objets_trouves
        """, connexion)

    liste_types = ["Tous"] + sorted(liste_types['type'].tolist())

    # Affichage de la carte avec Streamlit
    selected_year = st.selectbox("Sélectionnez l'année :", ['2019', '2020', '2021', '2022'])
    selected_object = st.selectbox("Sélectionnez un type d'objet", liste_types)

    def requete(selected_year, selected_object):
        """Requête SQL pour récupérer les données des gares et des objets trouvés"""
        
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
        """Fonction qui retourne la couleur en fonction de la fréquentation de la gare"""
        
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
        """Fonction qui affiche la carte"""
        
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
    """Fonction principale du script Streamlit"""
    
    st.set_page_config(page_title='Brief SNCF - Lost in translation', page_icon=':bar_chart:')
    st.title('Brief SNCF - Lost in translation')

    tabs = ['Nombre d’objets trouvés en fonction de la température - Scatterplot', 'Somme du nombre d’objets trouvés par semaine - Histogramme', 'Carte de Paris avec le nombre d’objets trouvés en fonction de la fréquentation de voyageur de chaque gare - Carte', "Nombre d'objets trouvés en fonction de la saison et de l'année - Boxplot", "Nombre d\'objets trouvés par saison, par type et par année - Barplot", "Réponses aux questions/Analyse"]
    selected_tab = st.radio('Sélectionner un type de graphique', tabs)

    if selected_tab == 'Nombre d’objets trouvés en fonction de la température - Scatterplot':
        scatterplot()
    elif selected_tab == 'Somme du nombre d’objets trouvés par semaine - Histogramme':
        histogram()
    elif selected_tab == "Nombre d'objets trouvés en fonction de la saison et de l'année - Boxplot":
        boxplot_number_objects_per_season()
    elif selected_tab == "Nombre d\'objets trouvés par saison, par type et par année - Barplot":
        barplot_type_season()
    elif selected_tab == 'Carte de Paris avec le nombre d’objets trouvés en fonction de la fréquentation de voyageur de chaque gare - Carte':
        map()
    elif selected_tab == "Réponses aux questions/Analyse":
        st.write("**Est ce que le nombre d’objets perdus est corrélé à la temperature d'après le scatterplot?**")
        st.write("Non, le nombre d'objets trouvés ne semble pas corrélé à la temperature selon ce graphique.")
        st.write(" ")
        st.write("**Quelle est la médiane du nombre d’objets trouvés en fonction de la saison? Il y a t il une correlation entre ces deux variables d'après le graphique?**")
        st.write("En ce qui concerne la corrélation entre ces deux variables, le graphique montre une légère tendance à une plus grande quantité d'objets trouvés en automne et en été, tandis que les quantités trouvées en hiver et au printemps sont plus faibles. Cependant, il n'y a pas de forte corrélation entre la saison et le nombre d'objets trouvés, car la variance des nombres d'objets trouvés à travers les différentes saisons est assez importante. Cela peut également être confirmé par le fait que la différence de médiane entre les saisons est relativement faible et très certainement lié à la fréquentation plus qu'à la saison.")
        st.write(" ")
        st.write("**Affichez le nombre d'objets trouvés en fonction du type de d'objet et de la saison sur un graphique. Il y a t il une correlation entre ces deux variables d'après le graphique?**")
        st.write("Oui il y a une petite corrélation entre le type d'objet et la saison, les articles de camping sont le plus oubliés en été par exemple ou encore les lunettes en été également de par la présence des lunettes de soleil.")
        st.write(" ")

if __name__ == '__main__':
    main()
