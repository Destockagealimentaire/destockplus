#!/usr/bin/env python3
"""Script d'initialisation complet de la base de données"""

from app import app, db
from models import Utilisateur, Produit, Categorie, Commande, CommandeItem, Paiement, Panier, Avis
from werkzeug.security import generate_password_hash
from datetime import datetime

print("🚀 Initialisation de la base de données...")

with app.app_context():
    # 1. Supprimer toutes les tables existantes
    print("📦 Suppression des anciennes tables...")
    db.drop_all()
    
    # 2. Créer toutes les tables avec le bon schéma
    print("🔨 Création des nouvelles tables...")
    db.create_all()
    print("✅ Tables créées avec succès")
    
    # 3. Vérifier que la table produit existe et a les bonnes colonnes
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('produit')]
    print(f"📋 Colonnes de la table produit: {len(columns)} colonnes")
    
    if 'devise' in columns:
        print("✅ Colonne 'devise' présente")
    else:
        print("❌ Colonne 'devise' manquante")
    
    # 4. Importer les données depuis data.py
    try:
        from data import categories as data_categories, products as data_products
        
        print("\n📥 Import des catégories...")
        for cat_data in data_categories:
            categorie = Categorie(
                id=cat_data["id"],
                nom=cat_data["nom"],
                description=cat_data["description"],
                ordre=cat_data["ordre"]
            )
            db.session.add(categorie)
            print(f"  ➕ {cat_data['nom']}")
        
        db.session.commit()
        print(f"✅ {len(data_categories)} catégories importées")
        
        print("\n📥 Import des produits...")
        for prod_data in data_products:
            produit = Produit(
                id=prod_data["id"],
                nom=prod_data["nom"],
                description=prod_data["description"],
                prix=prod_data["prix"],
                prix_promo=prod_data.get("prix_promo"),
                devise="EUR",
                categorie_id=prod_data["categorie_id"],
                stock=prod_data.get("stock", 0),
                image_principale=prod_data.get("images", ["default.jpg"])[0] if prod_data.get("images") else "default.jpg",
                en_promotion=prod_data.get("en_promotion", False),
                meilleure_vente=prod_data.get("meilleure_vente", False),
                actif=True
            )
            db.session.add(produit)
            print(f"  ➕ {prod_data['nom']}")
        
        db.session.commit()
        print(f"✅ {len(data_products)} produits importés")
        
    except ImportError:
        print("⚠️  data.py non trouvé, import des données ignoré")
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")
        db.session.rollback()
    
    # 5. Créer un admin par défaut
    print("\n👤 Création de l'utilisateur admin...")
    admin = Utilisateur(
        email='admin@destockpro.fr',
        password=generate_password_hash('admin123'),
        nom='Admin',
        prenom='Super',
        role='admin',
        actif=True,
        date_inscription=datetime.now()
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin créé: admin@destockpro.fr / admin123")
    
    # 6. Vérification finale
    print("\n🔍 Vérification finale:")
    print(f"  - Catégories: {Categorie.query.count()}")
    print(f"  - Produits: {Produit.query.count()}")
    print(f"  - Utilisateurs: {Utilisateur.query.count()}")
    
    print("\n🎉 Initialisation terminée avec succès!")

print("\n💡 Pour lancer l'application:")
print("   python3 app.py")