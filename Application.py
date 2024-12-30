import streamlit as st

# Titre principal
st.title("📊 Application de Visualisation de Données - Centre de Génie Industriel (CGI)")

# Introduction du projet
st.write("""
Bienvenue dans l'application de visualisation de données du **Centre de Génie Industriel (CGI)** d'IMT Mines Albi.

Le Centre de Génie Industriel est un laboratoire de recherche appliquée, spécialisé dans l'optimisation des systèmes industriels. Il s'intéresse à des domaines variés comme la gestion des ressources, l'optimisation des processus industriels et la mise en place de solutions technologiques pour l'industrie 4.0.

Cette application vous permet de découvrir et d'explorer des **publications et communications de congrès** réalisées par le CGI entre 2019 et 2024. Vous aurez accès à des visualisations interactives des résultats de ces travaux de recherche, permettant une analyse approfondie des données.
""")

# Section À propos / Fiche Technique
st.write("## 📋 À propos / Fiche Technique du CGI")
st.write("""
Le **Centre de Génie Industriel (CGI)** est un laboratoire de recherche et d'enseignement basé à **IMT Mines Albi**. Il s'engage activement dans des projets de recherche appliquée en partenariat avec des industriels et d'autres institutions académiques.

### 📌 **Domaines d'expertise :**
- Optimisation des systèmes de production et de logistique  
- Analyse et modélisation des systèmes complexes  
- Industrie 4.0 et transformation numérique des systèmes industriels  
- Gestion des ressources et durabilité industrielle  

### 🏢 **Infrastructure et Ressources :**
- Laboratoires de simulation et modélisation avancée  
- Outils d'analyse de données et intelligence artificielle  
- Plateformes collaboratives pour les projets industriels  

### 🤝 **Partenariats :**
- Collaborations avec des entreprises leaders dans le secteur industriel  
- Projets financés par des programmes de recherche européens et nationaux  

Pour plus d'informations, visitez le [site officiel d'IMT Mines Albi](https://www.imt-mines-albi.fr).
""")

# Objectifs de l'application
st.write("""
## 🎯 Objectifs de l'Application

L'objectif de cette application est de :

- Présenter des **publications scientifiques** publiées par le Centre de Génie Industriel entre 2019 et 2024.  
- Partager des **communications de congrès** concernant des thématiques en lien avec le génie industriel, l'optimisation des systèmes et l'innovation technologique.  
- Permettre une **exploration interactive** des données pour une meilleure compréhension des résultats scientifiques.  

Vous pouvez naviguer entre les différentes pages pour consulter les publications et communications.
""")

# Instructions de navigation
st.write("""
## 🧭 Navigation

Utilisez le menu sur le côté pour accéder aux sections suivantes :

- **Publications publiées entre 2019 et 2024** : Découvrez les publications scientifiques du CGI.  
- **Communications de congrès entre 2019 et 2024** : Explorez les communications de congrès réalisées par les chercheurs du CGI.  
""")

# Boutons interactifs
col1, col2 = st.columns(2)  # Diviser l'écran en 2 colonnes
# Initialiser la variable de navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'

# Fonction pour changer de page
def navigate_to(page):
    st.session_state['current_page'] = page
    st.rerun()
with col1:
    if st.button("### 📚 Voir Publications publiées entre 2019 et 2024"):
        st.switch_page("pages/1_Les publications publiées entre 2019 et 2024.py")

with col2:
    if st.button("### 📢 Voir Communications de congrès entre 2019 et 2024"):
        st.switch_page("pages/2_Les communications de congrès.py")

st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #f0f2f6;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            color: #6c757d;
            border-top: 1px solid #eaeaea;
        }
        .footer a {
            color: #6c757d;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="footer">
        <span>© 2024 Centre de Génie Industriel - IMT Mines Albi</span>
        <span>📍 <strong>Adresse :</strong> Campus Jarlard, 81013 Albi, France</span>
        <span>📞 <strong>Téléphone :</strong> +33 (0)5 63 49 30 00</span>
        <span>✉️ <strong>Email :</strong> <a href="mailto:contact@imt-mines-albi.fr">contact@imt-mines-albi.fr</a></span>
    </div>
""", unsafe_allow_html=True)