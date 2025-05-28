
#!/bin/bash

# Crée l'arborescence
mkdir -p ~/euromillions/data
mkdir -p ~/euromillions/logs
mkdir -p ~/euromillions/results

# Déplace les fichiers CSV si existants
if [ -f ~/euromillions/tirages_euromillion.csv ]; then
  mv ~/euromillions/tirages_euromillion.csv ~/euromillions/data/
fi

echo "✅ Arborescence euromillions préparée avec succès."
