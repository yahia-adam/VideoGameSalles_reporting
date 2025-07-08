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
st.markdown("# 🌍 Les États-Unis représentent-ils la plus grande part de consommation de jeux vidéo ❓")
st.markdown("---")

# Chargement du dataset
df = pd.read_csv("datasets/vgsales.csv")

# Nettoyage de base (on enlève les valeurs manquantes sur les colonnes de ventes régionales)
df = df.dropna(subset=["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"])

# Explication
st.info("""
### 🔎 Objectif de l'analyse :
Comparer les ventes régionales de jeux vidéo afin de savoir si **l’Amérique du Nord (NA_Sales)** est la région où les jeux se vendent le plus.
""")

# Agrégation des ventes par région
regional_sales = {
    "Amérique du Nord (NA)": df["NA_Sales"].sum(),
    "Europe (EU)": df["EU_Sales"].sum(),
    "Japon (JP)": df["JP_Sales"].sum(),
    "Autres régions": df["Other_Sales"].sum()
}

# Conversion en DataFrame
sales_df = pd.DataFrame.from_dict(regional_sales, orient='index', columns=["Ventes (en millions)"])
sales_df = sales_df.sort_values(by="Ventes (en millions)", ascending=False).reset_index()
sales_df.columns = ["Région", "Ventes (en millions)"]

# Affichage du tableau
st.markdown("### 📋 Ventes totales par région")
st.dataframe(sales_df.style.format({"Ventes (en millions)": "{:.2f}"}), use_container_width=True)

# Visualisation graphique
st.markdown("### 📊 Répartition des ventes mondiales par région")
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(sales_df["Région"], sales_df["Ventes (en millions)"], color="cornflowerblue")
ax.set_ylabel("Ventes (en millions)")
ax.set_title("Ventes régionales de jeux vidéo")
st.pyplot(fig)

# Conclusion dynamique
top_region = sales_df.iloc[0]["Région"]
top_value = sales_df.iloc[0]["Ventes (en millions)"]

if "NA" in top_region:
    st.success(f"""
✅ **Conclusion :** Oui, l'**Amérique du Nord** est la plus grande consommatrice de jeux vidéo, avec un total de **{top_value:.2f} millions** d’unités vendues.
""")
else:
    st.warning(f"""
❌ **Conclusion :** Non, l'Amérique du Nord n’est pas la plus grande consommatrice. C’est **{top_region}** qui arrive en tête avec **{top_value:.2f} millions** d’unités.
""")
