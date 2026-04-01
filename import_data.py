# import_data.py corrigé
from app import app, db
from models import Produit, Categorie
from data import products as products_data, categories as categories_data
import json

def import_products():
    with app.app_context():
        print("📦 IMPORTATION DES PRODUITS DEPUIS DATA.PY...")
        
        # Vérifier les catégories existantes
        categories_existantes = {c.id: c for c in Categorie.query.all()}
        print(f"Catégories existantes: {len(categories_existantes)}")
        
        produits_importes = 0
        produits_existants = 0
        
        for prod_data in products_data:
            # Vérifier si le produit existe déjà (par nom ou référence)
            existing = None
            if prod_data.get('reference'):
                existing = Produit.query.filter_by(reference=prod_data['reference']).first()
            if not existing and prod_data.get('nom'):
                existing = Produit.query.filter_by(nom=prod_data['nom']).first()
            
            if existing:
                produits_existants += 1
                print(f"   ⏩ Produit existant: {prod_data['nom'][:30]}...")
                continue
            
            # Trouver la catégorie
            categorie_nom = prod_data.get('categorie_nom', 'Épicerie')
            categorie = Categorie.query.filter_by(nom=categorie_nom).first()
            
            if not categorie:
                print(f"   ⚠️ Catégorie '{categorie_nom}' non trouvée, utilisation Épicerie")
                categorie = Categorie.query.filter_by(nom='Épicerie').first()
                if not categorie:
                    categorie = Categorie.query.first()
            
            if not categorie:
                print(f"   ❌ Aucune catégorie trouvée, skip {prod_data['nom']}")
                continue
            
            # Gérer les images
            images_list = prod_data.get('images', [])
            image_principale = images_list[0] if images_list else 'default.jpg'
            
            # Déterminer le prix
            prix = prod_data.get('prix', prod_data.get('prix_original', 0))
            prix_promo = prod_data.get('prix_promo')
            
            # Créer le produit
            try:
                produit = Produit(
                    nom=prod_data['nom'],
                    description=prod_data.get('description', ''),
                    prix=prix,
                    prix_promo=prix_promo,
                    stock=prod_data.get('stock', 0),
                    categorie_id=categorie.id,
                    image_principale=image_principale,
                    origine=prod_data.get('pays_origine'),
                    reference=prod_data.get('sku') or prod_data.get('reference'),
                    actif=True
                )
                db.session.add(produit)
                produits_importes += 1
                print(f"   ✅ Importé: {prod_data['nom'][:30]}...")
                
            except Exception as e:
                print(f"   ❌ Erreur pour {prod_data['nom']}: {e}")
                continue
            
            # Commit tous les 10 produits
            if produits_importes % 10 == 0:
                db.session.commit()
                print(f"   ✓ {produits_importes} produits commités...")
        
        db.session.commit()
        
        print(f"\n✅ IMPORTATION TERMINÉE !")
        print(f"   ➕ {produits_importes} nouveaux produits importés")
        print(f"   ➖ {produits_existants} produits déjà existants")
        print(f"   📊 Total produits maintenant: {Produit.query.count()}")

if __name__ == '__main__':
    import_products()
