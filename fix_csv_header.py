# fix_csv_header.py
import os
import csv

INPUT_PATH = os.path.join("data", "tirages_euromillion.csv")
TEMP_PATH = os.path.join("data", "tirages_euromillion_clean.csv")
HEADER = ["Date", "Jour", "1", "2", "3", "4", "5", "Star 1", "Star 2", "Fichier", "Feuille"]

# Détecter la première ligne contenant une vraie date ISO
def is_valid_date(row):
    if not row:
        return False
    try:
        if len(row[0]) == 10 and row[0].count("-") == 2:
            return True
    except:
        pass
    return False

# Lecture + écriture avec nettoyage
with open(INPUT_PATH, "r", encoding="utf-8") as infile, open(TEMP_PATH, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    data_started = False
    for row in reader:
        if not data_started:
            if is_valid_date(row):
                writer.writerow(HEADER)
                data_started = True
                writer.writerow(row)
        elif data_started:
            writer.writerow(row)

# Remplacer l'ancien fichier par la version nettoyée
os.replace(TEMP_PATH, INPUT_PATH)
print(f"✅ En-tête CSV corrigé et enregistré dans : {INPUT_PATH}")
