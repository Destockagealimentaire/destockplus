#!/usr/bin/env python3
from app import app, db
from werkzeug.security import generate_password_hash

print("🚀 Initialisation simple de la base...")

with app.app_context():
    # Supprimer et recréer toutes les tables
    db.drop_all()
    db.create_all()
    print("✅ Tables créées")
    
    # Importer les données
    try:
        from data import categories, products
        
        print("📥 Import des catégories...")
        for cat_data in categories:
            from models import Categorie
            cat = Categorie(
                id=cat_data["id"],
                nom=cat_data["nom"],
                description=cat_data["description"],
                ordre=cat_data["ordre"]
            )
            db.session.add(cat)
        db.session.commit()
        print(f"✅ {len(categories)} catégories")
        
        print("📥 Import des produits...")
        for prod_data in products:
            from models import Produit
            prod = Produit(
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
            db.session.add(prod)
        db.session.commit()
        print(f"✅ {len(products)} produits")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.session.rollback()
    
    # Admin
    from models import Utilisateur
    admin = Utilisateur(
        email='admin@destockpro.fr',
        password=generate_password_hash('admin123'),
        nom='Admin',
        prenom='Super',
        role='admin',
        actif=True
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin créé")
    
    print(f"\n📊 Statistiques:")
    print(f"  - Catégories: {Categorie.query.count()}")
    print(f"  - Produits: {Produit.query.count()}")
    print(f"  - Utilisateurs: {Utilisateur.query.count()}")

print("\n🎉 Terminé! Lancez: python3 app.py")