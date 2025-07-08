import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="Vente de jeux vidéo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titre
st.markdown("# 🇯🇵 Les joueurs japonais consomment-ils principalement des jeux sur les consoles Nintendo ❓")
st.markdown("---")

# Chargement du dataset
df = pd.read_csv("datasets/vgsales.csv")

# Nettoyage (valeurs manquantes sur JP_Sales et Platform)
df = df.dropna(subset=["Platform", "JP_Sales"])

# Explication de l'objectif
st.info("""
### 🔎 Objectif de l'analyse :
Nous allons analyser les ventes **au Japon** (`JP_Sales`) en fonction des **plateformes de jeux** pour déterminer si les consoles **Nintendo** dominent le marché japonais.
""")

# Liste des plateformes Nintendo (selon les données connues)
nintendo_platforms = ["DS", "3DS", "Wii", "WiiU", "GBA", "GC", "Switch", "SNES", "NES", "N64"]

# Agrégation des ventes japonaises par plateforme
jp_sales_by_platform = df.groupby("Platform")["JP_Sales"].sum().sort_values(ascending=False).reset_index()

# Ajout d’une colonne "Marque"
jp_sales_by_platform["Constructeur"] = jp_sales_by_platform["Platform"].apply(
    lambda x: "Nintendo" if x in nintendo_platforms else "Autre"
)

# Calcul total ventes Nintendo vs Autres au Japon
nintendo_vs_others = jp_sales_by_platform.groupby("Constructeur")["JP_Sales"].sum().reset_index()

# Affichage du tableau complet par plateforme
st.markdown("### 📋 Ventes au Japon par plateforme")
st.dataframe(jp_sales_by_platform.style.format({"JP_Sales": "{:.2f}"}), use_container_width=True)

# Visualisation par constructeur
st.markdown("### 📊 Répartition des ventes au Japon : Nintendo vs autres")
fig, ax = plt.subplots(figsize=(6, 4))
colors = ["lightgreen", "lightcoral"]
ax.pie(nintendo_vs_others["JP_Sales"], labels=nintendo_vs_others["Constructeur"], autopct='%1.1f%%', startangle=140, colors=colors)
ax.axis('equal')
st.pyplot(fig)

# Conclusion dynamique
nintendo_sales = nintendo_vs_others[nintendo_vs_others["Constructeur"] == "Nintendo"]["JP_Sales"].values[0]
total_sales = nintendo_vs_others["JP_Sales"].sum()
nintendo_share = (nintendo_sales / total_sales) * 100

if nintendo_share > 50:
    st.success(f"""
✅ **Conclusion :** Oui, les joueurs japonais consomment majoritairement des jeux sur les consoles **Nintendo**, représentant **{nintendo_share:.2f}%** des ventes au Japon.
""")
else:
    st.warning(f"""
❌ **Conclusion :** Non, les consoles Nintendo ne dominent pas les ventes au Japon. Elles représentent **{nintendo_share:.2f}%** du total.
""")
