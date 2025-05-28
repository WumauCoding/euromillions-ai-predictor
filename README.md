<p align="center">
  <img src="assets/banner-mini.png" alt="Euromillions AI Banner" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/WumauCoding/euromillions-ai-predictor/releases"><img src="https://img.shields.io/github/v/release/WumauCoding/euromillions-ai-predictor?label=latest&color=brightgreen" alt="Latest Release" /></a>
  <img src="https://img.shields.io/badge/python-3.10-blue.svg" alt="Python 3.10" />
  <img src="https://img.shields.io/github/last-commit/WumauCoding/euromillions-ai-predictor" alt="Last Commit" />
</p>



# Euromillions AI Prediction Toolkit

Ce projet open-source propose un ensemble de scripts pour :

* Générer automatiquement des grilles de tirage prédictives
* Créer des combinaisons pondérées à partir des statistiques passées (fréquence, retard, markov)
* Préparer un tirage pondéré exploitable par des simulateurs quantiques (Qiskit/IBMQ)
* Évaluer les prédictions sur des tirages passés (backtest)

---

## 📁 Structure du projet

```
euromillions/
├── data/                       # Fichiers d'entrée (tirages historiques)
│   └── tirages_euromillion.csv
├── results/                    # Fichiers de sortie générés
│   ├── grilles_prediction.csv
│   └── quantum_states.csv
├── logs/                      # Logs des backtests (ex: backtest_2022.csv)
├── predictor.py               # Génère les grilles de prédiction classiques
├── quantum_preparation.py    # Génère les combinaisons pondérées pour IBMQ
├── backtest.py               # Évalue les prédictions sur une année
├── run_all.py                # Exécute tout le pipeline
├── check_env.py              # Vérifie l'intégrité de l'installation
└── setup_euromillions.sh     # Initialise l'arborescence de projet
```

---

## 🧠 Méthodes utilisées

* **Fréquence et retard** des numéros (loi des grands nombres)
* **Transitions markoviennes** pour prédiction conditionnelle
* **Simulation pondérée** (préparation quantique)
* Prévision glissante par année (**backtest**)

---

## 🚀 Exécution complète

```bash
python3 run_all.py 2022
```

Cela lancera :

* `predictor.py` → produit 2 grilles : fréquence+retard et markov
* `quantum_preparation.py` → génère 5000 combinaisons pondérées
* `backtest.py` → compare la prédiction à chaque tirage réel de 2022

---

## 🛡 Vérification automatique

Lancer ce script pour s'assurer que tout est en place :

```bash
python3 check_env.py
```

Ce script vérifie :

* L'existence des répertoires `data/`, `logs/`, `results/`
* La présence des fichiers principaux
* L'installation de `pandas`
* Que le fichier `tirages_euromillion.csv` contient les bonnes colonnes et une date récente

---

## 🔁 Exécution automatique chaque semaine

Pour lancer la prédiction chaque vendredi à 18h via `cron` :

```bash
crontab -e
```

Puis ajouter :

```cron
0 18 * * FRI /usr/bin/python3 /home/wumix/euromillions/run_all.py >> /home/wumix/euromillions/logs/cron_output.txt 2>&1
```

---

## 📊 Fichiers de sortie

* `results/grilles_prediction.csv` → les 2 grilles proposées
* `results/quantum_states.csv` → combinaisons pondérées pour Qiskit
* `logs/backtest_<année>.csv` → résultats comparatifs grille vs réalité

---

## 📌 Pré-requis Python

* Python 3.6+
* `pandas`

Installation rapide :

```bash
pip install pandas
```

---

## 🧠 Avenir

* API FastAPI pour exposer les prédictions
* Intégration IBM Quantum pour tirage pondéré
* Ajout d’analyse FFT, entropie de Shannon et modèle bayésien

---

© 2025 - Projet personnel développé par Arthur Balaÿ
