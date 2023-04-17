# Projet SNCF : Lost in Translation

Ce projet est réalisé avec l'école Simplon. Le but de ce projet c'est qu'il permet d'analyser les données des objets trouvés dans les gares de la SNCF en France entre 2019 et 2022. Les données sont récupérées à partir de l'API Open Data de la SNCF et stockées dans une base de données SQLite. Différentes visualisations sont ensuite proposées pour explorer ces données.

## Fonctionnalités

**Mise à jour des données** : récupération des données des objets trouvés à partir de l'API de la SNCF pour une période donnée et stockage dans une base de données SQLite.

**Nombre d’objets trouvés en fonction de la température** : visualisation du nombre d’objets trouvés en fonction de la température à la date où ils ont été trouvés. Cette visualisation permet de voir s'il existe une corrélation entre la température et le nombre d’objets trouvés.

**Somme du nombre d’objets trouvés par semaine** : visualisation de la somme du nombre d’objets trouvés par semaine pour chaque année entre 2019 et 2022. Cette visualisation permet de voir si le nombre d’objets trouvés varie au fil des saisons.

**Carte de Paris avec le nombre d’objets trouvés en fonction de la fréquentation de voyageur de chaque gare** : visualisation du nombre d’objets trouvés pour chaque gare de Paris sur une carte de Paris. La taille des cercles sur la carte est proportionnelle au nombre d’objets trouvés et la couleur en fonction de la fréquentation de voyageurs de chaque gare.

**Nombre d'objets trouvés en fonction de la saison et de l'année** : visualisation du nombre d'objets trouvés en fonction de la saison et de l'année. Cette visualisation permet de voir si le nombre d'objets trouvés varie en fonction des saisons et des années.

**Nombre d'objets trouvés par saison, par type et par année** : visualisation du nombre d'objets trouvés par saison, par type et par année. Cette visualisation permet de voir s'il existe des différences dans les types d'objets trouvés en fonction des saisons et des années.

## Technologies utilisées

Python

SQLite

Streamlit

Pandas

Folium

Plotly

Seaborn

Matplotlib


## Installation

**Cloner le repository** : `git clone https://github.com/votre_nom/projet_sncf.git`

**Aller dans le dossier du projet** : `cd projet_sncf`

**Installer les dépendances** : `pip install -r requirements.txt`

**Lancer l'application** : `streamlit run app.py`

## Exemple d'utilisation

- Ouvrir l'application dans le navigateur

- Cliquer sur le bouton "Mise à jour des données" pour récupérer les données des objets trouvés à partir de l'API de la SNCF et les stocker dans une base de données SQLite

- Cliquer sur les différents onglets pour accéder aux différentes visualisations proposées

- Sélectionner les différentes options proposées pour afficher la visualisation souhaitée.


## Contributeurs

[@AgatheBecquart](https://github.com/AgatheBecquart)

[@neevaiti](https://github.com/neevaiti)


 ## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.