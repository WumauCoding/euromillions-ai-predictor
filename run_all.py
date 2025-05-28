# run_all.py
import subprocess
import sys
import os

# Chemins vers les scripts
base_dir = os.path.dirname(os.path.abspath(__file__))
predictor_script = os.path.join(base_dir, "predictor.py")
quantum_script = os.path.join(base_dir, "quantum_preparation.py")
backtest_script = os.path.join(base_dir, "backtest.py")

# Année à backtester
year = sys.argv[1] if len(sys.argv) > 1 else "2022"

print("\n🔍 Étape 1 : Génération des grilles (predictor.py)...")
subprocess.run(["python3", predictor_script])

print("\n🔁 Étape 2 : Génération des combinaisons pondérées (quantum_preparation.py)...")
subprocess.run(["python3", quantum_script])

print(f"\n📊 Étape 3 : Backtest pour l'année {year} (backtest.py)...")
subprocess.run(["python3", backtest_script, year])

print("\n✅ Tous les scripts ont été exécutés avec succès.")
