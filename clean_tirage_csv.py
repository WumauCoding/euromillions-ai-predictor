import pandas as pd
from pathlib import Path

DATA_FILE = Path("data/tirages_euromillion.csv")
OUTPUT_FILE = Path("data/tirages_euromillion_clean.csv")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Trouve la ligne d’en-tête (commence par "Date,")
header_index = next((i for i, line in enumerate(lines) if line.strip().startswith("Date,")), None)

if header_index is None:
    print("❌ Impossible de trouver la ligne d'en-tête contenant 'Date,'.")
    exit(1)

# Recrée un CSV propre à partir de cette ligne
clean_lines = lines[header_index:]
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.writelines(clean_lines)

# Lecture dans pandas avec nommage propre
df = pd.read_csv(OUTPUT_FILE)

# Renommer les colonnes utiles
df = df.rename(columns={
    df.columns[0]: "Date",
    df.columns[1]: "Jour",
    df.columns[2]: "B1",
    df.columns[3]: "B2",
    df.columns[4]: "B3",
    df.columns[5]: "B4",
    df.columns[6]: "B5",
    df.columns[7]: "E1",
    df.columns[8]: "E2"
})

# Ne garde que les colonnes essentielles
df = df[["Date", "Jour", "B1", "B2", "B3", "B4", "B5", "E1", "E2"]]

# Enregistrement
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Fichier nettoyé exporté vers : {OUTPUT_FILE}")
