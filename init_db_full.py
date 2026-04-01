#!/usr/bin/env python3
"""Script complet d'initialisation de la base de données"""

from app import app, db
from models import Utilisateur, Produit, Categorie, Commande, CommandeItem, Paiement, Panier, Avis, Wishlist
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

print("🚀 INITIALISATION COMPLÈTE DE LA BASE DE DONNÉES")
print("=" * 60)

with app.app_context():
    # 1. Supprimer toutes les tables
    print("📦 Suppression des anciennes tables...")
    db.drop_all()
    print("✅ Tables supprimées")
    
    # 2. Créer toutes les tables
    print("🔨 Création des tables...")
    db.create_all()
    print("✅ Tables créées")
    
    # 3. Vérifier que les tables existent
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Tables créées: {', '.join(tables)}")
    
    # 4. Importer les catégories
    print("\n📥 Import des catégories...")
    try:
        from data import categories as data_categories
        for cat_data in data_categories:
            categorie = Categorie(
                id=cat_data["id"],
                nom=cat_data["nom"],
                description=cat_data["description"],
                ordre=cat_data.get("ordre", 0)
            )
            db.session.add(categorie)
            print(f"   ➕ {cat_data['nom']}")
        db.session.commit()
        print(f"✅ {len(data_categories)} catégories importées")
    except Exception as e:
        print(f"❌ Erreur catégories: {e}")
        db.session.rollback()
    
    # 5. Importer les produits
    print("\n📥 Import des produits...")
    try:
        from data import products as data_products
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
            print(f"   ➕ {prod_data['nom']}")
        db.session.commit()
        print(f"✅ {len(data_products)} produits importés")
    except Exception as e:
        print(f"❌ Erreur produits: {e}")
        db.session.rollback()
    
    # 6. Créer l'utilisateur admin
    print("\n👤 Création de l'utilisateur admin...")
    admin = Utilisateur(
        email='admin@destockpro.fr',
        password=generate_password_hash('admin123'),
        nom='Admin',
        prenom='Super',
        role='admin',
        actif=True,
        pays='France'
    )
    db.session.add(admin)
    
    # 7. Créer un utilisateur test
    test = Utilisateur(
        email='test@test.fr',
        password=generate_password_hash('test123'),
        nom='Test',
        prenom='Utilisateur',
        role='client',
        actif=True,
        pays='France',
        adresse='123 rue de test',
        code_postal='75001',
        ville='Paris'
    )
    db.session.add(test)
    
    db.session.commit()
    print("✅ Admin créé: admin@destockpro.fr / admin123")
    print("✅ Test créé: test@test.fr / test123")
    
    # 8. Créer une commande test pour l'admin
    print("\n📝 Création d'une commande test...")
    commande_test = Commande(
        utilisateur_id=admin.id,
        email_client=admin.email,
        nom_client=f"{admin.prenom} {admin.nom}",
        adresse_livraison="123 rue du commerce, 75001 Paris",
        total=100.00,
        frais_port=0,
        reduction=0,
        total_final=100.00,
        statut='confirmee',
        mode_paiement='test'
    )
    db.session.add(commande_test)
    db.session.flush()
    print(f"   Commande test ID: {commande_test.id}, Numéro: {commande_test.numero}")
    db.session.commit()
    print("✅ Commande test créée")
    
    # 9. Vérification finale
    print("\n" + "=" * 60)
    print("🔍 VÉRIFICATION FINALE")
    print("=" * 60)
    
    categories_count = Categorie.query.count()
    produits_count = Produit.query.count()
    users_count = Utilisateur.query.count()
    commandes_count = Commande.query.count()
    
    print(f"📊 Statistiques:")
    print(f"   - Catégories: {categories_count}")
    print(f"   - Produits: {produits_count}")
    print(f"   - Utilisateurs: {users_count}")
    print(f"   - Commandes: {commandes_count}")
    
    # Vérifier que la table commande existe
    if 'commande' in tables:
        print("\n✅ La table 'commande' existe bien")
        
        # Afficher la commande test
        cmd = Commande.query.first()
        if cmd:
            print(f"   Commande exemple: ID={cmd.id}, Numéro={cmd.numero}, Utilisateur={cmd.utilisateur_id}")
    else:
        print("\n❌ ERREUR: La table 'commande' n'existe pas !")
    
    print("\n" + "=" * 60)
    print("🎉 INITIALISATION TERMINÉE AVEC SUCCÈS !")
    print("=" * 60)

print("\n💡 Pour lancer l'application:")
print("   python3 app.py")
print("\n🔑 Comptes de test:")
print("   Admin: admin@destockpro.fr / admin123")
print("   Test:  test@test.fr / test123")