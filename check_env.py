import os
import pandas as pd
import csv

DATA_PATH = "data/tirages_euromillion.csv"

REQUIRED_COLUMNS = ['Date', 'Jour', '1', '2', '3', '4', '5', 'Star 1', 'Star 2']

def verify_directories():
    print("\n📁 Vérification des dossiers...")
    for folder in ["data", "logs", "results"]:
        if os.path.isdir(folder):
            print(f"✅ Dossier présent : {folder}")
        else:
            print(f"❌ Dossier manquant : {folder}")

def verify_scripts():
    print("\n📄 Vérification des scripts...")
    for script in ["predictor.py", "quantum_preparation.py", "backtest.py", "run_all.py"]:
        if os.path.isfile(script):
            print(f"✅ Script présent : {script}")
        else:
            print(f"❌ Script manquant : {script}")

def verify_packages():
    print("\n📦 Vérification des packages Python requis...")
    try:
        import pandas
        print("✅ Package installé : pandas")
    except ImportError:
        print("❌ Package manquant : pandas")

def check_csv_header():
    print("\n🧾 Vérification du fichier de données...")
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                print(f"✅ Ligne d'en-tête détectée : {header}")
                missing = [col for col in REQUIRED_COLUMNS if col not in header]
                if missing:
                    print(f"❌ Colonnes manquantes : {missing}")
                    auto_fix_header()
                else:
                    print("✅ Toutes les colonnes essentielles sont présentes.")
            else:
                print("❌ Aucune ligne d'en-tête détectée. Tentative de correction...")
                auto_fix_header()
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {DATA_PATH} : {e}")

def auto_fix_header():
    try:
        df = pd.read_csv(DATA_PATH, skiprows=0, encoding='utf-8')
        for i in range(5):  # Cherche les 5 premières lignes pour la bonne en-tête
            temp_df = pd.read_csv(DATA_PATH, skiprows=i, encoding='utf-8')
            if set(REQUIRED_COLUMNS).issubset(temp_df.columns):
                temp_df.to_csv(DATA_PATH, index=False, encoding='utf-8')
                print(f"✅ En-tête corrigé et enregistré dans : {DATA_PATH}")
                return
        print("❌ Impossible de corriger automatiquement l'en-tête.")
    except Exception as e:
        print(f"❌ Erreur pendant la tentative de correction automatique : {e}")

if __name__ == "__main__":
    print("\n🔍 Lancement de la vérification de l'environnement Euromillions:")
    verify_directories()
    verify_scripts()
    verify_packages()
    check_csv_header()
    print("\n✅ Vérification terminée.")
