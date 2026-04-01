# import_all_products.py
from app import app, db
from models import Produit, Categorie
import json

# Données des produits (extrait de votre data.py)
produits_data = [
    {
        "id": 100,
        "nom": "🥤 Palette de Coca-Cola Original – Bouteilles 1L",
        "description": "Palette complète de 144 bouteilles de Coca-Cola Original 1L. La boisson gazeuse iconique au goût unique.",
        "prix": 129.00,
        "prix_promo": 129.00,
        "stock": 105,
        "categorie_nom": "Boissons",
        "image": "coca-palette.jpg",
        "origine": "France",
        "marque": "Coca-Cola"
    },
    {
        "id": 101,
        "nom": "🥤 Palette Red Bull 250ml (2592 canettes)",
        "description": "Palette complète de 2592 canettes Red Bull 250ml. La boisson énergisante originale.",
        "prix": 1432.80,
        "prix_promo": 1432.80,
        "stock": 8,
        "categorie_nom": "Boissons",
        "image": "redbull-palette.jpg",
        "origine": "Autriche",
        "marque": "Red Bull"
    },
    {
        "id": 102,
        "nom": "🥤 Fanta Orange 33cl (2592 canettes)",
        "description": "Palette complète de 2592 canettes de Fanta Orange 33cl. La boisson gazeuse fruitée.",
        "prix": 1012.00,
        "prix_promo": 1012.00,
        "stock": 120,
        "categorie_nom": "Boissons",
        "image": "fanta-palette.jpg",
        "origine": "France",
        "marque": "Fanta"
    },
    {
        "id": 103,
        "nom": "⚡ Palette Monster Energy 500ml (2592 canettes)",
        "description": "Palette complète de 2592 canettes de Monster Energy 500ml. La boisson énergisante au profil intense.",
        "prix": 1456.00,
        "prix_promo": 1456.00,
        "stock": 95,
        "categorie_nom": "Boissons",
        "image": "monster-palette.jpg",
        "origine": "États-Unis",
        "marque": "Monster"
    },
    {
        "id": 104,
        "nom": "🍊 Palette Orangina 33cl (2592 canettes)",
        "description": "Palette complète de 2592 canettes d'Orangina 33cl. La célèbre boisson pétillante à la pulpe.",
        "prix": 928.80,
        "prix_promo": 928.80,
        "stock": 110,
        "categorie_nom": "Boissons",
        "image": "orangina-palette.jpg",
        "origine": "France",
        "marque": "Orangina"
    },
    {
        "id": 105,
        "nom": "🍫 Palette Nutella 1kg (760 pots)",
        "description": "Palette complète de 760 pots de Nutella 1kg. La célèbre pâte à tartiner aux noisettes.",
        "prix": 1536.00,
        "prix_promo": 1536.00,
        "stock": 80,
        "categorie_nom": "Épicerie",
        "image": "nutella-palette.jpg",
        "origine": "France",
        "marque": "Nutella"
    },
    {
        "id": 112,
        "nom": "🍪 Palette biscuits Nutella 304g (1200 paquets)",
        "description": "Palette complète de 1200 paquets de biscuits fourrés à la pâte Nutella (304g).",
        "prix": 1400.00,
        "prix_promo": 1400.00,
        "stock": 5,
        "categorie_nom": "Épicerie",
        "image": "biscuits-nutella.jpg",
        "origine": "Pologne",
        "marque": "Nutella"
    },
    {
        "id": 113,
        "nom": "🥤 Palette Coca-Cola 33cl (2592 canettes)",
        "description": "Palette complète de 2592 canettes de Coca-Cola 33cl. Le Coca-Cola original en format canette.",
        "prix": 1096.00,
        "prix_promo": 1096.00,
        "stock": 10,
        "categorie_nom": "Boissons",
        "image": "coca-canettes.jpg",
        "origine": "France",
        "marque": "Coca-Cola"
    },
    {
        "id": 114,
        "nom": "💧 Palette San Pellegrino 50cl (600 bouteilles)",
        "description": "Palette complète de 600 bouteilles en verre de San Pellegrino 50cl. L'eau minérale gazeuse italienne.",
        "prix": 390.00,
        "prix_promo": 390.00,
        "stock": 8,
        "categorie_nom": "Boissons",
        "image": "san-pellegrino.jpg",
        "origine": "Italie",
        "marque": "San Pellegrino"
    },
    {
        "id": 115,
        "nom": "🍺 Palette Heineken 33cl (2592 canettes)",
        "description": "Palette complète de 2592 canettes de bière Heineken 33cl. La célèbre bière blonde lager.",
        "prix": 1156.00,
        "prix_promo": 1156.00,
        "stock": 6,
        "categorie_nom": "Boissons",
        "image": "heineken-palette.jpg",
        "origine": "Pays-Bas",
        "marque": "Heineken"
    },
    {
        "id": 116,
        "nom": "💧 Palette Perrier fines bulles 50cl (960 bouteilles)",
        "description": "Palette complète de 960 bouteilles en verre de Perrier fines bulles 50cl. L'eau gazeuse française emblématique.",
        "prix": 1090.00,
        "prix_promo": 1090.00,
        "stock": 7,
        "categorie_nom": "Boissons",
        "image": "perrier-palette.jpg",
        "origine": "France",
        "marque": "Perrier"
    }
]

def import_all():
    with app.app_context():
        print("📦 IMPORTATION DE TOUS LES PRODUITS...")
        
        # Récupérer les catégories
        categories = {c.nom: c.id for c in Categorie.query.all()}
        print(f"Catégories disponibles: {categories}")
        
        produits_importes = 0
        
        for prod_data in produits_data:
            # Vérifier si le produit existe déjà
            existing = Produit.query.filter_by(nom=prod_data['nom']).first()
            if existing:
                print(f"   ⏩ Déjà existant: {prod_data['nom'][:30]}...")
                continue
            
            # Trouver l'ID de catégorie
            categorie_id = categories.get(prod_data['categorie_nom'], 4)
            
            # Créer le produit
            produit = Produit(
                nom=prod_data['nom'],
                description=prod_data['description'],
                prix=prod_data['prix'],
                prix_promo=prod_data.get('prix_promo'),
                stock=prod_data['stock'],
                categorie_id=categorie_id,
                image_principale=prod_data['image'],
                origine=prod_data.get('origine'),
                marque=prod_data.get('marque'),
                actif=True
            )
            db.session.add(produit)
            produits_importes += 1
            print(f"   ✅ Importé: {prod_data['nom'][:30]}...")
        
        db.session.commit()
        print(f"\n✅ {produits_importes} nouveaux produits importés")
        print(f"📊 Total produits: {Produit.query.count()}")

if __name__ == '__main__':
    import_all()