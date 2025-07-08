import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Conclusion - Analyse des ventes de jeux vidéo",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.markdown("# ✅ **Conclusion du projet d’analyse des ventes de jeux vidéo**")
st.markdown("---")

# 🎯 Objectif du projet
st.markdown("### 🎯 Objectif du projet")
st.markdown("""
L’objectif de ce projet était **d’explorer, analyser et interpréter les données de ventes de jeux vidéo dans le monde**, à partir d’un dataset issu de [vgchartz.com](https://www.vgchartz.com/).

Nous ne cherchions pas uniquement à vérifier des hypothèses, mais avant tout à :
- **Comprendre la structure du marché du jeu vidéo** (répartition géographique, préférences culturelles, genres dominants).
- **Utiliser des techniques d’analyse de données** pour appuyer les observations avec des preuves concrètes.
- **Visualiser les tendances** grâce à des représentations claires (graphiques, tableaux).
""")

# ✅ Résumé des hypothèses vérifiées
st.markdown("### ✅ Vérification des hypothèses")

st.success("""
1. **Les jeux d'action sont les plus vendus dans le monde**  
   → Analyse par genre : le genre **Action** est en tête des ventes mondiales.

2. **Les États-Unis représentent la plus grande part de consommation de jeux vidéo**  
   → Les **ventes en Amérique du Nord (NA_Sales)** dépassent largement les autres régions.

3. **Les joueurs japonais consomment principalement des jeux sur les consoles Nintendo**  
   → Les plateformes **Nintendo** (DS, Wii, 3DS, etc.) regroupent plus de **50% des ventes au Japon**.
""")

# 🧠 Synthèse
st.markdown("### 🧠 Synthèse globale")

st.info("""
L’analyse met en lumière des tendances fortes du marché vidéoludique mondial :

- Le genre **Action** est un moteur central des ventes.
- L’**Amérique du Nord** est le marché le plus important en volume.
- Le **Japon reste fidèle à l’écosystème Nintendo**, qui y conserve une dominance historique.

Ces résultats confirment que les préférences de genre et de plateforme varient fortement selon les zones géographiques, ce qui est essentiel à prendre en compte dans le développement et la commercialisation de jeux vidéo.
""")

# Remerciement / ouverture
st.markdown("### 👋 Merci pour votre attention !")
st.markdown("Ce projet peut être enrichi avec d'autres dimensions : évolution dans le temps, analyse par éditeur, impact des franchises...")

