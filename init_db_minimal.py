#!/usr/bin/env python3
"""Script minimal pour créer la base de données"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# Créer une application Flask temporaire
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///destockage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser SQLAlchemy
db = SQLAlchemy(app)

# Définir les modèles
class Utilisateur(db.Model):
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
    role = db.Column(db.String(20), default='client')
    actif = db.Column(db.Boolean, default=True)
    date_inscription = db.Column(db.DateTime, default=datetime.now)

class Categorie(db.Model):
    __tablename__ = 'categorie'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ordre = db.Column(db.Integer, default=0)

class Produit(db.Model):
    __tablename__ = 'produit'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    prix = db.Column(db.Float, nullable=False)
    prix_promo = db.Column(db.Float)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'))
    stock = db.Column(db.Integer, default=0)
    image_principale = db.Column(db.String(200), default='default.jpg')
    en_promotion = db.Column(db.Boolean, default=False)
    meilleure_vente = db.Column(db.Boolean, default=False)
    actif = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    note_moyenne = db.Column(db.Float, default=0)
    note_count = db.Column(db.Integer, default=0)
    date_creation = db.Column(db.DateTime, default=datetime.now)

class Commande(db.Model):
    __tablename__ = 'commande'
    id = db.Column(db.Integer, primary_key=True)
    _numero = db.Column('numero', db.String(20), unique=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
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
    promo_code = db.Column(db.String(50))
    date_creation = db.Column(db.DateTime, default=datetime.now)
    
    @property
    def numero(self):
        return self._numero
    
    @numero.setter
    def numero(self, value):
        self._numero = value

class CommandeItem(db.Model):
    __tablename__ = 'commande_item'
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)

print("🚀 CRÉATION DE LA BASE DE DONNÉES")
print("=" * 50)

with app.app_context():
    # Supprimer et recréer
    print("📦 Suppression des anciennes tables...")
    db.drop_all()
    
    print("🔨 Création des tables...")
    db.create_all()
    
    # Vérifier les tables
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"✅ Tables créées: {', '.join(tables)}")
    
    # Ajouter l'admin
    print("\n👤 Création de l'admin...")
    admin = Utilisateur(
        email='admin@destockpro.fr',
        password=generate_password_hash('admin123'),
        nom='Admin',
        prenom='Super',
        role='admin',
        actif=True
    )
    db.session.add(admin)
    
    # Ajouter un test
    test = Utilisateur(
        email='test@test.fr',
        password=generate_password_hash('test123'),
        nom='Test',
        prenom='Utilisateur',
        role='client',
        actif=True,
        adresse='123 rue de test',
        code_postal='75001',
        ville='Paris'
    )
    db.session.add(test)
    db.session.commit()
    print("✅ Admin: admin@destockpro.fr / admin123")
    print("✅ Test: test@test.fr / test123")
    
    # Ajouter une commande test
    print("\n📝 Création d'une commande test...")
    commande = Commande(
        utilisateur_id=admin.id,
        email_client=admin.email,
        nom_client=f"{admin.prenom} {admin.nom}",
        adresse_livraison="123 rue du commerce, 75001 Paris",
        total=150.00,
        frais_port=10.00,
        reduction=0,
        total_final=160.00,
        statut='confirmee',
        mode_paiement='virement'
    )
    commande.numero = f"CMD-TEST-{datetime.now().strftime('%Y%m%d')}-001"
    db.session.add(commande)
    db.session.commit()
    print(f"✅ Commande test: ID={commande.id}, Numéro={commande.numero}")
    
    # Vérification finale
    print("\n" + "=" * 50)
    print("🔍 VÉRIFICATION")
    print("=" * 50)
    print(f"Utilisateurs: {Utilisateur.query.count()}")
    print(f"Commandes: {Commande.query.count()}")
    
    # Afficher les commandes
    orders = Commande.query.all()
    for o in orders:
        print(f"   Commande: {o.numero} - Utilisateur ID: {o.utilisateur_id} - Total: {o.total_final}€")
    
    print("\n✅ BASE DE DONNÉES CRÉÉE AVEC SUCCÈS !")

print("\n💡 Lancez maintenant: python3 app.py")