import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Analyse des Ventes de Jeux Vidéo",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header avec logo et titre
st.markdown("""
<div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
    <h1 style="color: white; margin: 0; font-size: 3rem;">🎮 Analyse des Ventes de Jeux Vidéo</h1>
    <p style="color: white; margin: 0; font-size: 1.2rem; opacity: 0.9;">Étude du marché mondial du gaming (1980-2020)</p>
</div>
""", unsafe_allow_html=True)

# Informations contextuelles
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 🎓 **Contexte Académique**
    
    **🏫 École :** ESGI  
    **📚 Classe :** 4ème année  
    **🎯 Filière :** Intelligence Artificielle et Big Data  
    **📊 Cours :** Reporting et Restitution  
    """)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px;">
        <h3>📅 Projet 2024/2025</h3>
        <p><strong>Analyse de données</strong><br>
        <strong>Visualisation interactive</strong><br>
        <strong>Business Intelligence</strong></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Équipe
st.markdown("## 👥 **Notre Équipe**")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <img src="https://ges-dl.kordis.fr/public/dEkj-aOcIw52B9RsgY-op3gtqnfCNW1ZCZSMwXEBz3M?pfdrid_c=true" 
             style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #667eea;">
        <h4 style="margin: 0.5rem 0; color: #333;">YAHIA ABDCHAFEE Adam</h4>
        <p style="color: #666; margin: 0;">Data Analyst</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <img src="https://ges-dl.kordis.fr/public/dEkj-aOcIw52B9RsgY-op5CjG2r1koq1CZSMwXEBz3M?pfdrid_c=true" 
             style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #667eea;">
        <h4 style="margin: 0.5rem 0; color: #333;">KIANMENE TAKUEFOU Clyde</h4>
        <p style="color: #666; margin: 0;">Data Scientist</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <img src="https://ges-dl.kordis.fr/public/dEkj-aOcIw52B9RsgY-opzVejpo67SADCZSMwXEBz3M?pfdrid_c=true" 
             style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #667eea;">
        <h4 style="margin: 0.5rem 0; color: #333;">BOUZOUBAA Yassine</h4>
        <p style="color: #666; margin: 0;">Business Analyst</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Objectif du projet
st.markdown("## 🎯 **Objectif du Projet**")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    ### Analyser le marché mondial des jeux vidéo pour :
    
    🔍 **Identifier les tendances** du marché gaming  
    📊 **Comprendre les préférences** régionales  
    🎮 **Analyser les performances** par plateforme et genre  
    💡 **Fournir des insights** pour l'industrie du gaming  
    """)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b, #feca57); padding: 2rem; border-radius: 15px; text-align: center;">
        <h3 style="color: white; margin: 0;">📈 Data-Driven</h3>
        <p style="color: white; margin: 0.5rem 0;">Analyse basée sur</p>
        <h2 style="color: white; margin: 0;">16,598 jeux</h2>
        <p style="color: white; margin: 0;">de 1980 à 2020</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Dataset Overview
st.markdown("## 📊 **Aperçu du Dataset**")

# Chargement des données pour les statistiques
df = pd.read_csv("datasets/vgsales.csv")

# Métriques principales
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🎮 Total Jeux", f"{len(df):,}")

with col2:
    st.metric("🌍 Ventes Totales", f"{df['Global_Sales'].sum():.0f}M")

with col3:
    st.metric("🎯 Genres", f"{df['Genre'].nunique()}")

with col4:
    st.metric("🕹️ Plateformes", f"{df['Platform'].nunique()}")

with col5:
    st.metric("📅 Années", f"{df['Year'].min():.0f}-{df['Year'].max():.0f}")

# Graphiques de présentation rapide
col1, col2 = st.columns(2)

with col1:
    # Top 10 des genres
    genre_sales = df.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).head(10)
    fig_genre = px.bar(
        x=genre_sales.values, 
        y=genre_sales.index,
        orientation='h',
        title="🎮 Top 10 des Genres",
        labels={'x': 'Ventes (millions)', 'y': 'Genre'},
        color=genre_sales.values,
        color_continuous_scale='viridis'
    )
    fig_genre.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_genre, use_container_width=True)

with col2:
    # Ventes par région
    regional_sales = {
        'Amérique du Nord': df['NA_Sales'].sum(),
        'Europe': df['EU_Sales'].sum(), 
        'Japon': df['JP_Sales'].sum(),
        'Autres': df['Other_Sales'].sum()
    }
    
    fig_region = px.pie(
        values=list(regional_sales.values()),
        names=list(regional_sales.keys()),
        title="🌍 Répartition Mondiale des Ventes",
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    )
    fig_region.update_layout(height=400)
    st.plotly_chart(fig_region, use_container_width=True)

# Structure du dataset
st.markdown("### 📋 **Structure du Dataset**")

col1, col2 = st.columns([3, 2])

with col1:
    # Affichage d'un échantillon du dataset
    st.dataframe(df.head(10), use_container_width=True)

with col2:
    st.markdown("""
    **Colonnes principales :**
    
    • **Name** : Nom du jeu  
    • **Platform** : Console/Plateforme  
    • **Year** : Année de sortie  
    • **Genre** : Catégorie du jeu  
    • **Publisher** : Éditeur  
    • **NA_Sales** : Ventes Amérique du Nord  
    • **EU_Sales** : Ventes Europe  
    • **JP_Sales** : Ventes Japon  
    • **Other_Sales** : Autres régions  
    • **Global_Sales** : Ventes mondiales  
    """)

st.markdown("---")

# Hypothèses
st.markdown("## ❓ **Hypothèses à Vérifier**")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="padding: 1.5rem; background-color: #e8f4fd; border-left: 5px solid #2196F3; border-radius: 10px;">
        <h4 style="margin: 0 0 1rem 0; color: #1976D2;">🎮 Hypothèse 1</h4>
        <p style="margin: 0; color: #333;"><strong>Les jeux d'Action sont-ils les plus vendus mondialement ?</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #666;">Analyse des ventes par genre</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding: 1.5rem; background-color: #f3e5f5; border-left: 5px solid #9C27B0; border-radius: 10px;">
        <h4 style="margin: 0 0 1rem 0; color: #7B1FA2;">🌍 Hypothèse 2</h4>
        <p style="margin: 0; color: #333;"><strong>Les États-Unis dominent-ils la consommation mondiale ?</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #666;">Analyse des ventes régionales</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="padding: 1.5rem; background-color: #fff3e0; border-left: 5px solid #FF9800; border-radius: 10px;">
        <h4 style="margin: 0 0 1rem 0; color: #F57C00;">🇯🇵 Hypothèse 3</h4>
        <p style="margin: 0; color: #333;"><strong>Le Japon privilégie-t-il les consoles Nintendo ?</strong></p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #666;">Analyse du marché japonais</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Liens et ressources
st.markdown("## 🔗 **Ressources du Projet**")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background-color: #f8f9fa; border-radius: 15px;">
        <h4>📂 Code Source</h4>
        <a href="https://github.com/yahia-adam/VideoGameSalles_reporting" target="_blank" 
           style="text-decoration: none; background-color: #24292e; color: white; padding: 0.7rem 1.5rem; 
                  border-radius: 25px; display: inline-block; margin-top: 1rem;">
            🔗 GitHub Repository
        </a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background-color: #f8f9fa; border-radius: 15px;">
        <h4>📊 Dataset</h4>
        <a href="https://www.kaggle.com/datasets/gregorut/videogamesales" target="_blank" 
           style="text-decoration: none; background-color: #20beff; color: white; padding: 0.7rem 1.5rem; 
                  border-radius: 25px; display: inline-block; margin-top: 1rem;">
            🔗 Kaggle Dataset
        </a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background-color: #f8f9fa; border-radius: 15px;">
        <h4>🎓 ESGI</h4>
        <a href="https://www.esgi.fr" target="_blank" 
           style="text-decoration: none; background-color: #e74c3c; color: white; padding: 0.7rem 1.5rem; 
                  border-radius: 25px; display: inline-block; margin-top: 1rem;">
            🔗 Site École
        </a>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;">
    <p style="margin: 0; color: #666; font-size: 0.9rem;">
        🎮 Projet développé dans le cadre du cours "Reporting et Restitution" - ESGI 2024/2025<br>
        📊 Analyse interactive des données de ventes de jeux vidéo avec Streamlit et Python
    </p>
</div>
""", unsafe_allow_html=True)