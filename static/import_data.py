# import_data.py
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
            # Vérifier si le produit existe déjà (par nom ou SKU)
            existing = None
            if prod_data.get('sku'):
                existing = Produit.query.filter_by(sku=prod_data['sku']).first()
            if not existing and prod_data.get('nom'):
                existing = Produit.query.filter_by(nom=prod_data['nom']).first()
            
            if existing:
                produits_existants += 1
                continue
            
            # Trouver la catégorie
            categorie_nom = prod_data.get('categorie_nom', 'Épicerie')
            categorie = Categorie.query.filter_by(nom=categorie_nom).first()
            
            if not categorie:
                # Chercher dans les catégories de data.py
                for cat_data in categories_data:
                    if cat_data['nom'] == categorie_nom:
                        categorie = Categorie(
                            id=cat_data['id'],
                            nom=cat_data['nom'],
                            description=cat_data['description'],
                            image=cat_data['image'],
                            ordre=cat_data['ordre']
                        )
                        db.session.add(categorie)
                        db.session.flush()
                        break
            
            if not categorie:
                print(f"⚠️ Catégorie non trouvée pour {prod_data['nom']}, utilisation de la catégorie 4")
                categorie_id = 4
            else:
                categorie_id = categorie.id
            
            # Créer le produit
            produit = Produit(
                nom=prod_data['nom'],
                description=prod_data.get('description', ''),
                prix=prod_data.get('prix', prod_data.get('prix_original', 0)),
                prix_promo=prod_data.get('prix_promo'),
                stock=prod_data.get('stock', 0),
                categorie_id=categorie_id,
                image_principale=prod_data.get('images', ['default.jpg'])[0] if prod_data.get('images') else 'default.jpg',
                images=json.dumps(prod_data.get('images', [])[1:]) if len(prod_data.get('images', [])) > 1 else None,
                origine=prod_data.get('pays_origine'),
                reference=prod_data.get('sku'),
                marque=prod_data.get('marque'),
                actif=True
            )
            db.session.add(produit)
            produits_importes += 1
        
        db.session.commit()
        
        print(f"\n✅ IMPORTATION TERMINÉE !")
        print(f"   ➕ {produits_importes} nouveaux produits importés")
        print(f"   ➖ {produits_existants} produits déjà existants")
        print(f"   📊 Total produits maintenant: {Produit.query.count()}")

if __name__ == '__main__':
    import_products()