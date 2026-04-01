#!/bin/bash

# Script de déploiement pour DestockPro

echo "🚀 Déploiement de DestockPro - Site de destockage alimentaire"
echo "=============================================================="

# Variables
PROJECT_DIR="/var/www/destockpro"
VENV_DIR="$PROJECT_DIR/venv"
REPO_URL="https://github.com/votre-repo/destockpro.git"

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERREUR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[ATTENTION] $1${NC}"
}

# Vérification des prérequis
check_prerequisites() {
    log "🔍 Vérification des prérequis..."
    
    if ! command -v python3 &> /dev/null; then
        error "Python3 n'est pas installé"
        exit 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        error "pip3 n'est pas installé"
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        error "git n'est pas installé"
        exit 1
    fi
    
    if ! command -v nginx &> /dev/null; then
        warning "Nginx n'est pas installé (optionnel)"
    fi
    
    log "✅ Prérequis vérifiés"
}

# Création de la structure de dossiers
create_directory_structure() {
    log "📁 Création de la structure de dossiers..."
    
    mkdir -p $PROJECT_DIR
    mkdir -p $PROJECT_DIR/static/images/produits
    mkdir -p $PROJECT_DIR/static/images/categories
    mkdir -p $PROJECT_DIR/static/css
    mkdir -p $PROJECT_DIR/static/js
    mkdir -p $PROJECT_DIR/logs
    mkdir -p $PROJECT_DIR/backups
    
    log "✅ Structure de dossiers créée"
}

# Installation de l'environnement virtuel
setup_virtualenv() {
    log "🐍 Configuration de l'environnement virtuel..."
    
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv $VENV_DIR
        log "✅ Environnement virtuel créé"
    else
        log "✅ Environnement virtuel existant"
    fi
    
    source $VENV_DIR/bin/activate
    pip install --upgrade pip
    pip install -r $PROJECT_DIR/requirements.txt
    log "✅ Dépendances installées"
}

# Configuration des variables d'environnement
setup_environment() {
    log "🔧 Configuration des variables d'environnement..."
    
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        cat > $PROJECT_DIR/.env << EOF
# Configuration Flask
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
FLASK_ENV=production
FLASK_APP=app.py

# Base de données
DATABASE_URL=sqlite:///destockage.db

# Stripe (à modifier)
STRIPE_PUBLIC_KEY=pk_test_votre_cle
STRIPE_SECRET_KEY=sk_test_votre_cle

# Telegram
TELEGRAM_BOT_TOKEN=votre_token_telegram
TELEGRAM_CHAT_ID=votre_chat_id

# Email
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@destockpro.fr
EOF
        log "✅ Fichier .env créé"
        warning "⚠️ Veuillez modifier les clés API dans le fichier .env"
    else
        log "✅ Fichier .env existant"
    fi
}

# Initialisation de la base de données
init_database() {
    log "🗄️ Initialisation de la base de données..."
    
    source $VENV_DIR/bin/activate
    cd $PROJECT_DIR
    python init_db.py
    
    log "✅ Base de données initialisée"
}

# Configuration de Nginx (optionnel)
setup_nginx() {
    if command -v nginx &> /dev/null; then
        log "🌐 Configuration de Nginx..."
        
        cat > /etc/nginx/sites-available/destockpro << EOF
server {
    listen 80;
    server_name destockpro.fr www.destockpro.fr;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /static {
        alias $PROJECT_DIR/static;
        expires 30d;
    }
    
    location /images {
        alias $PROJECT_DIR/static/images;
        expires 30d;
    }
}
EOF
        
        ln -sf /etc/nginx/sites-available/destockpro /etc/nginx/sites-enabled/
        nginx -t && systemctl reload nginx
        log "✅ Nginx configuré"
    fi
}

# Configuration de systemd pour le service
setup_systemd() {
    log "⚙️ Configuration du service systemd..."
    
    cat > /etc/systemd/system/destockpro.service << EOF
[Unit]
Description=DestockPro Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    systemctl enable destockpro
    systemctl start destockpro
    
    log "✅ Service systemd configuré"
}

# Backup de la base de données
backup_database() {
    log "💾 Création d'une sauvegarde..."
    
    BACKUP_FILE="$PROJECT_DIR/backups/destockpro_$(date +'%Y%m%d_%H%M%S').db"
    cp $PROJECT_DIR/instance/destockage.db $BACKUP_FILE
    gzip $BACKUP_FILE
    
    # Garder seulement les 10 dernières sauvegardes
    cd $PROJECT_DIR/backups
    ls -t *.gz | tail -n +11 | xargs -r rm
    
    log "✅ Sauvegarde créée : $(basename $BACKUP_FILE.gz)"
}

# Logs rotation
setup_logrotate() {
    log "📝 Configuration de logrotate..."
    
    cat > /etc/logrotate.d/destockpro << EOF
$PROJECT_DIR/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload destockpro > /dev/null 2>&1 || true
    endscript
}
EOF
    
    log "✅ Logrotate configuré"
}

# Configuration SSL avec Let's Encrypt (optionnel)
setup_ssl() {
    if command -v certbot &> /dev/null; then
        log "🔒 Configuration SSL..."
        
        certbot --nginx -d destockpro.fr -d www.destockpro.fr --non-interactive --agree-tos --email admin@destockpro.fr
        
        log "✅ SSL configuré"
    else
        warning "certbot non installé, SSL non configuré"
    fi
}

# Installation principale
main() {
    log "🚀 Début de l'installation de DestockPro"
    
    check_prerequisites
    create_directory_structure
    
    # Cloner ou mettre à jour le code
    if [ ! -d "$PROJECT_DIR/.git" ]; then
        log "📥 Clonage du dépôt..."
        git clone $REPO_URL $PROJECT_DIR
    else
        log "🔄 Mise à jour du code..."
        cd $PROJECT_DIR
        git pull
    fi
    
    setup_virtualenv
    setup_environment
    init_database
    setup_nginx
    setup_systemd
    setup_logrotate
    setup_ssl
    backup_database
    
    log "✅ Installation terminée avec succès !"
    log "🌐 Accédez à votre site : http://destockpro.fr"
    log "📧 Admin: admin@destockpro.fr / admin123"
    log "⚠️ N'oubliez pas de :"
    log "   1. Modifier les mots de passe par défaut"
    log "   2. Configurer les clés API Stripe"
    log "   3. Configurer le token Telegram"
    log "   4. Mettre à jour les informations de contact"
}

# Exécution
main