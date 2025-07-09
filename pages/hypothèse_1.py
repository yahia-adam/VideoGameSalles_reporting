import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Vente de jeux vidéo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre principal
st.markdown("# 🎮 Les jeux d'action sont-ils les plus vendus dans le monde ❓")
st.markdown("---")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("datasets/vgsales.csv")
    # Nettoyage basique
    df = df.dropna(subset=["Genre", "Global_Sales"])
    # Conversion de Year en numérique et nettoyage
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    return df

df = load_data()

# Sidebar pour les filtres
st.sidebar.header("🔧 Filtres")
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider("Sélectionnez la période", min_year, max_year, (min_year, max_year))

# Filtre par plateforme
platforms = ['Toutes'] + sorted(df['Platform'].unique().tolist())
selected_platform = st.sidebar.selectbox("Plateforme", platforms)

# Filtre par région
regions = st.sidebar.multiselect(
    "Régions à analyser", 
    ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
    default=['NA_Sales', 'EU_Sales', 'JP_Sales']
)

# Application des filtres
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
if selected_platform != 'Toutes':
    filtered_df = filtered_df[filtered_df['Platform'] == selected_platform]

# Explication de la démarche
st.info("""
### 🔎 Objectif de l'analyse :
Nous allons analyser les ventes mondiales (`Global_Sales`) par **genre de jeu** afin de déterminer si les jeux d'action (**Action**) sont effectivement les plus vendus à l'échelle mondiale.
""")

# Métriques principales
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total des jeux", len(filtered_df))
with col2:
    st.metric("Ventes totales", f"{filtered_df['Global_Sales'].sum():.1f}M")
with col3:
    st.metric("Genres uniques", filtered_df['Genre'].nunique())
with col4:
    st.metric("Plateformes", filtered_df['Platform'].nunique())

# Agrégation des ventes par genre
sales_by_genre = filtered_df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False).reset_index()

# Affichage du tableau
st.markdown("### 📋 Classement des genres par ventes mondiales")
st.dataframe(sales_by_genre.style.format({"Global_Sales": "{:.2f}"}), use_container_width=True)

# Layout en colonnes pour les graphiques
col1, col2 = st.columns(2)

with col1:
    # Graphique en barres horizontales (original amélioré)
    st.markdown("### 📊 Ventes globales par genre")
    fig_bar = px.bar(
        sales_by_genre, 
        x='Global_Sales', 
        y='Genre',
        orientation='h',
        title="Ventes mondiales par genre de jeu",
        labels={'Global_Sales': 'Ventes (en millions)', 'Genre': 'Genre'},
        color='Global_Sales',
        color_continuous_scale='viridis'
    )
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Graphique en secteurs (camembert)
    st.markdown("### 🥧 Répartition des ventes par genre")
    fig_pie = px.pie(
        sales_by_genre.head(8), 
        values='Global_Sales', 
        names='Genre',
        title="Répartition des ventes par genre (Top 8)"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Graphiques supplémentaires
st.markdown("---")
st.markdown("## 📈 Analyses approfondies")

# Évolution temporelle des ventes par genre
st.markdown("### 📅 Évolution des ventes par genre au fil du temps")
yearly_genre_sales = filtered_df.groupby(['Year', 'Genre'])['Global_Sales'].sum().reset_index()
top_genres = sales_by_genre.head(5)['Genre'].tolist()
yearly_top_genres = yearly_genre_sales[yearly_genre_sales['Genre'].isin(top_genres)]

fig_timeline = px.line(
    yearly_top_genres, 
    x='Year', 
    y='Global_Sales', 
    color='Genre',
    title="Évolution des ventes des 5 genres les plus populaires",
    labels={'Global_Sales': 'Ventes (en millions)', 'Year': 'Année'}
)
st.plotly_chart(fig_timeline, use_container_width=True)

# Analyse par région
if regions:
    st.markdown("### 🌍 Ventes par région et genre")
    
    # Calcul des ventes par région pour chaque genre
    region_data = []
    for region in regions:
        region_sales = filtered_df.groupby('Genre')[region].sum().reset_index()
        region_sales['Region'] = region.replace('_Sales', '')
        region_sales = region_sales.rename(columns={region: 'Sales'})
        region_data.append(region_sales)
    
    region_df = pd.concat(region_data, ignore_index=True)
    
    # Graphique en barres groupées
    fig_region = px.bar(
        region_df, 
        x='Genre', 
        y='Sales', 
        color='Region',
        title="Ventes par région et genre",
        labels={'Sales': 'Ventes (en millions)', 'Genre': 'Genre'},
        barmode='group'
    )
    fig_region.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_region, use_container_width=True)

# Analyse des plateformes
st.markdown("### 🎮 Top 10 des plateformes par ventes")
platform_sales = filtered_df.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(10)

col1, col2 = st.columns(2)

with col1:
    fig_platform = px.bar(
        x=platform_sales.values,
        y=platform_sales.index,
        orientation='h',
        title="Top 10 des plateformes",
        labels={'x': 'Ventes (en millions)', 'y': 'Plateforme'}
    )
    fig_platform.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_platform, use_container_width=True)

with col2:
    # Heatmap genre x plateforme
    st.markdown("### 🔥 Heatmap Genre x Plateforme (Top 10)")
    top_platforms = platform_sales.head(10).index.tolist()
    heatmap_data = filtered_df[filtered_df['Platform'].isin(top_platforms)].pivot_table(
        index='Genre', 
        columns='Platform', 
        values='Global_Sales', 
        aggfunc='sum', 
        fill_value=0
    )
    
    fig_heatmap = px.imshow(
        heatmap_data,
        title="Ventes par Genre et Plateforme",
        labels=dict(x="Plateforme", y="Genre", color="Ventes (millions)"),
        aspect="auto"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Analyse statistique avancée
st.markdown("### 📊 Analyse statistique des genres")

col1, col2 = st.columns(2)

with col1:
    # Box plot des ventes par genre
    fig_box = px.box(
        filtered_df, 
        x='Genre', 
        y='Global_Sales',
        title="Distribution des ventes par genre (Box Plot)"
    )
    fig_box.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    # Violon plot
    fig_violin = px.violin(
        filtered_df, 
        x='Genre', 
        y='Global_Sales',
        title="Distribution des ventes par genre (Violin Plot)"
    )
    fig_violin.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_violin, use_container_width=True)

# Top des jeux par genre
st.markdown("### 🏆 Top 3 des jeux par genre")
top_games_by_genre = (filtered_df.groupby('Genre')
                     .apply(lambda x: x.nlargest(3, 'Global_Sales')[['Name', 'Global_Sales', 'Year', 'Platform']])
                     .reset_index(drop=True))

for genre in sales_by_genre['Genre'].head(6):  # Top 6 genres
    genre_games = filtered_df[filtered_df['Genre'] == genre].nlargest(3, 'Global_Sales')
    if not genre_games.empty:
        st.markdown(f"**{genre}:**")
        for idx, game in genre_games.iterrows():
            st.write(f"• {game['Name']} ({game['Year']}) - {game['Global_Sales']:.2f}M ventes")

# Analyse de corrélation
st.markdown("### 🔗 Corrélations entre régions")
correlation_data = filtered_df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].corr()
fig_corr = px.imshow(
    correlation_data,
    title="Matrice de corrélation entre les ventes régionales",
    labels=dict(color="Corrélation"),
    text_auto=True
)
st.plotly_chart(fig_corr, use_container_width=True)

# Conclusion dynamique
st.markdown("---")
st.markdown("## 🎯 Conclusion")

top_genre = sales_by_genre.iloc[0]["Genre"]
top_sales = sales_by_genre.iloc[0]["Global_Sales"]

if top_genre.lower() == "action":
    st.success(f"""
    ✅ **Conclusion :** Oui, les jeux d'**action** sont les plus vendus dans le monde, avec un total de **{top_sales:.2f} millions** d'unités vendues.
    """)
else:
    st.warning(f"""
    ❌ **Conclusion :** Non, les jeux d'**action** ne sont pas les plus vendus. Le genre le plus vendu est **{top_genre}** avec **{top_sales:.2f} millions** d'unités.
    """)

# Insights supplémentaires
st.info(f"""
### 💡 Insights supplémentaires :
- **Période analysée :** {year_range[0]} - {year_range[1]}
- **Plateforme :** {selected_platform}
- **Genre dominant :** {top_genre} représente {(top_sales/filtered_df['Global_Sales'].sum()*100):.1f}% des ventes totales
- **Nombre de jeux analysés :** {len(filtered_df)} jeux
""")

# Footer
st.markdown("---")
st.markdown("*Analyse réalisée avec Streamlit et Plotly*")