import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Utiliser @st.cache_resource pour la mise en cache des données
@st.cache_resource
def load_data():
    return pd.read_csv('data/publications publiées entre 2019 et 2024.csv')

# Charger les données
df = load_data()

# Titre principal de la page
st.title("📈 Visualisation des publications publiées entre 2019 et 2024")

# Créer deux colonnes : une pour le premier graphique et l'autre pour le filtre
col1, col2 = st.columns([3, 1])

with col2:
    # Créer un slider pour sélectionner la plage d'années
    annees = st.select_slider('Sélectionnez la plage d\'années', options=list(range(2019, 2025)), value=(2019, 2024))

# Filtrer les données selon la plage d'années sélectionnée
annee_debut, annee_fin = annees
df_filtered = df[(df['Année'] >= annee_debut) & (df['Année'] <= annee_fin)]

with col1:
    # Calcul de la répartition des types de publications après le filtrage
    type_counts = df_filtered['Type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Nombre de publications']

    # Création du graphique avec Plotly
    fig1 = px.bar(type_counts, x='Type', y='Nombre de publications', 
                  title=f"Répartition des types de publications ({annee_debut} - {annee_fin})",
                  labels={'Type': 'Type de publication', 'Nombre de publications': 'Nombre de publications'},
                  color='Type', color_discrete_sequence=px.colors.sequential.Viridis)

    # Affichage du premier graphique dans Streamlit
    st.plotly_chart(fig1)

# Calcul du cumul des publications par type et année
df_grouped = df_filtered.groupby(['Année', 'Type']).size().reset_index(name='Nombre de publications')

# Calcul du cumul des publications par type
df_grouped['Nombre de publications cumulées'] = df_grouped.groupby('Type')['Nombre de publications'].cumsum()

# Créer deux colonnes pour afficher les graphiques côte à côte
col3, col4 = st.columns([2, 1])

# Afficher le graphique cumulatif dans la première colonne
with col3:
    st.subheader(f"Évolution cumulée des publications de {annee_debut} à {annee_fin}")
    fig2 = px.line(df_grouped, x="Année", y="Nombre de publications cumulées", color="Type", 
                   title=f"Évolution cumulée des publications par type ({annee_debut} - {annee_fin})", 
                   labels={'Année': 'Année', 'Nombre de publications cumulées': 'Nombre de publications cumulées'})

    # Mettre à jour les axes pour personnaliser les graduations
    fig2.update_xaxes(dtick=1, tickformat="%Y")

    # Affichage du graphique cumulatif dans Streamlit
    st.plotly_chart(fig2)

# Afficher le graphique en camembert de la répartition des langues dans la deuxième colonne
with col4:
    st.subheader("Répartition des langues des publications")
    langue_counts = df_filtered['Langue'].value_counts()

    # Création du graphique en camembert (pie chart) avec Plotly
    fig3 = px.pie(langue_counts, names=langue_counts.index, values=langue_counts, 
                  title='Répartition des langues des publications', 
                  color_discrete_sequence=px.colors.sequential.Plasma)

    # Affichage du graphique de répartition des langues
    st.plotly_chart(fig3)

# Assurez-vous que la colonne 'Date' est bien au format datetime
# Fonction pour traiter les différents formats de dates

def parse_date(date_str):
    if pd.isna(date_str):  # Si la valeur est NaN (NaT), la laisser telle quelle
        return pd.NaT
    
    # Si la valeur est déjà un Timestamp (datetime), la laisser telle quelle
    if isinstance(date_str, pd.Timestamp):
        return date_str
    
    # Vérifier si la date est une chaîne de caractères avant de tenter de la traiter
    if isinstance(date_str, str):
        if len(date_str) == 4 and date_str.isdigit():  # Cas de l'année seule
            return pd.to_datetime(date_str + "-01-01")
        
        # Si la date est au format année-mois (exemple "2020-11"), ajouter le 1er jour du mois
        if len(date_str) == 7 and date_str[4] == '-' and date_str[:4].isdigit() and date_str[5:].isdigit():
            return pd.to_datetime(date_str + "-01")
        
        # Si la date est déjà complète (exemple "05/07/2022"), tenter de la convertir
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT  # Si la conversion échoue, renvoyer NaT
    else:
        return pd.NaT  # Si ce n'est pas une chaîne ou un Timestamp valide, retourner NaT

# Appliquer la fonction à la colonne 'Date'
df_filtered['Date'] = df_filtered['Date'].apply(parse_date)

# Vérifier que la colonne 'Date' est correctement convertie en datetime
#if df_filtered['Date'].isnull().any():
 #   st.warning("Certaines dates sont mal formatées ou manquantes.")

# Ajouter une colonne 'Année' pour référence
df_filtered['Année'] = df_filtered['Date'].dt.year

# Interface Streamlit
st.title("Évolution cumulée des publications par famille au fil du temps")
# **Filtre sur les familles**  
familles_uniques = df_filtered['Famille'].unique().tolist()
famille_selectionnee = st.multiselect(
    'Sélectionnez les familles à afficher :',
    options=familles_uniques,
    default=familles_uniques  # Par défaut, toutes les familles sont sélectionnées
)

# Appliquer le filtre sur les familles sélectionnées
if famille_selectionnee:
    df_filtered = df_filtered[df_filtered['Famille'].isin(famille_selectionnee)]

# Calculer le nombre de publications par famille et date
df_grouped_famille = df_filtered.groupby(['Date', 'Famille']).size().reset_index(name='Nombre de publications')

# Calculer le nombre de publications cumulées par famille
df_grouped_famille['Nombre de publications cumulées'] = df_grouped_famille.groupby('Famille')['Nombre de publications'].cumsum()

# Créer un graphique de l'évolution cumulée des publications par famille
fig5 = px.line(
    df_grouped_famille, 
    x="Date",  # Utiliser la date pour l'axe X
    y="Nombre de publications cumulées",  # Nombre de publications cumulées pour l'axe Y
    color="Famille",  # Séparer par famille
    title="Évolution cumulée des publications par famille au fil du temps",
    labels={'Date': 'Date', 'Nombre de publications cumulées': 'Nombre de publications cumulées'}
)

# Personnalisation des axes
fig5.update_xaxes(
    tickformat="%Y-%m-%d",  # Afficher les dates au format AAAA-MM-JJ
    title="Date"
)

# Affichage du graphique cumulatif dans Streamlit
st.plotly_chart(fig5)

# Calcul de la répartition des publications par famille
famille_counts = df_filtered['Famille'].value_counts().reset_index()
famille_counts.columns = ['Famille', 'Nombre de publications']

# Création du graphique de répartition des publications par famille
fig4 = px.bar(famille_counts, x='Famille', y='Nombre de publications',
              title="Répartition des publications par famille",
              labels={'Famille': 'Famille', 'Nombre de publications': 'Nombre de publications'},
              color='Famille', color_discrete_sequence=px.colors.sequential.Viridis)

# Affichage du graphique dans Streamlit
st.plotly_chart(fig4)

# ------------------------ Word Cloud ------------------------
st.subheader("🌐 Nuage de mots (Word Cloud) des mots-clés")
# Extraire les mots-clés de la colonne 'Mots_clés' et les joindre en une seule chaîne
mots_cles = ' '.join(df['Mots_clés'].dropna().astype(str))

# Créer un WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(mots_cles)

# Afficher le WordCloud avec matplotlib
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

# ------------------------ Parallel Categories ------------------------
# Ajoutez une colonne 'size' avec les occurrences des combinaisons uniques
df_filtered['size'] = df_filtered.groupby(['Famille', 'Type', 'Année'])['Famille'].transform('count')

# Créez un dictionnaire de couleurs pour chaque Famille
palette = px.colors.qualitative.Set2  # Palette de couleurs attrayante
unique_familles = df_filtered['Famille'].unique()
color_map = {famille: palette[i % len(palette)] for i, famille in enumerate(unique_familles)}

# Ajoutez une colonne 'color' correspondant à la couleur de chaque 'Famille'
df_filtered['color'] = df_filtered['Famille'].map(color_map)

# Créez le graphique avec des couleurs cohérentes
fig = px.parallel_categories(
    df_filtered,
    dimensions=['Famille', 'Année', 'Type'],
    color='color',  # Utilisez la colonne 'color' pour appliquer les couleurs
    color_continuous_scale=px.colors.sequential.Inferno
)

# Mise à jour de la mise en page pour cacher la barre de couleur
fig.update_layout(
    title_text="Diagramme Parallel Categories : Famille → Type → Année",
    title_font=dict(size=18, color='rgb(0, 0, 0)', family='Arial, sans-serif'),  # Police du titre plus claire
    font=dict(size=14, color='rgb(0, 0, 0)', family='Arial, sans-serif'),  # Police des autres textes claire
    width=2000,  # Augmenter la largeur
    height=900,  # Augmenter la hauteur
    coloraxis_showscale=False,  # Cache l'échelle de couleur
    plot_bgcolor='rgb(255, 255, 255)',  # Fond blanc pour plus de clarté
    paper_bgcolor='rgb(255, 255, 255)',  # Fond blanc de la page
    margin=dict(t=40, b=40, l=200, r=20)
)

# Afficher le graphique Parallel Categories dans Streamlit
st.plotly_chart(fig)

import pandas as pd
import plotly.express as px
import streamlit as st

# Définir la fonction pour analyser les dates
def parse_date(date_str):
    if pd.isna(date_str):  # Si la valeur est NaN (NaT), la laisser telle quelle
        return pd.NaT
    
    # Si la valeur est déjà un Timestamp (datetime), la laisser telle quelle
    if isinstance(date_str, pd.Timestamp):
        return date_str
    
    # Vérifier si la date est une chaîne de caractères avant de tenter de la traiter
    if isinstance(date_str, str):
        if len(date_str) == 4 and date_str.isdigit():  # Cas de l'année seule
            return pd.to_datetime(date_str + "-01-01")
        
        # Si la date est au format année-mois (exemple "2020-11"), ajouter le 1er jour du mois
        if len(date_str) == 7 and date_str[4] == '-' and date_str[:4].isdigit() and date_str[5:].isdigit():
            return pd.to_datetime(date_str + "-01")
        
        # Si la date est déjà complète (exemple "05/07/2022"), tenter de la convertir
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT  # Si la conversion échoue, renvoyer NaT
    else:
        return pd.NaT  # Si ce n'est pas une chaîne ou un Timestamp valide, retourner NaT

# Appliquer la fonction à la colonne 'Date'
df['Date'] = df['Date'].apply(parse_date)

# Créer une liste vide pour stocker les données
data = []

# Exemple : Parcourir chaque ligne et récupérer les auteurs et les dates
for _, row in df.iterrows():
    auteurs_split = row['Auteurs'].split(',')  # Séparer les auteurs (assumé format "Nom, Prénom")
    for i in range(0, len(auteurs_split), 2):  # Nom et Prénom alternent
        prenom = auteurs_split[i].strip()
        nom = auteurs_split[i+1].strip() if i + 1 < len(auteurs_split) else ""
        auteur = f"{nom} {prenom}"
        date = row['Date']
        data.append([auteur, date])

# Convertir en DataFrame
df_auteurs = pd.DataFrame(data, columns=['Auteur', 'Date'])

# Groupement par Auteur et Date pour compter les occurrences par auteur et par date
df_grouped = df_auteurs.groupby(['Auteur', 'Date']).size().reset_index(name='Nombre de publications')

# Calculer le nombre cumulatif de publications par auteur
df_grouped['Nombre de publications cumulées'] = df_grouped.groupby('Auteur')['Nombre de publications'].cumsum()

# Trouver les 10 auteurs les plus fréquents en fonction du nombre total de publications
top_10_auteurs = df_grouped.groupby('Auteur')['Nombre de publications'].sum().nlargest(10).index

# Filtrer les données pour ne conserver que les 10 auteurs les plus fréquents
df_top_10 = df_grouped[df_grouped['Auteur'].isin(top_10_auteurs)]
st.title("Analyse de l'évolution cumulée des publications selon les auteurs")
# Ajouter une barre de défilement pour choisir le nombre d'auteurs
number_of_authors = st.slider(
    "Sélectionner le nombre d'auteurs",
    min_value=1,
    max_value=7,  # Ajustez selon vos besoins
    value=5  # Valeur par défaut
)

# Trouver les auteurs les plus fréquents en fonction du nombre sélectionné
top_auteurs_limit = df_grouped.groupby('Auteur')['Nombre de publications'].sum().nlargest(number_of_authors).index

# Filtrer les données en fonction du nombre d'auteurs sélectionnés
df_selected_authors = df_grouped[df_grouped['Auteur'].isin(top_auteurs_limit)]

# Créer un graphique avec Plotly pour l'évolution cumulée des publications par auteur au fil du temps
fig = px.line(
    df_selected_authors, 
    x="Date",  # Utiliser la date pour l'axe X
    y="Nombre de publications cumulées",  # Nombre de publications cumulées pour l'axe Y
    color="Auteur",  # Séparer par auteur
    title="Évolution cumulée des publications des auteurs au fil du temps",
    labels={'Date': 'Date', 'Nombre de publications cumulées': 'Nombre de publications cumulées'}
)

# Personnalisation des axes
fig.update_xaxes(
    tickformat="%Y-%m-%d",  # Afficher les dates au format AAAA-MM-JJ
    title="Date"
)

# Afficher le graphique
st.plotly_chart(fig)






import pandas as pd
import plotly.express as px
import streamlit as st

# Définir la fonction pour analyser les dates
def parse_date(date_str):
    if pd.isna(date_str):  # Si la valeur est NaN (NaT), la laisser telle quelle
        return pd.NaT
    
    # Si la valeur est déjà un Timestamp (datetime), la laisser telle quelle
    if isinstance(date_str, pd.Timestamp):
        return date_str
    
    # Vérifier si la date est une chaîne de caractères avant de tenter de la traiter
    if isinstance(date_str, str):
        if len(date_str) == 4 and date_str.isdigit():  # Cas de l'année seule
            return pd.to_datetime(date_str + "-01-01")
        
        # Si la date est au format année-mois (exemple "2020-11"), ajouter le 1er jour du mois
        if len(date_str) == 7 and date_str[4] == '-' and date_str[:4].isdigit() and date_str[5:].isdigit():
            return pd.to_datetime(date_str + "-01")
        
        # Si la date est déjà complète (exemple "05/07/2022"), tenter de la convertir
        try:
            return pd.to_datetime(date_str, dayfirst=True)
        except:
            return pd.NaT  # Si la conversion échoue, renvoyer NaT
    else:
        return pd.NaT  # Si ce n'est pas une chaîne ou un Timestamp valide, retourner NaT

# Appliquer la fonction à la colonne 'Date'
df['Date'] = df['Date'].apply(parse_date)

# Créer une liste vide pour stocker les données
data = []

# Exemple : Parcourir chaque ligne et récupérer les lieux et les dates
for _, row in df.iterrows():
    lieux_split = row['Lieu'].split(',')  # Séparer les lieux (assumé format "Lieu1, Lieu2, ...")
    for lieu in lieux_split:  # Parcourir chaque lieu séparé
        lieu = lieu.strip()  # Nettoyer l'espace
        date = row['Date']
        data.append([lieu, date])

# Convertir en DataFrame
df_lieux = pd.DataFrame(data, columns=['Lieu', 'Date'])

# Groupement par Lieu et Date pour compter les occurrences par lieu et par date
df_grouped = df_lieux.groupby(['Lieu', 'Date']).size().reset_index(name='Nombre de publications')

# Calculer le nombre cumulatif de publications par lieu
df_grouped['Nombre de publications cumulées'] = df_grouped.groupby('Lieu')['Nombre de publications'].cumsum()

# Trouver les 10 lieux les plus fréquents en fonction du nombre total de publications
top_10_lieux = df_grouped.groupby('Lieu')['Nombre de publications'].sum().nlargest(10).index

# Filtrer les données pour ne conserver que les 10 lieux les plus fréquents
df_top_10 = df_grouped[df_grouped['Lieu'].isin(top_10_lieux)]

# Titre de la section avec Streamlit
st.title("Analyse de l'évolution cumulée des publications selon les lieux")

# Ajouter une barre de défilement pour choisir le nombre de lieux
number_of_places = st.slider(
    "Sélectionner le nombre de lieux",
    min_value=1,
    max_value=7,  # Ajustez selon vos besoins
    value=5  # Valeur par défaut
)

# Trouver les lieux les plus fréquents en fonction du nombre sélectionné
top_lieux_limit = df_grouped.groupby('Lieu')['Nombre de publications'].sum().nlargest(number_of_places).index

# Filtrer les données en fonction du nombre de lieux sélectionnés
df_selected_places = df_grouped[df_grouped['Lieu'].isin(top_lieux_limit)]

# Créer un graphique avec Plotly pour l'évolution cumulée des publications par lieu au fil du temps
fig = px.line(
    df_selected_places, 
    x="Date",  # Utiliser la date pour l'axe X
    y="Nombre de publications cumulées",  # Nombre de publications cumulées pour l'axe Y
    color="Lieu",  # Séparer par lieu
    title="Évolution cumulée des publications des lieux au fil du temps",
    labels={'Date': 'Date', 'Nombre de publications cumulées': 'Nombre de publications cumulées'},
    width=5000,  # Largeur du graphique
    height=450   # Hauteur du graphique
)

# Personnalisation des axes
fig.update_xaxes(
    tickformat="%Y-%m-%d",  # Afficher les dates au format AAAA-MM-JJ
    title="Date"
)

# Afficher le graphique
st.plotly_chart(fig)

if st.button("⬅️ Retour à l'accueil"):
    st.switch_page("Application.py")



