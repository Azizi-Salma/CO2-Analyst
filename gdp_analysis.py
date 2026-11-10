
import pandas as pd
import plotly.express as px

# ==========================================
# 1. CHARGEMENT DES DONNEES
# ==========================================

url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

print("Chargement des donnees...")

df = pd.read_csv(url)

# ==========================================
# 2. NETTOYAGE DES DONNEES
# ==========================================

# Garder uniquement les codes ISO des pays a 3 lettres
df = df[
    df["iso_code"].str.fullmatch(r"[A-Z]{3}", na=False)
].copy()

# Selectionner uniquement l'annee 2022
df = df[df["year"] == 2022].copy()

# Garder les observations avec les donnees necessaires
df = df.dropna(
    subset=["gdp", "population", "co2_per_capita"]
)

# Eliminer les valeurs nulles ou negatives
df = df[
    (df["population"] > 0) &
    (df["gdp"] > 0) &
    (df["co2_per_capita"] >= 0)
].copy()

print("\nNombre de pays analyses :", df["country"].nunique())

# ==========================================
# 3. CALCUL DU PIB PAR HABITANT
# ==========================================

df["gdp_per_capita"] = df["gdp"] / df["population"]

print("\nAPERÇU DES DONNEES :")

print(
    df[
        ["country", "gdp_per_capita", "co2_per_capita"]
    ].head(10).to_string(index=False)
)

# ==========================================
# 4. CALCUL DE LA CORRELATION
# ==========================================

correlation = df["gdp_per_capita"].corr(
    df["co2_per_capita"]
)

print("\nCORRELATION ENTRE PIB ET CO2 :")
print(round(correlation, 3))

# ==========================================
# 5. CREATION DU GRAPHIQUE
# ==========================================

fig = px.scatter(
    df,
    x="gdp_per_capita",
    y="co2_per_capita",
    hover_name="country",
    size="population",
    color="co2_per_capita",
    title="Relation entre PIB par habitant et emissions de CO2 (2022)",
    labels={
        "gdp_per_capita": "PIB par habitant (dollars)",
        "co2_per_capita": "CO2 par habitant (tonnes)",
        "population": "Population"
    },
    log_x=True,
    color_continuous_scale="Reds"
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    hovermode="closest"
)

fig.show()

# ==========================================
# 6. INTERPRETATION DES RESULTATS
# ==========================================

print("\nINTERPRETATION :")

if correlation >= 0.7:
    print("Forte correlation positive.")
elif correlation >= 0.3:
    print("Correlation positive moderee.")
elif correlation > 0:
    print("Faible correlation positive.")
elif correlation <= -0.7:
    print("Forte correlation negative.")
elif correlation <= -0.3:
    print("Correlation negative moderee.")
else:
    print("Correlation faible ou proche de zero.")

print("\nAttention : correlation ne signifie pas causalite.")

print("\nAnalyse terminee avec succes !")
