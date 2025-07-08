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

# Titre principal
st.markdown("# 🎮 Les jeux d'action sont-ils les plus vendus dans le monde ❓")
st.markdown("---")

# Chargement des données
df = pd.read_csv("datasets/vgsales.csv")

# Nettoyage basique si besoin
df = df.dropna(subset=["Genre", "Global_Sales"])

# Explication de la démarche
st.info("""
### 🔎 Objectif de l'analyse :
Nous allons analyser les ventes mondiales (`Global_Sales`) par **genre de jeu** afin de déterminer si les jeux d'action (**Action**) sont effectivement les plus vendus à l'échelle mondiale.
""")

# Agrégation des ventes par genre
sales_by_genre = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False).reset_index()

# Affichage du tableau
st.markdown("### 📋 Classement des genres par ventes mondiales")
st.dataframe(sales_by_genre.style.format({"Global_Sales": "{:.2f}"}), use_container_width=True)

# Affichage du graphique avec matplotlib
st.markdown("### 📊 Visualisation des ventes globales par genre")
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(sales_by_genre["Genre"], sales_by_genre["Global_Sales"], color="skyblue")
ax.invert_yaxis()  # Pour avoir le genre le plus vendu en haut
ax.set_xlabel("Ventes globales (en millions)")
ax.set_ylabel("Genre")
ax.set_title("Ventes mondiales par genre de jeu")

# Afficher les valeurs sur les barres
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2, f"{width:.2f}", va='center')

st.pyplot(fig)

# Conclusion dynamique
top_genre = sales_by_genre.iloc[0]["Genre"]
top_sales = sales_by_genre.iloc[0]["Global_Sales"]

if top_genre.lower() == "action":
    st.success(f"""
✅ **Conclusion :** Oui, les jeux d'**action** sont les plus vendus dans le monde, avec un total de **{top_sales:.2f} millions** d’unités vendues.
""")
else:
    st.warning(f"""
❌ **Conclusion :** Non, les jeux d'**action** ne sont pas les plus vendus. Le genre le plus vendu est **{top_genre}** avec **{top_sales:.2f} millions** d’unités.
""")
