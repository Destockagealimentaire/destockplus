from app import app, db
from models import Utilisateur, Categorie, Produit, Commande
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def init_database():
    with app.app_context():
        # Créer les tables
        db.drop_all()
        db.create_all()
        
        # Créer un admin
        admin = Utilisateur(
            email='admin@destockpro.fr',
            password=generate_password_hash('admin123'),
            nom='Admin',
            prenom='Super',
            role='admin',
            telephone='0123456789',
            adresse='123 Rue du Commerce',
            code_postal='75001',
            ville='Paris',
            actif=True
        )
        db.session.add(admin)
        
        # Créer quelques clients de test
        for i in range(1, 6):
            client = Utilisateur(
                email=f'client{i}@test.com',
                password=generate_password_hash('client123'),
                nom=f'Dupont{i}',
                prenom=f'Jean{i}',
                role='client',
                telephone=f'01234567{i:02d}',
                adresse=f'{i} Rue de Test',
                code_postal='75001',
                ville='Paris',
                actif=True
            )
            db.session.add(client)
        
        # Catégories
        categories = [
            {'nom': 'Produits Frais', 'description': 'Fruits, légumes et produits frais', 'ordre': 1},
            {'nom': 'Épicerie', 'description': 'Produits d\'épicerie secs', 'ordre': 2},
            {'nom': 'Boissons', 'description': 'Jus, sodas et boissons diverses', 'ordre': 3},
            {'nom': 'Surgelés', 'description': 'Produits surgelés', 'ordre': 4},
            {'nom': 'Bio', 'description': 'Produits biologiques', 'ordre': 5},
            {'nom': 'Promotions', 'description': 'Offres spéciales', 'ordre': 6}
        ]
        
        for cat_data in categories:
            cat = Categorie(**cat_data)
            db.session.add(cat)
        
        db.session.commit()
        
        # Produits de test
        produits_data = [
            {
                'nom': 'Pack de 6 bouteilles d\'eau minérale',
                'description': 'Eau minérale naturelle 1.5L x6, idéale pour toute la famille',
                'prix': 4.50,
                'prix_promo': 3.90,
                'stock': 150,
                'categorie_id': 3,
                'image_principale': 'eau.jpg',
                'date_peremption': datetime.now() + timedelta(days=365),
                'origine': 'France',
                'poids': '9kg',
                'actif': True
            },
            {
                'nom': 'Pommes Golden 1kg',
                'description': 'Pommes Golden croquantes et sucrées, idéales pour le dessert',
                'prix': 2.99,
                'prix_promo': 2.49,
                'stock': 45,
                'categorie_id': 1,
                'image_principale': 'pommes.jpg',
                'date_peremption': datetime.now() + timedelta(days=15),
                'origine': 'France',
                'poids': '1kg',
                'actif': True
            },
            {
                'nom': 'Pâtes complètes bio 500g',
                'description': 'Pâtes complètes biologiques, riches en fibres',
                'prix': 1.99,
                'prix_promo': None,
                'stock': 200,
                'categorie_id': 5,
                'image_principale': 'pates.jpg',
                'date_peremption': datetime.now() + timedelta(days=730),
                'origine': 'Italie',
                'poids': '500g',
                'actif': True
            },
            {
                'nom': 'Filet de poulet fermier 500g',
                'description': 'Filet de poulet fermier label rouge, élevé en plein air',
                'prix': 7.99,
                'prix_promo': 6.99,
                'stock': 30,
                'categorie_id': 1,
                'image_principale': 'poulet.jpg',
                'date_peremption': datetime.now() + timedelta(days=5),
                'origine': 'France',
                'poids': '500g',
                'actif': True
            },
            {
                'nom': 'Yaourts nature lot de 16',
                'description': 'Yaourts nature au lait de vache, idéal pour toute la famille',
                'prix': 5.99,
                'prix_promo': 4.99,
                'stock': 80,
                'categorie_id': 1,
                'image_principale': 'yaourts.jpg',
                'date_peremption': datetime.now() + timedelta(days=21),
                'origine': 'France',
                'poids': '1.6kg',
                'actif': True
            },
            {
                'nom': 'Café en grains 1kg',
                'description': 'Café en grains 100% Arabica, torréfaction artisanale',
                'prix': 15.99,
                'prix_promo': 13.99,
                'stock': 25,
                'categorie_id': 2,
                'image_principale': 'cafe.jpg',
                'date_peremption': datetime.now() + timedelta(days=180),
                'origine': 'Colombie',
                'poids': '1kg',
                'actif': True
            },
            {
                'nom': 'Pizza 4 fromages surgelée',
                'description': 'Pizza 4 fromages sur pâte fine, prête en 10 minutes',
                'prix': 4.99,
                'prix_promo': 3.99,
                'stock': 60,
                'categorie_id': 4,
                'image_principale': 'pizza.jpg',
                'date_peremption': datetime.now() + timedelta(days=90),
                'origine': 'France',
                'poids': '400g',
                'actif': True
            },
            {
                'nom': 'Jus d\'orange pressé 1L',
                'description': 'Jus d\'orange 100% pur jus, sans sucres ajoutés',
                'prix': 3.49,
                'prix_promo': 2.99,
                'stock': 100,
                'categorie_id': 3,
                'image_principale': 'jus.jpg',
                'date_peremption': datetime.now() + timedelta(days=30),
                'origine': 'Espagne',
                'poids': '1L',
                'actif': True
            }
        ]
        
        for prod_data in produits_data:
            prod = Produit(**prod_data)
            db.session.add(prod)
        
        db.session.commit()
        
        # Créer quelques commandes de test
        clients = Utilisateur.query.filter_by(role='client').all()
        produits = Produit.query.all()
        
        for i, client in enumerate(clients[:3]):
            commande = Commande(
                numero=f"CMD-2024{random.randint(1000,9999)}",
                utilisateur_id=client.id,
                total=random.uniform(20, 100),
                statut=random.choice(['en_attente', 'confirmee', 'expediee', 'livree']),
                mode_paiement=random.choice(['carte', 'virement']),
                adresse_livraison=f"{client.adresse}, {client.code_postal} {client.ville}"
            )
            db.session.add(commande)
        
        db.session.commit()
        
        print("✅ Base de données initialisée avec succès !")
        print(f"📧 Admin: admin@destockpro.fr / admin123")
        print(f"👥 {Utilisateur.query.count()} utilisateurs")
        print(f"📦 {Categorie.query.count()} catégories")
        print(f"🏷️ {Produit.query.count()} produits")
        print(f"📋 {Commande.query.count()} commandes")

if __name__ == '__main__':
    init_database()