#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
from collections import Counter

# Définir les chemins relatifs des fichiers de données et de résultats
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(BASE_DIR, "data", "tirages_euromillion.csv")
output_file = os.path.join(BASE_DIR, "results", "grilles_prediction.csv")

# S'assurer que le dossier de résultats existe
os.makedirs(os.path.join(BASE_DIR, "results"), exist_ok=True)

# Initialiser les structures de données
draws = []  # Liste des tirages sous la forme (date, [nums_main], [nums_star])

# Charger et parser le fichier CSV des tirages historiques
with open(data_file, encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(',')
        # Identifier les lignes de tirage par un format de date AAAA-MM-JJ en début de ligne
        if parts and re.match(r'^\d{4}-\d{2}-\d{2}$', parts[0]):
            date_str = parts[0]
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except Exception:
                # Si la date n'est pas au format ISO, ignorer la ligne
                continue
            # Les 5 numéros principaux se trouvent aux colonnes 3 à 7 (index 2 à 6)
            main_numbers = [int(float(x)) for x in parts[2:7]]
            # Les 2 étoiles se trouvent aux colonnes 8 à 9 (index 7 à 8)
            star_numbers = [int(float(x)) for x in parts[7:9]]
            draws.append((date_obj, main_numbers, star_numbers))

# Trier les tirages par date croissante pour un traitement chronologique
draws.sort(key=lambda x: x[0])

# Calculer la fréquence de chaque numéro principal et étoile
freq_main = Counter()
freq_star = Counter()
for _, main_nums, star_nums in draws:
    freq_main.update(main_nums)
    freq_star.update(star_nums)

# Calculer le retard de chaque numéro (nombre de tirages depuis la dernière apparition)
last_index_main = {n: -1 for n in range(1, 51)}   # dernier index de tirage vu pour chaque numéro principal
last_index_star = {s: -1 for s in range(1, 13)}   # dernier index de tirage vu pour chaque étoile
for idx, (_, main_nums, star_nums) in enumerate(draws):
    for n in main_nums:
        last_index_main[n] = idx
    for s in star_nums:
        last_index_star[s] = idx

total_draws = len(draws)
delay_main = {}  # retard des numéros principaux
delay_star = {}  # retard des étoiles
for n in range(1, 51):
    # Si un numéro n'est jamais sorti, last_index_main[n] = -1 => retard = total_draws (tous les tirages écoulés sans le voir)
    delay_main[n] = total_draws - 1 - last_index_main[n] if total_draws > 0 else 0
for s in range(1, 13):
    delay_star[s] = total_draws - 1 - last_index_star[s] if total_draws > 0 else 0

# Calculer le score combiné Fréquence + Retard pour chaque numéro
score_main = {n: freq_main[n] + delay_main[n] for n in range(1, 51)}
score_star = {s: freq_star[s] + delay_star[s] for s in range(1, 13)}

# Construire la matrice de transitions markoviennes pour les numéros principaux et étoiles
trans_main = [[0] * 51 for _ in range(51)]  # trans_main[x][y] = occurrences de y après x (numéros principaux)
trans_star = [[0] * 13 for _ in range(13)]  # trans_star[a][b] = occurrences de b après a (étoiles)
for i in range(len(draws) - 1):
    main_cur = draws[i][1]    # numéros du tirage courant
    star_cur = draws[i][2]    # étoiles du tirage courant
    main_next = draws[i+1][1]  # numéros du tirage suivant
    star_next = draws[i+1][2]  # étoiles du tirage suivant
    # Incrémenter les transitions pour chaque paire (x dans tirage i, y dans tirage i+1)
    for x in main_cur:
        for y in main_next:
            trans_main[x][y] += 1
    for a in star_cur:
        for b in star_next:
            trans_star[a][b] += 1

# Récupérer le dernier tirage de l'historique (état actuel)
last_draw_main = draws[-1][1] if draws else []
last_draw_star = draws[-1][2] if draws else []

# Calculer le score markovien pour chaque numéro en fonction du dernier tirage connu
markov_score_main = {n: 0 for n in range(1, 51)}
markov_score_star = {s: 0 for s in range(1, 13)}
for x in last_draw_main:
    for y in range(1, 51):
        markov_score_main[y] += trans_main[x][y]
for a in last_draw_star:
    for b in range(1, 13):
        markov_score_star[b] += trans_star[a][b]

# Sélectionner les meilleurs numéros selon chaque méthode
# Top 5 numéros principaux et top 2 étoiles pour la méthode Fréquence+Retard
best5_freq_delay = sorted(score_main.keys(), key=lambda n: score_main[n], reverse=True)[:5]
best2_freq_delay_star = sorted(score_star.keys(), key=lambda s: score_star[s], reverse=True)[:2]
# Top 5 numéros principaux et top 2 étoiles pour la méthode Markov
best5_markov = sorted(markov_score_main.keys(), key=lambda n: markov_score_main[n], reverse=True)[:5]
best2_markov_star = sorted(markov_score_star.keys(), key=lambda s: markov_score_star[s], reverse=True)[:2]

# Trier les numéros sélectionnés dans l'ordre croissant pour l'affichage
best5_freq_delay.sort()
best2_freq_delay_star.sort()
best5_markov.sort()
best2_markov_star.sort()

# Écrire les grilles prédictives dans le fichier CSV de sortie
with open(output_file, "w", encoding="utf-8") as fout:
    # En-tête CSV
    fout.write("Method," + ",".join([f"N{i}" for i in range(1, 6)]) + ",Star1,Star2\n")
    # Grille basée sur Fréquence+Retard
    fout.write("Freq+Retard," + ",".join(map(str, best5_freq_delay)) + "," + ",".join(map(str, best2_freq_delay_star)) + "\n")
    # Grille basée sur Markov
    fout.write("Markov," + ",".join(map(str, best5_markov)) + "," + ",".join(map(str, best2_markov_star)) + "\n")

print(f"Grilles prédictives générées dans {output_file}")
    