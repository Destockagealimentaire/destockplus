# seed_reviews.py
import random
from datetime import datetime, timedelta
from app import app, db
from models import Produit, Avis, Utilisateur

# Liste de commentaires réalistes pour le destockage alimentaire
COMMENTAIRES = [
    # 5 étoiles
    ("Très satisfait du produit ! Qualité au rendez-vous, livraison rapide. Je recommande vivement cette plateforme de destockage.", 5),
    ("Excellent rapport qualité-prix. Conforme à la description. Je vais commander à nouveau sans hésiter.", 5),
    ("Produit de grande qualité, emballage soigné. Merci DestockPro pour ce service exceptionnel !", 5),
    ("Superbe découverte ! Le produit est parfait, livraison en 24h. Vraiment impressionné.", 5),
    ("Je recommande à 100% ! Le meilleur site de destockage alimentaire que j'ai testé.", 5),
    ("Produit conforme, prix imbattable, livraison rapide. Que demander de plus ?", 5),
    ("Une pépite ! Qualité professionnelle, je suis ravi de mon achat.", 5),
    ("Service client au top, produit parfait. Je suis un client fidèle maintenant.", 5),
    
    # 4 étoiles
    ("Très bon produit, petite erreur dans l'emballage mais le service client a tout de suite réglé le problème.", 4),
    ("Bon rapport qualité-prix, livraison un peu plus longue que prévu mais produit conforme.", 4),
    ("Je recommande ce produit. Quelques petites imperfections mais rien de grave.", 4),
    ("Très satisfait globalement. La qualité est bonne, le prix est intéressant.", 4),
    ("Bon produit, je m'attendais à un peu mieux mais ça reste une bonne affaire.", 4),
    ("Produit de qualité, livraison soignée. Un petit bémol sur l'emballage.", 4),
    
    # 3 étoiles
    ("Produit correct mais pas exceptionnel. Le rapport qualité-prix est acceptable.", 3),
    ("Moyennement satisfait. Le produit fait le travail mais je m'attendais à mieux.", 3),
    ("Ça passe, mais je pense qu'on peut trouver mieux ailleurs. Les prix restent intéressants.", 3),
    ("Livraison un peu lente, produit correct. Je ne suis pas sûr de recommander.", 3),
    
    # 2 étoiles
    ("Déçu par la qualité du produit. Je ne recommande pas malgré le prix attractif.", 2),
    ("Le produit ne correspond pas tout à fait à la description. Dommage.", 2),
    ("Service client difficile à joindre, produit endommagé à la livraison.", 2),
    
    # 1 étoile
    ("Très déçu, produit non conforme. Je ne recommande vraiment pas.", 1),
    ("Qualité médiocre, je regrette mon achat. Attention à la description trompeuse.", 1),
    ("Produit abîmé, service client inexistant. Expérience catastrophique.", 1),
]

# Commentaires spécifiques par catégorie de produit
COMMENTAIRES_PAR_CATEGORIE = {
    'Boissons': [
        "Parfait pour mon bar ! Les canettes sont bien conditionnées et la date de péremption est bonne.",
        "Boisson fraîche et agréable, livraison en parfait état. Je recommande pour les professionnels.",
        "Excellent produit, mes clients adorent. Le prix est imbattable en destockage.",
        "Attention à la manipulation, certaines canettes étaient cabossées mais le service après-vente a été réactif.",
    ],
    'Vins, Champagnes et Spiritueux': [
        "Un champagne d'excellente qualité à prix cassé ! Mes clients sont ravis.",
        "Vin très correct pour le prix, parfait pour les soirées. Je recommande chaudement.",
        "Délicieux, livraison très soignée pour des produits fragiles. Je suis conquis.",
        "Très bon rapport qualité-prix pour ce vin. Parfait pour les professionnels de la restauration.",
    ],
    'Produits frais': [
        "Fruits et légumes d'une fraîcheur exceptionnelle, livraison rapide. Je suis très satisfait.",
        "La qualité est là, les produits sont bien frais. Ça change des supermarchés !",
        "Produits frais de qualité, emballage parfait pour préserver la fraîcheur.",
        "Très bonne surprise, les produits sont arrivés bien frais malgré la distance.",
    ],
    'Épicerie': [
        "Produits d'épicerie de qualité, large choix. Je trouve toujours ce que je cherche.",
        "Les pâtes et le riz sont excellents, la date de péremption est loin. Idéal pour le stock.",
        "Très bon rapport qualité-prix pour l'épicerie. Je recommande à tous les commerçants.",
        "Produits bien conditionnés, variété intéressante. Je suis un client régulier maintenant.",
    ],
    'Surgelés': [
        "Produits surgelés de qualité, chaîne du froid respectée. Emballage impeccable.",
        "Très satisfait des surgelés, la livraison a été parfaite. Je recommande.",
        "Les produits sont arrivés bien congelés, la qualité est au rendez-vous.",
        "Excellent rapport qualité-prix pour les surgelés. Je vais racheter.",
    ],
    'Produits laitiers': [
        "Fromages d'excellente qualité, livraison rapide et bien emballée.",
        "Les produits laitiers sont très frais, la date de péremption est correcte.",
        "Très bon rapport qualité-prix pour ces fromages. Mes clients les adorent.",
        "Produits laitiers de qualité professionnelle, je suis très satisfait.",
    ],
    'Viandes et poissons': [
        "Viande de qualité, bien emballée et livrée rapidement. Je suis conquis.",
        "Poisson très frais, emballage sous vide parfait. Je recommande ce site.",
        "Excellente qualité de viande, le rapport qualité-prix est imbattable.",
        "Livraison rapide, produits bien conditionnés. Je suis très satisfait.",
    ],
}

def generate_reviews_for_all_products():
    """Génère des avis aléatoires pour tous les produits"""
    print("🔄 Début de la génération des avis factices...")
    
    # Récupérer tous les produits actifs
    produits = Produit.query.filter_by(actif=True).all()
    
    if not produits:
        print("❌ Aucun produit trouvé dans la base de données.")
        return
    
    print(f"📦 {len(produits)} produits trouvés.")
    
    # Récupérer ou créer un utilisateur de test pour les avis
    user = Utilisateur.query.filter_by(email='reviewer@destockpro.fr').first()
    if not user:
        user = Utilisateur(
            email='reviewer@destockpro.fr',
            prenom='Client',
            nom='Test',
            password='hashed_password_placeholder',  # Pas besoin de mot de passe pour les avis factices
            actif=True,
            date_inscription=datetime.now()
        )
        db.session.add(user)
        db.session.commit()
        print("👤 Utilisateur de test créé.")
    
    total_avis = 0
    avis_par_produit = {}
    
    for produit in produits:
        # Déterminer le nombre d'avis (entre 0 et 25)
        nb_avis = random.randint(3, 25)
        
        # Si c'est un produit populaire, plus d'avis
        if produit.meilleure_vente:
            nb_avis = random.randint(15, 40)
        elif produit.en_promotion:
            nb_avis = random.randint(8, 30)
        
        avis_produit = []
        
        # Récupérer les commentaires spécifiques à la catégorie
        categorie_nom = produit.categorie.nom if produit.categorie else 'Épicerie'
        commentaires_categorie = COMMENTAIRES_PAR_CATEGORIE.get(categorie_nom, COMMENTAIRES_PAR_CATEGORIE['Épicerie'])
        
        # Combiner tous les commentaires
        tous_commentaires = COMMENTAIRES + [(c, 4) for c in commentaires_categorie]
        
        for i in range(nb_avis):
            # Choisir un commentaire aléatoire
            commentaire, note_base = random.choice(tous_commentaires)
            
            # Variation aléatoire de la note (+/- 1)
            note = max(1, min(5, note_base + random.randint(-1, 1)))
            
            # Date aléatoire entre aujourd'hui et 6 mois en arrière
            jours_ecoules = random.randint(1, 180)
            date_avis = datetime.now() - timedelta(days=jours_ecoules)
            
            # Créer l'avis - CORRECTION ICI : supprimer 'date_maj'
            avis = Avis(
                utilisateur_id=user.id,
                produit_id=produit.id,
                note=note,
                commentaire=commentaire,
                date_creation=date_avis
                # date_maj supprimé car n'existe pas dans le modèle
            )
            db.session.add(avis)
            avis_produit.append(avis)
            total_avis += 1
        
        avis_par_produit[produit.id] = avis_produit
        print(f"   ✅ {nb_avis} avis pour '{produit.nom}'")
    
    # Mettre à jour les notes moyennes des produits
    print("📊 Mise à jour des notes moyennes...")
    for produit in produits:
        avis = Avis.query.filter_by(produit_id=produit.id).all()
        if avis:
            produit.note_moyenne = sum(a.note for a in avis) / len(avis)
            produit.note_count = len(avis)
            print(f"   📊 {produit.nom}: {produit.note_moyenne:.1f}★ ({produit.note_count} avis)")
    
    # Sauvegarder
    db.session.commit()
    print(f"✅ {total_avis} avis générés avec succès pour {len(produits)} produits !")

def clear_all_reviews():
    """Supprime tous les avis (utile pour recommencer)"""
    print("🗑️ Suppression de tous les avis...")
    Avis.query.delete()
    db.session.commit()
    
    # Réinitialiser les notes des produits
    produits = Produit.query.all()
    for produit in produits:
        produit.note_moyenne = 0
        produit.note_count = 0
    db.session.commit()
    print("✅ Tous les avis supprimés")

if __name__ == '__main__':
    with app.app_context():
        print("=" * 60)
        print("🌟 GÉNÉRATEUR D'AVIS FACTICES")
        print("=" * 60)
        
        choice = input("Voulez-vous (1) générer des avis, (2) supprimer tous les avis, ou (3) les deux ? (1/2/3) : ")
        
        if choice == '2':
            clear_all_reviews()
        elif choice == '3':
            clear_all_reviews()
            print("\n" + "=" * 60)
            generate_reviews_for_all_products()
        else:
            generate_reviews_for_all_products()
        
        print("\n" + "=" * 60)
        print("🏁 Terminé !")
