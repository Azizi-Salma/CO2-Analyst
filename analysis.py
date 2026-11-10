
import pandas as pd
import plotly.express as px

# ==========================================
# 1. CHARGEMENT ET NETTOYAGE
# ==========================================

url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df = pd.read_csv(url)

df = df[
    df["iso_code"].str.match(r"^[A-Z]{3}$", na=False)
    & (df["year"] >= 1950)
].copy()

print("Dataset chargé :", len(df), "lignes")


# ==========================================
# 2. TOP 10 DES EMETTEURS EN 2022
# ==========================================

df_2022 = df[df["year"] == 2022].dropna(subset=["co2"])

top10 = df_2022.nlargest(10, "co2").copy()

total_emissions = df_2022["co2"].sum()
total_top10 = top10["co2"].sum()
percentage = total_top10 / total_emissions * 100

print("\n=== ANALYSE 1 : TOP 10 EN 2022 ===")

print(top10[["country", "co2", "co2_per_capita"]].to_string(index=False))

print("Total émissions :", round(total_emissions, 2), "Mt")
print("Total Top 10 :", round(total_top10, 2), "Mt")
print("Part Top 10 :", round(percentage, 2), "%")

fig1 = px.bar(
    top10.sort_values("co2"),
    x="co2",
    y="country",
    orientation="h",
    text="co2",
    title="Top 10 des pays émetteurs de CO2 en 2022",
    labels={"co2": "Émissions (Mt)", "country": "Pays"},
    color="co2",
    color_continuous_scale="Teal"
)

fig1.update_layout(template="plotly_dark", showlegend=False)
fig1.update_traces(texttemplate="%{text:,.0f} Mt", textposition="outside")
fig1.write_html("top10_co2_2022.html")
fig1.show()


# ==========================================
# 3. EVOLUTION DU CO2 AU MAROC
# ==========================================

morocco = df[
    (df["country"] == "Morocco")
    & (df["year"].between(2000, 2024))
].dropna(subset=["co2_per_capita"]).sort_values("year").copy()

first_value = morocco.iloc[0]["co2_per_capita"]
last_value = morocco.iloc[-1]["co2_per_capita"]

variation = (last_value - first_value) / first_value * 100

print("\n=== ANALYSE 2 : EVOLUTION AU MAROC ===")
print(morocco[["year", "co2_per_capita"]].to_string(index=False))
print("Début :", round(first_value, 2), "tonnes")
print("Fin :", round(last_value, 2), "tonnes")
print("Variation :", round(variation, 2), "%")

fig2 = px.line(
    morocco,
    x="year",
    y="co2_per_capita",
    markers=True,
    title="Evolution du CO2 par habitant au Maroc (2000-2024)",
    labels={
        "year": "Année",
        "co2_per_capita": "CO2 par habitant (tonnes)"
    }
)

fig2.update_layout(template="plotly_dark")
fig2.write_html("morocco_co2_evolution.html")
fig2.show()


# ==========================================
# 4. COMPARAISON ENTRE 4 PAYS
# ==========================================

countries = ["Morocco", "France", "China", "United States"]

comparison = df[
    df["country"].isin(countries)
    & (df["year"].between(2000, 2024))
].dropna(subset=["co2_per_capita"]).copy()

print("\n=== ANALYSE 3 : COMPARAISON ENTRE PAYS ===")

print(
    comparison.pivot(
        index="year",
        columns="country",
        values="co2_per_capita"
    ).tail(5).to_string()
)

fig3 = px.line(
    comparison,
    x="year",
    y="co2_per_capita",
    color="country",
    markers=True,
    title="Comparaison des émissions de CO2 par habitant (2000-2024)",
    labels={
        "year": "Année",
        "co2_per_capita": "CO2 par habitant (tonnes)",
        "country": "Pays"
    }
)

fig3.update_layout(
    template="plotly_dark",
    xaxis_title="Année",
    yaxis_title="Tonnes de CO2 par habitant"
)

fig3.write_html("comparison_countries.html")
fig3.show()


print("\n=== LES 3 ANALYSES SONT TERMINEES ===")
