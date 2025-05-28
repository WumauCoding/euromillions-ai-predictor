#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import random
from datetime import datetime
from collections import Counter

# Chemins relatifs des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(BASE_DIR, "data", "tirages_euromillion.csv")
output_file = os.path.join(BASE_DIR, "results", "quantum_states.csv")

# S'assurer que le répertoire de résultats existe
os.makedirs(os.path.join(BASE_DIR, "results"), exist_ok=True)

# Charger et parser les tirages historiques depuis le CSV
draws = []
with open(data_file, encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(',')
        if parts and re.match(r'^\d{4}-\d{2}-\d{2}$', parts[0]):
            date_str = parts[0]
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            except Exception:
                continue
            main_numbers = [int(float(x)) for x in parts[2:7]]
            star_numbers = [int(float(x)) for x in parts[7:9]]
            draws.append((date_obj, main_numbers, star_numbers))

# Trier les tirages par date pour calculer correctement les retards
draws.sort(key=lambda x: x[0])

# Calculer fréquences et retards des numéros sur l'ensemble des tirages
freq_main = Counter()
freq_star = Counter()
last_index_main = {n: -1 for n in range(1, 51)}
last_index_star = {s: -1 for s in range(1, 13)}
for idx, (_, main_nums, star_nums) in enumerate(draws):
    freq_main.update(main_nums)
    freq_star.update(star_nums)
    for n in main_nums:
        last_index_main[n] = idx
    for s in star_nums:
        last_index_star[s] = idx

total_draws = len(draws)
delay_main = {n: total_draws - 1 - last_index_main[n] if total_draws > 0 else 0 for n in range(1, 51)}
delay_star = {s: total_draws - 1 - last_index_star[s] if total_draws > 0 else 0 for s in range(1, 13)}

# Calculer les poids de chaque numéro (somme fréquence + retard) pour la pondération
weight_main = {n: freq_main[n] + delay_main[n] for n in range(1, 51)}
weight_star = {s: freq_star[s] + delay_star[s] for s in range(1, 13)}

# Préparer les listes de numéros et leurs poids correspondants
nums_main = list(range(1, 51))
nums_star = list(range(1, 13))
weights_main = [weight_main[n] for n in nums_main]
weights_star = [weight_star[s] for s in nums_star]

# Générer 5000 combinaisons aléatoires optimisées (pondérées par les poids)
combos_counter = Counter()  # Compteur pour les combinaisons générées
for _ in range(5000):
    # Sélection pondérée des 5 numéros principaux sans répétition
    available_nums = nums_main[:]       # liste des numéros disponibles
    available_weights = weights_main[:] # liste des poids correspondants
    chosen_main = []
    for _ in range(5):
        # Tirage aléatoire pondéré d'un numéro parmi les disponibles
        total_w = sum(available_weights)
        r = random.random() * total_w
        cum_w = 0.0
        chosen_index = 0
        for i, w in enumerate(available_weights):
            cum_w += w
            if r <= cum_w:
                chosen_index = i
                break
        # Ajouter le numéro choisi et le retirer des disponibles
        chosen_number = available_nums.pop(chosen_index)
        available_weights.pop(chosen_index)
        chosen_main.append(chosen_number)
    # Sélection pondérée des 2 étoiles sans répétition
    available_stars = nums_star[:]
    available_star_weights = weights_star[:]
    chosen_stars = []
    for _ in range(2):
        total_w = sum(available_star_weights)
        r = random.random() * total_w
        cum_w = 0.0
        chosen_index = 0
        for j, w in enumerate(available_star_weights):
            cum_w += w
            if r <= cum_w:
                chosen_index = j
                break
        chosen_star = available_stars.pop(chosen_index)
        available_star_weights.pop(chosen_index)
        chosen_stars.append(chosen_star)
    # Trier les numéros choisis pour représenter la combinaison de manière unique
    chosen_main.sort()
    chosen_stars.sort()
    # Enregistrer la combinaison (tuples immuables) dans le compteur
    combo_key = (tuple(chosen_main), tuple(chosen_stars))
    combos_counter[combo_key] += 1

# Normaliser les scores des combinaisons en probabilités
total_combinations = sum(combos_counter.values())  # devrait être 5000
# Trier les combinaisons par fréquence décroissante pour lisibilité
combo_items = sorted(combos_counter.items(), key=lambda item: item[1], reverse=True)

# Écrire les états quantiques dans le fichier CSV de sortie
with open(output_file, "w", encoding="utf-8") as fout:
    # En-tête : 5 numéros, 2 étoiles, et la probabilité de l'état
    fout.write(",".join([f"N{i}" for i in range(1, 6)]) + ",Star1,Star2,Probability\n")
    for (main_tuple, star_tuple), count in combo_items:
        # Calculer la probabilité de la combinaison (fréquence / total)
        probability = count / total_combinations
        # Écrire la ligne CSV : chaque numéro dans sa colonne, puis la probabilité formatée
        fout.write(",".join(map(str, main_tuple)) + "," + ",".join(map(str, star_tuple)) + f",{probability:.6f}\n")

print(f"États quantiques générés dans {output_file}")
