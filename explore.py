
import pandas as pd

url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

df = pd.read_csv(url)

# 1. Garder uniquement les pays
df = df[df["iso_code"].notna()]

# 2. Garder les années à partir de 1950
df = df[df["year"] >= 1950]

# 3. Afficher les informations après nettoyage
print("Dimensions après nettoyage :", df.shape)

print("\nPremières lignes :")
print(df[["country", "year", "population", "gdp", "co2", "co2_per_capita"]].head())

print("\nPériode disponible :")
print(df["year"].min(), "-", df["year"].max())

print("\nNombre de pays :")
print(df["country"].nunique())
