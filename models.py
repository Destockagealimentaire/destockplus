from flask_login import UserMixin
from datetime import datetime
import random
from extensions import db  # ← Importer depuis extensions

class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateur'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.String(200))
    code_postal = db.Column(db.String(10))
    ville = db.Column(db.String(100))
    pays = db.Column(db.String(50), default='France')
    societe = db.Column(db.String(100))
    role = db.Column(db.String(20), default='client')
    actif = db.Column(db.Boolean, default=True)
    date_inscription = db.Column(db.DateTime, default=datetime.now)
    
    # Relations
    commandes = db.relationship('Commande', backref='utilisateur', lazy=True)
    avis = db.relationship('Avis', backref='utilisateur', lazy=True)

class Categorie(db.Model):
    __tablename__ = 'categorie'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    ordre = db.Column(db.Integer, default=0)
    
    # Relations
    produits = db.relationship('Produit', backref='categorie', lazy=True)

class Produit(db.Model):
    __tablename__ = 'produit'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    description_courte = db.Column(db.String(500))
    prix = db.Column(db.Float, nullable=False)
    prix_promo = db.Column(db.Float)
    devise = db.Column(db.String(10), default='EUR')
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'))
    stock = db.Column(db.Integer, default=0)
    stock_initial = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(50), unique=True)
    upc = db.Column(db.String(50))
    marque = db.Column(db.String(100))
    fournisseur = db.Column(db.String(100))
    poids = db.Column(db.String(50))
    poids_net = db.Column(db.String(50))
    dimensions = db.Column(db.String(100))
    volume_palette = db.Column(db.String(50))
    format = db.Column(db.String(100))
    unites = db.Column(db.Integer)
    type_conditionnement = db.Column(db.String(100))
    contenance_unitaire = db.Column(db.String(50))
    volume_total = db.Column(db.String(50))
    pays_origine = db.Column(db.String(100))
    usine = db.Column(db.String(200))
    dlc = db.Column(db.String(50))
    dlc_mois = db.Column(db.Integer)
    conservation = db.Column(db.Text)
    conservation_apres_ouverture = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    allergenes = db.Column(db.Text)
    traces = db.Column(db.Text)
    valeurs_nutritionnelles = db.Column(db.Text)
    certifications = db.Column(db.Text)
    labels = db.Column(db.Text)
    logistique = db.Column(db.Text)
    avis = db.Column(db.Text)
    tags = db.Column(db.Text)
    mots_cles = db.Column(db.Text)
    seo = db.Column(db.Text)
    date_ajout = db.Column(db.DateTime, default=datetime.now)
    date_maj = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    actif = db.Column(db.Boolean, default=True)
    en_promotion = db.Column(db.Boolean, default=False)
    nouveau = db.Column(db.Boolean, default=False)
    meilleure_vente = db.Column(db.Boolean, default=False)
    coup_coeur = db.Column(db.Boolean, default=False)
    image_principale = db.Column(db.String(200), default='default.jpg')
    images = db.Column(db.Text)
    videos = db.Column(db.Text)
    documents = db.Column(db.Text)
    views = db.Column(db.Integer, default=0)
    note_moyenne = db.Column(db.Float, default=0)
    note_count = db.Column(db.Integer, default=0)
    
    def prix_actuel(self):
        """Retourne le prix actuel (promo si disponible, sinon prix normal)"""
        return self.prix_promo if self.prix_promo else self.prix
    
    def est_en_promotion(self):
        """Vérifie si le produit est en promotion"""
        return self.prix_promo is not None and self.prix_promo < self.prix


class Commande(db.Model):
    __tablename__ = 'commande'
    
    id = db.Column(db.Integer, primary_key=True)
    _numero = db.Column('numero', db.String(20), unique=True, nullable=False)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    email_client = db.Column(db.String(120), nullable=False)
    nom_client = db.Column(db.String(200), nullable=False)
    telephone_client = db.Column(db.String(20))
    adresse_livraison = db.Column(db.Text, nullable=False)
    total = db.Column(db.Float, nullable=False)
    frais_port = db.Column(db.Float, default=0)
    reduction = db.Column(db.Float, default=0)
    total_final = db.Column(db.Float, nullable=False)
    statut = db.Column(db.String(50), default='en_attente')
    mode_paiement = db.Column(db.String(50))
    paiement_id = db.Column(db.String(100))
    promo_code = db.Column(db.String(50))
    date_creation = db.Column(db.DateTime, default=datetime.now)
    date_maj = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relations
    items = db.relationship('CommandeItem', backref='commande', lazy=True, cascade='all, delete-orphan')
    
    @property
    def numero(self):
        return self._numero
    
    @numero.setter
    def numero(self, value):
        self._numero = value
    
    def __init__(self, **kwargs):
        numero_value = kwargs.pop('numero', None)
        super(Commande, self).__init__(**kwargs)
        if numero_value:
            self._numero = numero_value
        else:
            self.generer_numero()
    
    def generer_numero(self):
        if not self._numero:
            date_part = datetime.now().strftime('%Y%m%d')
            random_part = random.randint(1000, 9999)
            self._numero = f"CMD-{date_part}-{random_part}"

class CommandeItem(db.Model):
    __tablename__ = 'commande_item'
    
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)
    
    # Relations
    produit = db.relationship('Produit')

class Paiement(db.Model):
    __tablename__ = 'paiement'
    
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    mode = db.Column(db.String(50))
    statut = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    date_paiement = db.Column(db.DateTime, default=datetime.now)

class Panier(db.Model):
    __tablename__ = 'panier'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=True)
    session_id = db.Column(db.String(100))
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    quantite = db.Column(db.Integer, default=1)
    date_ajout = db.Column(db.DateTime, default=datetime.now)
    
    # Relations
    produit = db.relationship('Produit')

class Avis(db.Model):
    __tablename__ = 'avis'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    note = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.now)
    
    # Relations
    produit = db.relationship('Produit')

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    date_ajout = db.Column(db.DateTime, default=datetime.now)
    
    # Relations
    utilisateur = db.relationship('Utilisateur', backref='favoris')
    produit = db.relationship('Produit')
    
    # Contrainte unique pour éviter les doublons
    __table_args__ = (db.UniqueConstraint('utilisateur_id', 'produit_id', name='unique_favoris'),)
