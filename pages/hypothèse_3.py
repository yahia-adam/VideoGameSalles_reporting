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
    page_title="Nintendo au Japon",
    page_icon="🇯🇵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre
st.markdown("# 🇯🇵 Les joueurs japonais consomment-ils principalement des jeux sur les consoles Nintendo ❓")
st.markdown("---")

# Chargement du dataset
@st.cache_data
def load_data():
    df = pd.read_csv("datasets/vgsales.csv")
    # Nettoyage
    df = df.dropna(subset=["Platform", "JP_Sales"])
    # Conversion de Year en numérique
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    return df

df = load_data()

# Sidebar pour les filtres
st.sidebar.header("🎮 Filtres d'analyse")

# Filtre par période
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())
year_range = st.sidebar.slider("Période d'analyse", min_year, max_year, (min_year, max_year))

# Filtre par genre
genres = ['Tous'] + sorted(df['Genre'].unique().tolist())
selected_genre = st.sidebar.selectbox("Genre de jeu", genres)

# Filtre par génération de console
generations = st.sidebar.multiselect(
    "Générations de consoles",
    ['Rétro (1980-1995)', 'Classique (1996-2005)', 'Moderne (2006-2015)', 'Actuelle (2016+)'],
    default=['Rétro (1980-1995)', 'Classique (1996-2005)', 'Moderne (2006-2015)', 'Actuelle (2016+)']
)

# Seuil de ventes
min_sales = st.sidebar.slider("Ventes minimales au Japon (millions)", 0.0, 2.0, 0.0, 0.1)

# Mapping des générations
def get_generation(year):
    if year <= 1995:
        return 'Rétro (1980-1995)'
    elif year <= 2005:
        return 'Classique (1996-2005)'
    elif year <= 2015:
        return 'Moderne (2006-2015)'
    else:
        return 'Actuelle (2016+)'

df['Generation'] = df['Year'].apply(get_generation)

# Application des filtres
filtered_df = df[
    (df['Year'] >= year_range[0]) & 
    (df['Year'] <= year_range[1]) &
    (df['JP_Sales'] >= min_sales) &
    (df['Generation'].isin(generations))
]

if selected_genre != 'Tous':
    filtered_df = filtered_df[filtered_df['Genre'] == selected_genre]

# Explication de l'objectif
st.info("""
### 🔎 Objectif de l'analyse :
Nous allons analyser les ventes **au Japon** (`JP_Sales`) en fonction des **plateformes de jeux** pour déterminer si les consoles **Nintendo** dominent le marché japonais.
""")

# Liste des plateformes par constructeur (étendue)
nintendo_platforms = ["DS", "3DS", "Wii", "WiiU", "GBA", "GC", "Switch", "SNES", "NES", "N64", "GB"]
sony_platforms = ["PS", "PS2", "PS3", "PS4", "PSP", "PSV"]
microsoft_platforms = ["XB", "X360", "XOne"]
sega_platforms = ["DC", "GEN", "SAT", "SCD", "WS", "GG"]
other_platforms = ["PC", "2600", "3DO", "NG", "TG16", "PCFX"]

def get_manufacturer(platform):
    if platform in nintendo_platforms:
        return "🎮 Nintendo"
    elif platform in sony_platforms:
        return "🎯 Sony"
    elif platform in microsoft_platforms:
        return "🟢 Microsoft"
    elif platform in sega_platforms:
        return "🔵 Sega"
    else:
        return "🖥️ Autres"

# Agrégation des ventes japonaises par plateforme
jp_sales_by_platform = filtered_df.groupby("Platform")["JP_Sales"].sum().sort_values(ascending=False).reset_index()

# Ajout des colonnes constructeur et génération
jp_sales_by_platform["Constructeur"] = jp_sales_by_platform["Platform"].apply(get_manufacturer)

# Calcul des totaux par constructeur
constructor_sales = jp_sales_by_platform.groupby("Constructeur")["JP_Sales"].sum().sort_values(ascending=False).reset_index()

# Métriques principales
total_jp_sales = filtered_df["JP_Sales"].sum()
nintendo_sales = constructor_sales[constructor_sales["Constructeur"] == "🎮 Nintendo"]["JP_Sales"].values[0] if len(constructor_sales[constructor_sales["Constructeur"] == "🎮 Nintendo"]) > 0 else 0
nintendo_share = (nintendo_sales / total_jp_sales) * 100 if total_jp_sales > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎮 Nintendo", f"{nintendo_sales:.1f}M", f"{nintendo_share:.1f}%")

with col2:
    sony_sales = constructor_sales[constructor_sales["Constructeur"] == "🎯 Sony"]["JP_Sales"].values[0] if len(constructor_sales[constructor_sales["Constructeur"] == "🎯 Sony"]) > 0 else 0
    sony_share = (sony_sales / total_jp_sales) * 100 if total_jp_sales > 0 else 0
    st.metric("🎯 Sony", f"{sony_sales:.1f}M", f"{sony_share:.1f}%")

with col3:
    st.metric("🇯🇵 Total Japon", f"{total_jp_sales:.1f}M", f"{len(filtered_df)} jeux")

with col4:
    st.metric("🏆 Leader", constructor_sales.iloc[0]["Constructeur"].split()[1] if len(constructor_sales) > 0 else "N/A", f"{(constructor_sales.iloc[0]['JP_Sales']/total_jp_sales*100):.1f}%" if len(constructor_sales) > 0 else "0%")

# Affichage du tableau complet par plateforme
st.markdown("### 📋 Ventes au Japon par plateforme")
display_df = jp_sales_by_platform.copy()
display_df['Pourcentage'] = (display_df['JP_Sales'] / total_jp_sales * 100).round(2)
st.dataframe(
    display_df.style.format({"JP_Sales": "{:.2f}", "Pourcentage": "{:.2f}%"}), 
    use_container_width=True
)

# Layout principal avec graphiques
col1, col2 = st.columns(2)

with col1:
    # Graphique en secteurs par constructeur
    st.markdown("### 📊 Répartition par constructeur")
    fig_pie = px.pie(
        constructor_sales, 
        values='JP_Sales', 
        names='Constructeur',
        title="Parts de marché au Japon",
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Graphique en barres par plateforme (top 10)
    st.markdown("### 🏆 Top 10 des plateformes")
    top_platforms = jp_sales_by_platform.head(10)
    fig_bar = px.bar(
        top_platforms, 
        x='JP_Sales', 
        y='Platform',
        orientation='h',
        title="Top 10 des plateformes au Japon",
        color='Constructeur',
        labels={'JP_Sales': 'Ventes (millions)', 'Platform': 'Plateforme'}
    )
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

# Analyses temporelles
st.markdown("---")
st.markdown("## 📈 Évolution temporelle")

# Évolution des parts de marché Nintendo vs autres
yearly_data = filtered_df.groupby(['Year', 'Platform'])['JP_Sales'].sum().reset_index()
yearly_data['Constructeur'] = yearly_data['Platform'].apply(get_manufacturer)
yearly_constructor = yearly_data.groupby(['Year', 'Constructeur'])['JP_Sales'].sum().reset_index()

fig_timeline = px.line(
    yearly_constructor, 
    x='Year', 
    y='JP_Sales', 
    color='Constructeur',
    title="Évolution des ventes par constructeur au Japon",
    labels={'JP_Sales': 'Ventes (millions)', 'Year': 'Année'}
)
st.plotly_chart(fig_timeline, use_container_width=True)

# Analyse par génération
st.markdown("### 🎯 Analyse par génération de consoles")

generation_data = filtered_df.groupby(['Generation', 'Platform'])['JP_Sales'].sum().reset_index()
generation_data['Constructeur'] = generation_data['Platform'].apply(get_manufacturer)
generation_constructor = generation_data.groupby(['Generation', 'Constructeur'])['JP_Sales'].sum().reset_index()

fig_generation = px.bar(
    generation_constructor, 
    x='Generation', 
    y='JP_Sales', 
    color='Constructeur',
    title="Ventes par génération et constructeur",
    labels={'JP_Sales': 'Ventes (millions)', 'Generation': 'Génération'},
    barmode='group'
)
st.plotly_chart(fig_generation, use_container_width=True)

# Analyse par genre
st.markdown("### 🎮 Dominance Nintendo par genre")

genre_analysis = filtered_df.groupby(['Genre', 'Platform'])['JP_Sales'].sum().reset_index()
genre_analysis['Constructeur'] = genre_analysis['Platform'].apply(get_manufacturer)
genre_constructor = genre_analysis.groupby(['Genre', 'Constructeur'])['JP_Sales'].sum().reset_index()

# Calculer la dominance Nintendo par genre
genre_dominance = []
for genre in filtered_df['Genre'].unique():
    genre_data = genre_constructor[genre_constructor['Genre'] == genre]
    total_genre = genre_data['JP_Sales'].sum()
    nintendo_genre = genre_data[genre_data['Constructeur'] == '🎮 Nintendo']['JP_Sales'].sum()
    nintendo_percent = (nintendo_genre / total_genre * 100) if total_genre > 0 else 0
    genre_dominance.append({
        'Genre': genre,
        'Nintendo_Share': nintendo_percent,
        'Total_Sales': total_genre,
        'Nintendo_Sales': nintendo_genre
    })

dominance_df = pd.DataFrame(genre_dominance).sort_values('Nintendo_Share', ascending=False)

fig_dominance = px.bar(
    dominance_df, 
    x='Genre', 
    y='Nintendo_Share',
    title="Dominance Nintendo par genre (%)",
    labels={'Nintendo_Share': 'Part Nintendo (%)', 'Genre': 'Genre'},
    color='Nintendo_Share',
    color_continuous_scale='RdYlGn'
)
fig_dominance.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_dominance, use_container_width=True)

# Heatmap des ventes par décennie et constructeur
st.markdown("### 🔥 Heatmap : Évolution par décennie")

filtered_df['Decade'] = (filtered_df['Year'] // 10) * 10
decade_data = filtered_df.groupby(['Decade', 'Platform'])['JP_Sales'].sum().reset_index()
decade_data['Constructeur'] = decade_data['Platform'].apply(get_manufacturer)
decade_constructor = decade_data.groupby(['Decade', 'Constructeur'])['JP_Sales'].sum().reset_index()

# Pivot pour heatmap
heatmap_data = decade_constructor.pivot(index='Decade', columns='Constructeur', values='JP_Sales').fillna(0)

fig_heatmap = px.imshow(
    heatmap_data,
    title="Évolution des ventes par décennie et constructeur",
    labels=dict(x="Constructeur", y="Décennie", color="Ventes (millions)"),
    aspect="auto",
    color_continuous_scale='Viridis'
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Comparaison Japon vs Monde
st.markdown("### 🌍 Comparaison Japon vs Monde")

col1, col2 = st.columns(2)

with col1:
    # Parts de marché au Japon
    st.markdown("**🇯🇵 Parts de marché au Japon**")
    jp_constructor = constructor_sales.copy()
    jp_constructor['Pourcentage'] = (jp_constructor['JP_Sales'] / jp_constructor['JP_Sales'].sum() * 100).round(1)
    
    for idx, row in jp_constructor.head(5).iterrows():
        st.write(f"• {row['Constructeur']}: {row['Pourcentage']:.1f}%")

with col2:
    # Parts de marché mondial
    st.markdown("**🌍 Parts de marché mondial**")
    world_data = filtered_df.groupby('Platform')['Global_Sales'].sum().reset_index()
    world_data['Constructeur'] = world_data['Platform'].apply(get_manufacturer)
    world_constructor = world_data.groupby('Constructeur')['Global_Sales'].sum().sort_values(ascending=False).reset_index()
    world_constructor['Pourcentage'] = (world_constructor['Global_Sales'] / world_constructor['Global_Sales'].sum() * 100).round(1)
    
    for idx, row in world_constructor.head(5).iterrows():
        st.write(f"• {row['Constructeur']}: {row['Pourcentage']:.1f}%")

# Top des jeux Nintendo au Japon
st.markdown("### 🏆 Top 10 des jeux Nintendo au Japon")

nintendo_games = filtered_df[filtered_df['Platform'].isin(nintendo_platforms)].nlargest(10, 'JP_Sales')
nintendo_top = nintendo_games[['Name', 'Platform', 'JP_Sales', 'Year', 'Genre']].reset_index(drop=True)
nintendo_top.index = nintendo_top.index + 1

col1, col2 = st.columns(2)

with col1:
    for i in range(1, 6):
        if i <= len(nintendo_top):
            game = nintendo_top.iloc[i-1]
            st.write(f"**{i}. {game['Name']}**")
            st.write(f"   📱 {game['Platform']} • 🎮 {game['Genre']} • 📅 {game['Year']} • 📊 {game['JP_Sales']:.2f}M")

with col2:
    for i in range(6, 11):
        if i <= len(nintendo_top):
            game = nintendo_top.iloc[i-1]
            st.write(f"**{i}. {game['Name']}**")
            st.write(f"   📱 {game['Platform']} • 🎮 {game['Genre']} • 📅 {game['Year']} • 📊 {game['JP_Sales']:.2f}M")

# Analyse des exclusivités vs multi-plateformes
st.markdown("### 🎯 Exclusivités vs Multi-plateformes")

# Compter le nombre de plateformes par jeu
game_platforms = filtered_df.groupby('Name')['Platform'].nunique().reset_index()
game_platforms.columns = ['Name', 'Platform_Count']

# Merge avec les données principales
exclusivity_data = filtered_df.merge(game_platforms, on='Name')
exclusivity_data['Type'] = exclusivity_data['Platform_Count'].apply(lambda x: 'Exclusivité' if x == 1 else 'Multi-plateforme')

# Analyse par type pour Nintendo
nintendo_exclusivity = exclusivity_data[exclusivity_data['Platform'].isin(nintendo_platforms)]
exclusivity_stats = nintendo_exclusivity.groupby('Type')['JP_Sales'].agg(['count', 'sum', 'mean']).reset_index()

fig_exclusivity = px.bar(
    exclusivity_stats, 
    x='Type', 
    y='sum',
    title="Ventes Nintendo : Exclusivités vs Multi-plateformes",
    labels={'sum': 'Ventes totales (millions)', 'Type': 'Type de jeu'},
    color='sum',
    color_continuous_scale='Blues'
)
st.plotly_chart(fig_exclusivity, use_container_width=True)

# Analyse de performance par plateforme Nintendo
st.markdown("### 📊 Performance des plateformes Nintendo")

nintendo_platform_stats = filtered_df[filtered_df['Platform'].isin(nintendo_platforms)].groupby('Platform').agg({
    'JP_Sales': ['sum', 'mean', 'count'],
    'Year': ['min', 'max']
}).round(2)

nintendo_platform_stats.columns = ['Ventes_Totales', 'Ventes_Moyennes', 'Nb_Jeux', 'Année_Min', 'Année_Max']
nintendo_platform_stats = nintendo_platform_stats.sort_values('Ventes_Totales', ascending=False)

st.dataframe(nintendo_platform_stats.style.format({
    'Ventes_Totales': '{:.2f}',
    'Ventes_Moyennes': '{:.3f}',
    'Nb_Jeux': '{:.0f}',
    'Année_Min': '{:.0f}',
    'Année_Max': '{:.0f}'
}), use_container_width=True)

# Conclusion dynamique
st.markdown("---")
st.markdown("## 🎯 Conclusion")

if nintendo_share > 50:
    st.success(f"""
    ✅ **Conclusion :** Oui, les joueurs japonais consomment majoritairement des jeux sur les consoles **Nintendo**, représentant **{nintendo_share:.1f}%** des ventes au Japon.
    
    **Détails :**
    - Nintendo domine avec {nintendo_sales:.1f} millions d'unités vendues
    - Cela représente {nintendo_share:.1f}% du marché japonais analysé
    - Les plateformes Nintendo les plus performantes sont : {', '.join(jp_sales_by_platform[jp_sales_by_platform['Constructeur'] == '🎮 Nintendo'].head(3)['Platform'].tolist())}
    """)
else:
    st.warning(f"""
    ❌ **Conclusion :** Non, les consoles Nintendo ne dominent pas les ventes au Japon. Elles représentent **{nintendo_share:.1f}%** du total.
    
    **Détails :**
    - Nintendo : {nintendo_sales:.1f} millions d'unités ({nintendo_share:.1f}%)
    - Leader actuel : {constructor_sales.iloc[0]['Constructeur']} avec {(constructor_sales.iloc[0]['JP_Sales']/total_jp_sales*100):.1f}%
    """)

# Insights supplémentaires
st.info(f"""
### 💡 Insights détaillés de l'analyse :
- **Période analysée :** {year_range[0]} - {year_range[1]}
- **Genre sélectionné :** {selected_genre}
- **Générations incluses :** {', '.join(generations)}
- **Seuil de ventes :** {min_sales} millions minimum
- **Nombre de jeux analysés :** {len(filtered_df)} jeux
- **Total des ventes au Japon :** {total_jp_sales:.1f} millions d'unités

### 🎮 Classement des constructeurs :
{chr(10).join([f"• {row['Constructeur']}: {row['JP_Sales']:.1f}M ({row['JP_Sales']/total_jp_sales*100:.1f}%)" for idx, row in constructor_sales.head(5).iterrows()])}

### 🏆 Plateformes Nintendo les plus performantes :
{chr(10).join([f"• {row['Platform']}: {row['JP_Sales']:.1f}M" for idx, row in jp_sales_by_platform[jp_sales_by_platform['Constructeur'] == '🎮 Nintendo'].head(3).iterrows()])}
""")

# Footer
st.markdown("---")
st.markdown("*Analyse réalisée avec Streamlit et Plotly - Focus sur le marché japonais du jeu vidéo*")