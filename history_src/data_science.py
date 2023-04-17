#!/usr/bin/env python
# coding: utf-8

# # Data Science

# In[230]:


import pandas as pd
import plotly.express as px
import sqlite3
import streamlit as st

# Charger les données des objets trouvés et des gares depuis la base de données SQLite
conn = sqlite3.connect('objets_trouves.db')
query_objets_trouves = "SELECT * FROM objets_trouves"
query_temperature = "SELECT * FROM temperature"
df_objets_trouves = pd.read_sql_query(query_objets_trouves, conn)
df_temperature = pd.read_sql_query(query_temperature, conn)


# In[231]:


df_objets_trouves['date'] = df_objets_trouves['date'].apply(lambda x: pd.to_datetime(x).date() if pd.notnull(x) else x)
df_temperature['date'] = df_temperature['date'].apply(lambda x: pd.to_datetime(x).date() if pd.notnull(x) else x)


# In[232]:


df_objets_trouves=df_objets_trouves.groupby(['date']).count()['gare'].rename('nombre_objets').to_frame().reset_index()


# In[233]:


df = pd.merge(df_objets_trouves, df_temperature, on='date')
df


# ## Afficher le nombre d’objets trouvés en fonction de la température sur un scatterplot. Est ce que le nombre d’objets perdus est corrélé à la temperature d'après ce graphique?

# In[234]:


# Création du scatterplot
fig = px.scatter(df, x='temperature', y='nombre_objets', 
                 title='Relation entre la température et le nombre d\'objets trouvés')
fig.show()


# Non, le nombre d'objets trouvés ne semble pas corrélé à la temperature selon ce graphique. Cependant pour avoir une idée définitive il faut prendre en compte la température et voir si pour un même nombre de personne il y a plus ou moins d'objets trouvés selon les saisons. 

# ## Quelle est la médiane du nombre d’objets trouvés en fonction de la saison? Il y a t il une correlation entre ces deux variables d'après le graphique?

# In[235]:


# Définir une fonction pour déterminer la saison en fonction du mois
def get_season(month):
    if month in [12, 1, 2]:
        return "hiver"
    elif month in [3, 4, 5]:
        return "printemps"
    elif month in [6, 7, 8]:
        return "été"
    else:
        return "automne"

# Ajouter une nouvelle colonne "saison" au dataframe
df["saison"] = pd.to_datetime(df["date"]).dt.month.apply(get_season)


# In[236]:


df


# In[237]:


df['année'] = pd.DatetimeIndex(df['date']).year


# In[238]:


df


# In[239]:


import seaborn as sns
import matplotlib.pyplot as plt

def plot_box(df, year):
    sub_df = df[df['année'] == year]
    # Création d'un box plot pour chaque saison
    sns.boxplot(x='saison', y='nombre_objets', data=sub_df)
    plt.title(f'Boxplot par saison pour {year}')
    plt.show()
    
plot_box(df, 2020)


# In[240]:


# Regrouper les données par saison et calculer la médiane
median_objets_trouves = df.groupby("saison")["nombre_objets"].median()

# Afficher les médianes
print("Médiane journalière du nombre d'objets trouvés par saison :")
print(median_objets_trouves)


# In[241]:


import seaborn as sns
import matplotlib.pyplot as plt

# Créer un graphique en barres avec Seaborn
sns.set_style("whitegrid")
plt.figure(figsize=(8, 6))
sns.barplot(x="saison", y="nombre_objets", data=df)
plt.title("Médiane journalière du nombre d'objets trouvés en fonction de la saison")
plt.xlabel("Saison")
plt.ylabel("Nombre d'objets trouvés")

plt.show()


# En ce qui concerne la corrélation entre ces deux variables, le graphique montre une légère tendance à une plus grande quantité d'objets trouvés en automne et en été, tandis que les quantités trouvées en hiver et au printemps sont plus faibles. Cependant, il n'y a pas de forte corrélation entre la saison et le nombre d'objets trouvés, car la variance des nombres d'objets trouvés à travers les différentes saisons est assez importante. Cela peut également être confirmé par le fait que la différence de médiane entre les saisons est relativement faible et très certainement lié à la fréquentation plus qu'à la saison.

# ## Affichez le nombre d'objets trouvés en fonction du type de d'objet et de la saison sur un graphique. Il y a t il une correlation entre ces deux variables d'après le graphique?

# In[242]:


df_objets_trouves = pd.read_sql_query(query_objets_trouves, conn)
df_objets_trouves['date'] = df_objets_trouves['date'].apply(lambda x: pd.to_datetime(x).date())
df = pd.merge(df_objets_trouves, df, on='date')


# In[243]:


df


# In[244]:


import matplotlib.pyplot as plt
import seaborn as sns

# Création d'un sous-ensemble de données pour chaque année
def plot_bar(df, year, object_type):
    sub_df = df[(df['année'] == year) & (df['type'] == object_type)]

    # Création d'un countplot pour chaque saison
    ax = sns.countplot(x='saison', data=sub_df)
    ax.set_title(f"Nombre d'objets trouvés de type '{object_type}' en {year} par saison")

    plt.show()

# Utilisation de la fonction pour afficher le graphique
plot_bar(df, 2022, 'Parapluies')


# In[245]:


df = df.groupby(['saison', 'type']).count()['gare'].rename('nombre_objets').to_frame().reset_index()
df


# In[246]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Créer la table pivot
table = pd.pivot_table(df, values='nombre_objets', index='type', columns='saison')
table


# In[247]:


# Créer le graphique à barres groupées
fig, ax = plt.subplots(figsize=(18, 18))
index = np.arange(len(table.index))
bar_width = 0.2
opacity = 0.8

for i, saison in enumerate(table.columns):
    ax.bar(index + i*bar_width, table[saison], bar_width, label=saison)

ax.set_xlabel('Objets')
ax.set_ylabel('Nombre d\'objets')
ax.set_title('Nombre d\'objets trouvés par saison et par type')
ax.set_xticks(index + bar_width*1.5)
ax.set_xticklabels(table.index, rotation=85)
ax.legend()

plt.tight_layout()
plt.show()


# Oui il y a une petite corrélation entre le type d'objet et la saison, les articles de camping sont le plus oubliés en été par exemple ou encore les lunettes en été également de par la présence des lunettes de soleil.
