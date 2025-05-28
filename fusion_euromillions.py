import pandas as pd
import os

# === CONFIGURATION ===
DOSSIER_XLS = "/home/wumix/euromillions/data"  # ✅ Correction ici
USER = os.getenv("USER") or os.getenv("USERNAME") or "wumix"
EXPORT_PATH = f"/home/{USER}/euromillions/data/tirages_euromillion.csv"

# === INITIALISATION ===
all_draws = []

# === PARCOURS DES FICHIERS ===
for fichier in os.listdir(DOSSIER_XLS):
    if fichier.endswith(".xls") or fichier.endswith(".xlsx"):
        chemin_fichier = os.path.join(DOSSIER_XLS, fichier)
        try:
            xls = pd.ExcelFile(chemin_fichier, engine="xlrd")
        except:
            try:
                xls = pd.ExcelFile(chemin_fichier, engine="openpyxl")
            except:
                print(f"❌ Erreur lors de la lecture : {fichier}")
                continue

        for feuille in xls.sheet_names:
            df = xls.parse(feuille)
            df["Fichier"] = fichier
            df["Feuille"] = feuille
            all_draws.append(df)

# === CONCATÉNATION ET EXPORT ===
if all_draws:
    fusion = pd.concat(all_draws, ignore_index=True)
    fusion.drop_duplicates(inplace=True)
    fusion.to_csv(EXPORT_PATH, index=False)
    print(f"✅ Données combinées exportées dans : {EXPORT_PATH}")
else:
    print("⚠️ Aucun tirage trouvé.")
