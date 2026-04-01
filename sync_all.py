#!/usr/bin/env python3
"""Script pour recréer complètement la base de données"""

import os
import sys

# Supprimer les anciennes bases
for db_file in ['destockage.db', 'instance/destockage.db']:
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"🗑️  Supprimé: {db_file}")

# Importer et exécuter l'initialisation
print("🔨 Création de la base...")
os.system("python3 init_db_minimal.py")

print("\n✅ Terminé !")
print("💡 Lancez maintenant: python3 app.py")