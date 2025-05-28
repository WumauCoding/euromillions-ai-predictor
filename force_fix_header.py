# force_fix_header.py
import csv
import os
import re

input_file = "data/tirages_euromillion.csv"
output_file = "data/tirages_euromillion_fixed.csv"
expected_header = ["Date", "Jour", "1", "2", "3", "4", "5", "Star 1", "Star 2", "Fichier", "Feuille"]

found_data = False

with open(input_file, encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
    reader = csv.reader(infile, delimiter=";")
    writer = csv.writer(outfile, delimiter=";")

    for row in reader:
        # Détecte une ligne qui commence par une date YYYY-MM-DD
        if len(row) >= 5 and re.match(r"\d{4}-\d{2}-\d{2}", row[0]):
            writer.writerow(expected_header)
            writer.writerow(row)
            found_data = True
            break

    if not found_data:
        print("❌ Aucune ligne de données valide trouvée (avec date au format AAAA-MM-JJ).")
        exit(1)

    for row in reader:
        writer.writerow(row)

# Remplacer l'ancien fichier
os.replace(output_file, input_file)
print("✅ En-tête corrigé avec succès dans :", input_file)
