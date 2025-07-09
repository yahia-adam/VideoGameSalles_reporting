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
    page_title="Vente de jeux vidéo par région",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre
st.markdown("# 🌍 Les États-Unis représentent-ils la plus grande part de consommation de jeux vidéo ❓")
st.markdown("---")

# Chargement du dataset
@st.cache_data
def load_data():
    df = pd.read_csv("datasets/vgsales.csv")
    # Nettoyage de base
    df = df.dropna(subset=["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"])
    # Conversion de Year en numérique
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    return df

df = load_data()

# Sidebar pour les filtres
st.sidebar.header("🔧 Filtres d'analyse")

# Filtre par période
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider("Période d'analyse", min_year, max_year, (min_year, max_year))

# Filtre par genre
genres = ['Tous'] + sorted(df['Genre'].unique().tolist())
selected_genre = st.sidebar.selectbox("Genre de jeu", genres)

# Filtre par plateforme
platforms = ['Toutes'] + sorted(df['Platform'].unique().tolist())
selected_platform = st.sidebar.selectbox("Plateforme", platforms)

# Filtre par seuil de ventes
min_sales = st.sidebar.slider("Ventes minimales par jeu (millions)", 0.0, 5.0, 0.0, 0.1)

# Application des filtres
filtered_df = df[
    (df['Year'] >= year_range[0]) & 
    (df['Year'] <= year_range[1]) &
    (df['Global_Sales'] >= min_sales)
]

if selected_genre != 'Tous':
    filtered_df = filtered_df[filtered_df['Genre'] == selected_genre]

if selected_platform != 'Toutes':
    filtered_df = filtered_df[filtered_df['Platform'] == selected_platform]

# Explication
st.info("""
### 🔎 Objectif de l'analyse :
Comparer les ventes régionales de jeux vidéo afin de savoir si **l'Amérique du Nord (NA_Sales)** est la région où les jeux se vendent le plus.
""")

# Métriques principales
col1, col2, col3, col4 = st.columns(4)

# Calcul des ventes totales par région
na_total = filtered_df["NA_Sales"].sum()
eu_total = filtered_df["EU_Sales"].sum()
jp_total = filtered_df["JP_Sales"].sum()
other_total = filtered_df["Other_Sales"].sum()
global_total = filtered_df["Global_Sales"].sum()

with col1:
    st.metric("🇺🇸 Amérique du Nord", f"{na_total:.1f}M", f"{(na_total/global_total*100):.1f}%")
with col2:
    st.metric("🇪🇺 Europe", f"{eu_total:.1f}M", f"{(eu_total/global_total*100):.1f}%")
with col3:
    st.metric("🇯🇵 Japon", f"{jp_total:.1f}M", f"{(jp_total/global_total*100):.1f}%")
with col4:
    st.metric("🌏 Autres régions", f"{other_total:.1f}M", f"{(other_total/global_total*100):.1f}%")

# Agrégation des ventes par région
regional_sales = {
    "Amérique du Nord (NA)": na_total,
    "Europe (EU)": eu_total,
    "Japon (JP)": jp_total,
    "Autres régions": other_total
}

# Conversion en DataFrame
sales_df = pd.DataFrame.from_dict(regional_sales, orient='index', columns=["Ventes (en millions)"])
sales_df = sales_df.sort_values(by="Ventes (en millions)", ascending=False).reset_index()
sales_df.columns = ["Région", "Ventes (en millions)"]

# Affichage du tableau
st.markdown("### 📋 Ventes totales par région")
st.dataframe(sales_df.style.format({"Ventes (en millions)": "{:.2f}"}), use_container_width=True)

# Layout en colonnes pour les graphiques principaux
col1, col2 = st.columns(2)

with col1:
    # Graphique en barres interactif
    st.markdown("### 📊 Ventes par région")
    fig_bar = px.bar(
        sales_df, 
        x='Région', 
        y='Ventes (en millions)',
        title="Ventes régionales de jeux vidéo",
        color='Ventes (en millions)',
        color_continuous_scale='viridis'
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Graphique en secteurs
    st.markdown("### 🥧 Répartition mondiale")
    fig_pie = px.pie(
        sales_df, 
        values='Ventes (en millions)', 
        names='Région',
        title="Répartition des ventes mondiales",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Analyses temporelles
st.markdown("---")
st.markdown("## 📈 Évolution temporelle des ventes régionales")

# Évolution des ventes par région au fil du temps
yearly_regional_sales = filtered_df.groupby('Year').agg({
    'NA_Sales': 'sum',
    'EU_Sales': 'sum',
    'JP_Sales': 'sum',
    'Other_Sales': 'sum'
}).reset_index()

# Reshape pour plotly
yearly_melted = yearly_regional_sales.melt(
    id_vars=['Year'], 
    value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
    var_name='Région', 
    value_name='Ventes'
)

# Mapping des noms de régions
region_mapping = {
    'NA_Sales': 'Amérique du Nord',
    'EU_Sales': 'Europe',
    'JP_Sales': 'Japon',
    'Other_Sales': 'Autres régions'
}
yearly_melted['Région'] = yearly_melted['Région'].map(region_mapping)

fig_timeline = px.line(
    yearly_melted, 
    x='Year', 
    y='Ventes', 
    color='Région',
    title="Évolution des ventes par région (1980-2020)",
    labels={'Ventes': 'Ventes (en millions)', 'Year': 'Année'}
)
st.plotly_chart(fig_timeline, use_container_width=True)

# Analyse par genre et région
st.markdown("### 🎮 Ventes par genre et région")

genre_regional = filtered_df.groupby('Genre').agg({
    'NA_Sales': 'sum',
    'EU_Sales': 'sum',
    'JP_Sales': 'sum',
    'Other_Sales': 'sum'
}).reset_index()

# Reshape pour la visualisation
genre_melted = genre_regional.melt(
    id_vars=['Genre'], 
    value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
    var_name='Région', 
    value_name='Ventes'
)
genre_melted['Région'] = genre_melted['Région'].map(region_mapping)

fig_genre_region = px.bar(
    genre_melted, 
    x='Genre', 
    y='Ventes', 
    color='Région',
    title="Ventes par genre et région",
    labels={'Ventes': 'Ventes (en millions)'},
    barmode='group'
)
fig_genre_region.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_genre_region, use_container_width=True)

# Heatmap des ventes par décennie et région
st.markdown("### 🔥 Heatmap : Ventes par décennie et région")

# Créer des décennies
filtered_df['Decade'] = (filtered_df['Year'] // 10) * 10
decade_regional = filtered_df.groupby('Decade').agg({
    'NA_Sales': 'sum',
    'EU_Sales': 'sum',
    'JP_Sales': 'sum',
    'Other_Sales': 'sum'
}).reset_index()

# Reshape pour heatmap
decade_melted = decade_regional.melt(
    id_vars=['Decade'], 
    value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
    var_name='Région', 
    value_name='Ventes'
)
decade_melted['Région'] = decade_melted['Région'].map(region_mapping)

# Pivot pour heatmap
heatmap_data = decade_melted.pivot(index='Decade', columns='Région', values='Ventes')

fig_heatmap = px.imshow(
    heatmap_data,
    title="Ventes par décennie et région",
    labels=dict(x="Région", y="Décennie", color="Ventes (millions)"),
    aspect="auto",
    color_continuous_scale='RdYlBu_r'
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Analyse des plateformes par région
st.markdown("### 🕹️ Top 10 des plateformes par région")

col1, col2 = st.columns(2)

with col1:
    # Top plateformes en Amérique du Nord
    na_platforms = filtered_df.groupby('Platform')['NA_Sales'].sum().sort_values(ascending=False).head(10)
    
    fig_na_platforms = px.bar(
        x=na_platforms.values,
        y=na_platforms.index,
        orientation='h',
        title="Top 10 plateformes - Amérique du Nord",
        labels={'x': 'Ventes (millions)', 'y': 'Plateforme'},
        color=na_platforms.values,
        color_continuous_scale='blues'
    )
    fig_na_platforms.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_na_platforms, use_container_width=True)

with col2:
    # Top plateformes en Europe
    eu_platforms = filtered_df.groupby('Platform')['EU_Sales'].sum().sort_values(ascending=False).head(10)
    
    fig_eu_platforms = px.bar(
        x=eu_platforms.values,
        y=eu_platforms.index,
        orientation='h',
        title="Top 10 plateformes - Europe",
        labels={'x': 'Ventes (millions)', 'y': 'Plateforme'},
        color=eu_platforms.values,
        color_continuous_scale='greens'
    )
    fig_eu_platforms.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_eu_platforms, use_container_width=True)

# Analyse de la dominance régionale par genre
st.markdown("### 🏆 Dominance régionale par genre")

# Calculer quelle région domine chaque genre
genre_dominance = []
for genre in filtered_df['Genre'].unique():
    genre_data = filtered_df[filtered_df['Genre'] == genre]
    sales_by_region = {
        'NA': genre_data['NA_Sales'].sum(),
        'EU': genre_data['EU_Sales'].sum(),
        'JP': genre_data['JP_Sales'].sum(),
        'Other': genre_data['Other_Sales'].sum()
    }
    dominant_region = max(sales_by_region, key=sales_by_region.get)
    genre_dominance.append({
        'Genre': genre,
        'Région_dominante': dominant_region,
        'Ventes_max': sales_by_region[dominant_region],
        'Total_genre': sum(sales_by_region.values())
    })

dominance_df = pd.DataFrame(genre_dominance)
dominance_df['Pourcentage'] = (dominance_df['Ventes_max'] / dominance_df['Total_genre'] * 100).round(1)

# Mapping des régions pour l'affichage
region_display = {'NA': 'Amérique du Nord', 'EU': 'Europe', 'JP': 'Japon', 'Other': 'Autres'}
dominance_df['Région_dominante'] = dominance_df['Région_dominante'].map(region_display)

fig_dominance = px.bar(
    dominance_df.sort_values('Pourcentage', ascending=False),
    x='Genre',
    y='Pourcentage',
    color='Région_dominante',
    title="Pourcentage de dominance par genre et région",
    labels={'Pourcentage': 'Dominance (%)', 'Genre': 'Genre'}
)
fig_dominance.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_dominance, use_container_width=True)

# Comparaison avec les ventes globales
st.markdown("### 📊 Corrélation entre ventes régionales et globales")

col1, col2 = st.columns(2)

with col1:
    # Scatter plot NA vs Global
    fig_scatter_na = px.scatter(
        filtered_df, 
        x='NA_Sales', 
        y='Global_Sales',
        title="Corrélation NA vs Ventes Globales",
        labels={'NA_Sales': 'Ventes Amérique du Nord', 'Global_Sales': 'Ventes Globales'},
        opacity=0.6
    )
    # Ligne de tendance
    fig_scatter_na.add_trace(
        go.Scatter(
            x=filtered_df['NA_Sales'], 
            y=filtered_df['NA_Sales'] * (filtered_df['Global_Sales'] / filtered_df['NA_Sales']).mean(),
            mode='lines', 
            name='Tendance',
            line=dict(dash='dash')
        )
    )
    st.plotly_chart(fig_scatter_na, use_container_width=True)

with col2:
    # Scatter plot EU vs Global
    fig_scatter_eu = px.scatter(
        filtered_df, 
        x='EU_Sales', 
        y='Global_Sales',
        title="Corrélation EU vs Ventes Globales",
        labels={'EU_Sales': 'Ventes Europe', 'Global_Sales': 'Ventes Globales'},
        opacity=0.6
    )
    st.plotly_chart(fig_scatter_eu, use_container_width=True)

# Top des jeux par région
st.markdown("### 🎯 Top 5 des jeux les plus vendus par région")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🇺🇸 Amérique du Nord**")
    top_na = filtered_df.nlargest(5, 'NA_Sales')[['Name', 'NA_Sales', 'Year', 'Genre']]
    for idx, game in top_na.iterrows():
        st.write(f"• **{game['Name']}** ({game['Year']}) - {game['NA_Sales']:.2f}M - {game['Genre']}")

with col2:
    st.markdown("**🇪🇺 Europe**")
    top_eu = filtered_df.nlargest(5, 'EU_Sales')[['Name', 'EU_Sales', 'Year', 'Genre']]
    for idx, game in top_eu.iterrows():
        st.write(f"• **{game['Name']}** ({game['Year']}) - {game['EU_Sales']:.2f}M - {game['Genre']}")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**🇯🇵 Japon**")
    top_jp = filtered_df.nlargest(5, 'JP_Sales')[['Name', 'JP_Sales', 'Year', 'Genre']]
    for idx, game in top_jp.iterrows():
        st.write(f"• **{game['Name']}** ({game['Year']}) - {game['JP_Sales']:.2f}M - {game['Genre']}")

with col4:
    st.markdown("**🌏 Autres régions**")
    top_other = filtered_df.nlargest(5, 'Other_Sales')[['Name', 'Other_Sales', 'Year', 'Genre']]
    for idx, game in top_other.iterrows():
        st.write(f"• **{game['Name']}** ({game['Year']}) - {game['Other_Sales']:.2f}M - {game['Genre']}")

# Analyse statistique
st.markdown("### 📈 Statistiques détaillées")

# Calcul des statistiques
stats_data = {
    'Région': ['Amérique du Nord', 'Europe', 'Japon', 'Autres régions'],
    'Moyenne': [filtered_df['NA_Sales'].mean(), filtered_df['EU_Sales'].mean(), 
                filtered_df['JP_Sales'].mean(), filtered_df['Other_Sales'].mean()],
    'Médiane': [filtered_df['NA_Sales'].median(), filtered_df['EU_Sales'].median(), 
                filtered_df['JP_Sales'].median(), filtered_df['Other_Sales'].median()],
    'Écart-type': [filtered_df['NA_Sales'].std(), filtered_df['EU_Sales'].std(), 
                   filtered_df['JP_Sales'].std(), filtered_df['Other_Sales'].std()],
    'Maximum': [filtered_df['NA_Sales'].max(), filtered_df['EU_Sales'].max(), 
                filtered_df['JP_Sales'].max(), filtered_df['Other_Sales'].max()]
}

stats_df = pd.DataFrame(stats_data)
st.dataframe(stats_df.style.format({
    'Moyenne': '{:.3f}',
    'Médiane': '{:.3f}',
    'Écart-type': '{:.3f}',
    'Maximum': '{:.2f}'
}), use_container_width=True)

# Conclusion dynamique
st.markdown("---")
st.markdown("## 🎯 Conclusion")

top_region = sales_df.iloc[0]["Région"]
top_value = sales_df.iloc[0]["Ventes (en millions)"]
percentage = (top_value / global_total * 100)

if "NA" in top_region:
    st.success(f"""
    ✅ **Conclusion :** Oui, l'**Amérique du Nord** est la plus grande consommatrice de jeux vidéo, avec un total de **{top_value:.2f} millions** d'unités vendues (**{percentage:.1f}%** du marché mondial).
    """)
else:
    st.warning(f"""
    ❌ **Conclusion :** Non, l'Amérique du Nord n'est pas la plus grande consommatrice. C'est **{top_region}** qui arrive en tête avec **{top_value:.2f} millions** d'unités (**{percentage:.1f}%** du marché).
    """)

# Insights supplémentaires
st.info(f"""
### 💡 Insights détaillés :
- **Période analysée :** {year_range[0]} - {year_range[1]}
- **Genre sélectionné :** {selected_genre}
- **Plateforme :** {selected_platform}
- **Seuil de ventes :** {min_sales} millions minimum
- **Nombre de jeux analysés :** {len(filtered_df)} jeux
- **Ventes totales :** {global_total:.2f} millions d'unités

### 🌍 Répartition mondiale actuelle :
- 🇺🇸 Amérique du Nord : {(na_total/global_total*100):.1f}%
- 🇪🇺 Europe : {(eu_total/global_total*100):.1f}%
- 🇯🇵 Japon : {(jp_total/global_total*100):.1f}%
- 🌏 Autres régions : {(other_total/global_total*100):.1f}%
""")

# Footer
st.markdown("---")
st.markdown("*Analyse réalisée avec Streamlit et Plotly - Données sur les ventes régionales de jeux vidéo*")