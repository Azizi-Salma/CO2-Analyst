
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

df = df[df["iso_code"].notna()]
df = df[df["year"].between(2000, 2024)]

# Garder uniquement les pays selectionnes
countries = ["Morocco", "France", "China", "United States"]

comparison = df[df["country"].isin(countries)].copy()

# Supprimer les valeurs manquantes
comparison = comparison.dropna(subset=["co2_per_capita"])

# ==========================================
# 3. AFFICHER LES DONNEES
# ==========================================

print("\nAPERÇU DES DONNEES :")

print(
    comparison[
        ["country", "year", "co2_per_capita"]
    ].groupby("country").head(3).to_string(index=False)
)

# ==========================================
# 4. COMPARAISON ENTRE 2000 ET 2024
# ==========================================

start = comparison[comparison["year"] == 2000][
    ["country", "co2_per_capita"]
].rename(columns={"co2_per_capita": "CO2_2000"})

end = comparison[comparison["year"] == 2024][
    ["country", "co2_per_capita"]
].rename(columns={"co2_per_capita": "CO2_2024"})

result = start.merge(end, on="country", how="inner")

# Calcul du pourcentage d'evolution
result["evolution_%"] = (
    (result["CO2_2024"] - result["CO2_2000"])
    / result["CO2_2000"]
) * 100

print("\nEVOLUTION DES EMISSIONS ENTRE 2000 ET 2024 :")

print(result.round(2).to_string(index=False))

# ==========================================
# 5. GRAPHIQUE D'EVOLUTION
# ==========================================

fig = px.line(
    comparison,
    x="year",
    y="co2_per_capita",
    color="country",
    markers=True,
    title="Evolution des emissions de CO2 par habitant (2000-2024)",
    labels={
        "year": "Annee",
        "co2_per_capita": "Tonnes de CO2 par habitant",
        "country": "Pays"
    }
)

fig.update_layout(
    template="plotly_white",
    title_x=0.5,
    hovermode="x unified"
)

fig.show()

# ==========================================
# 6. CONCLUSION AUTOMATIQUE
# ==========================================

print("\nCONCLUSION :")

if not result.empty:
    best_country = result.loc[
        result["evolution_%"].idxmin()
    ]

    print(
        f"{best_country['country']} a connu "
        f"la plus forte baisse relative des emissions "
        f"entre 2000 et 2024 : "
        f"{best_country['evolution_%']:.2f}%."
    )
else:
    print("Impossible de comparer les pays : donnees insuffisantes.")

print("\nAnalyse terminee avec succes !")
