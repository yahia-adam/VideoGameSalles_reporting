import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Vente de jeux vidéo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
### **Objectif du projet**

L’objectif de ce projet est de réaliser une étude du **marché mondial des jeux vidéo** à partir d’un dataset issu du site vgchartz.com.

À travers une analyse exploratoire des données, ce projet vise à :

- Mieux comprendre la répartition des ventes de jeux vidéo à l’échelle mondiale.
- Identifier les tendances dominantes du marché (plateformes populaires, genres les plus vendus, zones géographiques les plus actives, etc.).
- Mettre en évidence les comportements de consommation selon les régions.
- Fournir des visualisations claires et des statistiques pertinentes pour éclairer les décisions liées à l'industrie du jeu vidéo.
""")

st.markdown("---")
st.markdown("### 🎮 **Présentation du Dataset**")

st.markdown("""
Le dataset utilisé dans ce projet provient du site [vgchartz.com](https://www.vgchartz.com), une base de données spécialisée dans le suivi des ventes de jeux vidéo. Il regroupe **16 598 jeux** ayant dépassé les **100 000 exemplaires vendus** à travers le monde.

Chaque ligne du dataset correspond à un jeu vidéo, avec des informations commerciales, techniques et géographiques. Il permet ainsi d'étudier l’évolution du marché du jeu vidéo, les préférences des consommateurs selon les régions, et les succès commerciaux des éditeurs et plateformes.

#### **Structure détaillée du dataset :**

- **`Rank`** : *Classement mondial* du jeu en fonction des ventes globales (1 = jeu le plus vendu).
- **`Name`** : *Nom du jeu vidéo*.
- **`Platform`** : *Plateforme principale* sur laquelle le jeu a été publié (ex. PS2, Xbox 360, PC, Wii...).
- **`Year`** : *Année de sortie* du jeu. Certaines valeurs peuvent être manquantes ou imprécises.
- **`Genre`** : *Genre du jeu* (Action, Sport, Stratégie, Simulation, etc.).
- **`Publisher`** : *Éditeur du jeu*, c’est-à-dire la société responsable de sa commercialisation.
- **`NA_Sales`** : *Ventes en Amérique du Nord* (en millions d’unités).
- **`EU_Sales`** : *Ventes en Europe* (en millions d’unités).
- **`JP_Sales`** : *Ventes au Japon* (en millions d’unités).
- **`Other_Sales`** : *Ventes dans les autres régions* du monde (en millions d’unités).
- **`Global_Sales`** : *Ventes mondiales totales* (somme des quatre régions précédentes, en millions d’unités).
---
""")

st.markdown("#### **Aperçu du dataset**")
df = pd.read_csv("datasets/vgsales.csv")
st.dataframe(df)


st.markdown("---")
st.markdown("""
### ❓ **Hypothèses à vérifier**

1. **Les jeux d'action sont-ils les plus vendus dans le monde ?**  
   → Cette hypothèse vise à déterminer si le genre *Action* domine le marché mondial en termes de ventes globales.

2. **Les États-Unis représentent-ils la plus grande part de consommation de jeux vidéo ?**  
   → Nous chercherons à savoir si l’Amérique du Nord (NA_Sales) est la région où les jeux se vendent le plus.

3. **Les joueurs japonais consomment-ils principalement des jeux sur les consoles Nintendo ?**  
   → Cette hypothèse explore la préférence du marché japonais pour les plateformes Nintendo (comme la DS, Wii, Switch...).
""")


st.markdown("---")
