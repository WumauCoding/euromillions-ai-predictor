#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import argparse
from datetime import datetime
from collections import Counter

# Configuration de l'argument d'année (par défaut 2022)
parser = argparse.ArgumentParser(description="Simulation de pr\u00e9dictions pour une ann\u00e9e donn\u00e9e (backtest).")
parser.add_argument("year", type=int, nargs='?', default=2022, help="Ann\u00e9e \u00e0 tester (par exemple 2022).")
args = parser.parse_args()
YEAR = args.year

# Chemins relatifs des fichiers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(BASE_DIR, "data", "tirages_euromillion.csv")
output_file = os.path.join(BASE_DIR, "logs", f"backtest_{YEAR}.csv")

# S'assurer que le dossier de logs existe
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

# Charger et trier tous les tirages historiques
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
# Trier par date croissante
draws.sort(key=lambda x: x[0])

# Trouver les indices de d\u00e9but et de fin pour l'ann\u00e9e choisie
start_index = None
end_index = None
for i, (date_obj, _, _) in enumerate(draws):
    if date_obj.year == YEAR and start_index is None:
        start_index = i
    if start_index is not None and date_obj.year != YEAR:
        end_index = i - 1
        break
if start_index is None:
    print(f"Aucun tirage trouv\u00e9 pour l'ann\u00e9e {YEAR}.")
    exit(1)
if end_index is None:
    end_index = len(draws) - 1  # jusqu'\u00e0 la fin si l'ann\u00e9e choisie est la derni\u00e8re pr\u00e9sente

# Pr\u00e9parer le contenu CSV avec un en-t\u00eate
lines = []
header = "Date,Tirage,Pred_FreqRetard,Hits_main_FD,Hits_star_FD,Pred_Markov,Hits_main_M,Hits_star_M"
lines.append(header)

# Boucle sur chaque tirage de l'ann\u00e9e cible
for idx in range(start_index, end_index + 1):
    # S'assurer qu'il existe des tirages pr\u00e9c\u00e9dents (sinon on ne peut pas pr\u00e9dire)
    if idx == 0:
        continue

    current_date, actual_main, actual_stars = draws[idx]
    # R\u00e9cup\u00e9rer tous les tirages avant celui-ci (jusqu'\u00e0 idx-1)
    past_draws = draws[:idx]

    # Calculer les fr\u00e9quences et retards sur les tirages pass\u00e9s
    freq_main = Counter()
    freq_star = Counter()
    last_index_main = {n: -1 for n in range(1, 51)}
    last_index_star = {s: -1 for s in range(1, 13)}
    for j, (_, main_nums, star_nums) in enumerate(past_draws):
        freq_main.update(main_nums)
        freq_star.update(star_nums)
        for n in main_nums:
            last_index_main[n] = j
        for s in star_nums:
            last_index_star[s] = j

    total_past = len(past_draws)
    delay_main = {n: total_past - 1 - last_index_main[n] if total_past > 0 else 0 for n in range(1, 51)}
    delay_star = {s: total_past - 1 - last_index_star[s] if total_past > 0 else 0 for s in range(1, 13)}

    score_main = {n: freq_main[n] + delay_main[n] for n in range(1, 51)}
    score_star = {s: freq_star[s] + delay_star[s] for s in range(1, 13)}

    # Calculer les matrices de transition markovienne sur les tirages pass\u00e9s
    trans_main = [[0] * 51 for _ in range(51)]
    trans_star = [[0] * 13 for _ in range(13)]
    for j in range(len(past_draws) - 1):
        main_cur = past_draws[j][1]
        star_cur = past_draws[j][2]
        main_next = past_draws[j+1][1]
        star_next = past_draws[j+1][2]
        for x in main_cur:
            for y in main_next:
                trans_main[x][y] += 1
        for a in star_cur:
            for b in star_next:
                trans_star[a][b] += 1

    # Derni\u00e8re combinaison connue avant le tirage actuel (tirage idx-1)
    last_past_main = past_draws[-1][1] if past_draws else []
    last_past_stars = past_draws[-1][2] if past_draws else []

    markov_score_main = {n: 0 for n in range(1, 51)}
    markov_score_star = {s: 0 for s in range(1, 13)}
    for x in last_past_main:
        for y in range(1, 51):
            markov_score_main[y] += trans_main[x][y]
    for a in last_past_stars:
        for b in range(1, 13):
            markov_score_star[b] += trans_star[a][b]

    # G\u00e9n\u00e9rer les pr\u00e9dictions pour ce tirage
    best5_fd = sorted(score_main.keys(), key=lambda n: score_main[n], reverse=True)[:5]
    best2_fd = sorted(score_star.keys(), key=lambda s: score_star[s], reverse=True)[:2]
    best5_markov = sorted(markov_score_main.keys(), key=lambda n: markov_score_main[n], reverse=True)[:5]
    best2_markov = sorted(markov_score_star.keys(), key=lambda s: markov_score_star[s], reverse=True)[:2]

    best5_fd.sort()
    best2_fd.sort()
    best5_markov.sort()
    best2_markov.sort()

    # Comparer aux r\u00e9sultats r\u00e9els
    actual_main_set = set(actual_main)
    actual_star_set = set(actual_stars)
    fd_hits_main = len(actual_main_set & set(best5_fd))
    fd_hits_star = len(actual_star_set & set(best2_fd))
    m_hits_main = len(actual_main_set & set(best5_markov))
    m_hits_star = len(actual_star_set & set(best2_markov))

    # Construire les cha\u00eenes de num\u00e9ros pour l'enregistrement
    actual_main_sorted = sorted(actual_main)
    actual_stars_sorted = sorted(actual_stars)
    pred_fd_str = " ".join(map(str, best5_fd)) + " + " + " ".join(map(str, best2_fd))
    pred_markov_str = " ".join(map(str, best5_markov)) + " + " + " ".join(map(str, best2_markov))
    actual_str = " ".join(map(str, actual_main_sorted)) + " + " + " ".join(map(str, actual_stars_sorted))

    # Ligne de r\u00e9sultat pour ce tirage
    line = (
        f"{current_date.strftime('%Y-%m-%d')},"
        f"{actual_str},"
        f"{pred_fd_str},{fd_hits_main},{fd_hits_star},"
        f"{pred_markov_str},{m_hits_main},{m_hits_star}"
    )
    lines.append(line)

# \u00c9crire le fichier CSV de backtest
with open(output_file, "w", encoding="utf-8") as fout:
    fout.write("\n".join(lines))

print(f"R\u00e9sultats du backtest {YEAR} \u00e9crits dans {output_file}")
