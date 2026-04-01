# init_db_force.py
from app import app, db
from models import Utilisateur, Categorie, Produit
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    with app.app_context():
        print("🗑️ SUPPRESSION DE TOUTES LES TABLES...")
        db.drop_all()
        print("✅ Tables supprimées")
        
        print("🗄️ CRÉATION DES TABLES...")
        db.create_all()
        print("✅ Tables créées")
        
        # ADMIN
        admin = Utilisateur(
            email='admin@destockpro.fr',
            password=generate_password_hash('admin123'),
            nom='Admin',
            prenom='Super',
            role='admin'
        )
        db.session.add(admin)
        print("👤 Admin créé")
        
        # CATÉGORIES
        categories = [
            Categorie(id=1, nom='🥤 Boissons', description='Eaux, jus, sodas, boissons énergisantes', ordre=1),
            Categorie(id=2, nom='🍾 Vins & Spiritueux', description='Vins fins, champagnes, spiritueux', ordre=2),
            Categorie(id=3, nom='🥗 Produits frais', description='Fruits, légumes, produits frais', ordre=3),
            Categorie(id=4, nom='🏺 Épicerie', description='Pâtes, riz, conserves, épicerie fine', ordre=4),
            Categorie(id=5, nom='❄️ Surgelés', description='Plats surgelés, glaces, légumes', ordre=5),
            Categorie(id=6, nom='🥛 Produits laitiers', description='Lait, fromages, yaourts', ordre=6),
            Categorie(id=7, nom='🥩 Viandes & Poissons', description='Viandes premium, poissons frais', ordre=7),
            Categorie(id=8, nom='🔥 Promotions', description='Offres spéciales et destockage', ordre=8),
        ]
        
        for cat in categories:
            db.session.add(cat)
        db.session.commit()
        print(f"📦 {len(categories)} catégories créées")
        
        # PRODUITS DE TEST
        produits = [
            # Boissons
            Produit(
                nom='🥤 Coca-Cola 1L - Lot de 6',
                description='Pack de 6 bouteilles de Coca-Cola Original 1L. La boisson gazeuse iconique.',
                prix=9.90,
                prix_promo=7.90,
                stock=45,
                categorie_id=1,
                image_principale='coca.jpg',
                origine='France',
                actif=True
            ),
            Produit(
                nom='⚡ Red Bull 250ml - Pack de 24',
                description='Boisson énergisante Red Bull Original. Pack de 24 canettes de 250ml.',
                prix=42.00,
                prix_promo=36.00,
                stock=30,
                categorie_id=1,
                image_principale='redbull.jpg',
                origine='Autriche',
                actif=True
            ),
            Produit(
                nom='💧 Evian 1.5L - Lot de 6',
                description='Eau minérale naturelle Evian. Pack de 6 bouteilles de 1.5L.',
                prix=6.90,
                stock=60,
                categorie_id=1,
                image_principale='evian.jpg',
                origine='France',
                actif=True
            ),
            
            # Vins & Spiritueux
            Produit(
                nom='🍾 Champagne Moët & Chandon Brut Impérial',
                description='Champagne Brut Impérial 75cl. La référence des champagnes de prestige.',
                prix=49.90,
                prix_promo=42.90,
                stock=15,
                categorie_id=2,
                image_principale='moet.jpg',
                origine='France',
                actif=True
            ),
            Produit(
                nom='🥃 Whisky Johnnie Walker Black Label',
                description='Whisky écossais blend 12 ans d\'âge. Bouteille 70cl.',
                prix=39.90,
                stock=20,
                categorie_id=2,
                image_principale='johnnie-walker.jpg',
                origine='Écosse',
                actif=True
            ),
            
            # Produits frais
            Produit(
                nom='🧀 Camembert de Normandie AOP',
                description='Camembert au lait cru AOP 250g. Fabriqué en Normandie.',
                prix=5.90,
                stock=25,
                categorie_id=3,
                image_principale='camembert.jpg',
                origine='France',
                actif=True
            ),
            
            # Épicerie
            Produit(
                nom='🍝 Pâtes Panzani Penne Rigate 500g',
                description='Pâtes italiennes de qualité supérieure. Paquet de 500g.',
                prix=1.80,
                stock=200,
                categorie_id=4,
                image_principale='pates.jpg',
                origine='Italie',
                actif=True
            ),
            Produit(
                nom='🍫 Nutella 1kg',
                description='Pâte à tartiner aux noisettes et cacao. Pot de 1kg.',
                prix=8.90,
                prix_promo=7.50,
                stock=40,
                categorie_id=4,
                image_principale='nutella.jpg',
                origine='France',
                actif=True
            ),
            
            # Surgelés
            Produit(
                nom='❄️ Pizza 4 Fromages 400g',
                description='Pizza surgelée 4 fromages (mozzarella, gorgonzola, parmesan, chèvre).',
                prix=5.99,
                prix_promo=4.50,
                stock=35,
                categorie_id=5,
                image_principale='pizza.jpg',
                origine='France',
                actif=True
            ),
            Produit(
                nom='🍦 Glace vanille 1L',
                description='Glace à la vanille de Madagascar. Pot de 1L.',
                prix=4.90,
                stock=28,
                categorie_id=5,
                image_principale='glace.jpg',
                origine='France',
                actif=True
            ),
            
            # Viandes & Poissons
            Produit(
                nom='🥩 Entrecôte de Bœuf 300g',
                description='Entrecôte de bœuf française 300g. Viande de qualité supérieure.',
                prix=15.90,
                stock=12,
                categorie_id=7,
                image_principale='entrecote.jpg',
                origine='France',
                actif=True
            ),
            Produit(
                nom='🐟 Saumon fumé Norvège 200g',
                description='Saumon fumé de Norvège. Tranches épaisses, prêtes à déguster.',
                prix=8.90,
                stock=18,
                categorie_id=7,
                image_principale='saumon.jpg',
                origine='Norvège',
                actif=True
            ),
        ]
        
        for prod in produits:
            db.session.add(prod)
        
        db.session.commit()
        print(f"🏷️ {len(produits)} produits créés")
        
        # RÉCAPITULATIF
        print("\n" + "="*50)
        print("✅ BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS !")
        print("="*50)
        print(f"👤 Admin: admin@destockpro.fr / admin123")
        print(f"📦 Catégories: {Categorie.query.count()}")
        print(f"🏷️ Produits: {Produit.query.count()}")
        print("="*50)
        
        # AFFICHER LES PRODUITS
        print("\n📋 LISTE DES PRODUITS DISPONIBLES :")
        for p in Produit.query.all():
            promo = f" (PROMO: {p.prix_promo}€)" if p.prix_promo else ""
            print(f"  • [{p.categorie_id}] {p.nom} - {p.prix}€{promo} - Stock: {p.stock}")

if __name__ == '__main__':
    init_database()