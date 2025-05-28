import pandas as pd
import os

# Dossier contenant tous les fichiers XLS
folder = f"/home/{USER}/euromillions/"  # remplace par le vrai chemin
import os

# Détection du nom d'utilisateur
USER = os.getenv("USER") or os.getenv("USERNAME") or "wumix"
EXPORT_PATH = f"/home/{USER}/tirages_euromillion.csv"


all_draws = []

for file in os.listdir(folder):
    if file.endswith(".xls"):
        xls = pd.ExcelFile(os.path.join(folder, file), engine="xlrd")
        for sheet in xls.sheet_names:
            df = xls.parse(sheet)
            df["Fichier"] = file
            df["Feuille"] = sheet
            all_draws.append(df)

# Fusion de tous les tirages
combined = pd.concat(all_draws, ignore_index=True)
combined.to_csv(EXPORT_PATH, index=False)
print("Exporté vers tirages_combines.xlsx")
