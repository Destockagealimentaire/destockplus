# email_service.py - Créez ce fichier

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from datetime import datetime

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"  # ou votre serveur SMTP
        self.smtp_port = 587
        self.sender_email = "commandes@destockpro.fr"
        self.sender_password = "votre-mot-de-passe"  # À configurer dans les variables d'environnement
        self.company_name = "DestockPro"
        self.company_address = "123 Avenue du Commerce, 75001 Paris"
        self.company_phone = "01 23 45 67 89"
        self.company_email = "contact@destockpro.fr"
        self.company_siret = "123 456 789 00012"
    
    def send_order_confirmation(self, commande, client_email, client_nom):
        """Envoie un email de confirmation de commande professionnel"""
        
        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Confirmation de votre commande {commande.numero} - DestockPro"
        msg['From'] = f"DestockPro <{self.sender_email}>"
        msg['To'] = client_email
        
        # Version HTML de l'email
        html = self._generate_order_html(commande, client_nom)
        
        # Attacher la version HTML
        msg.attach(MIMEText(html, 'html'))
        
        # Envoyer l'email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Erreur envoi email: {e}")
            return False
    
    def _generate_order_html(self, commande, client_nom):
        """Génère le HTML de l'email de confirmation"""
        
        # Calculer les totaux
        sous_total = commande.total
        frais_port = commande.frais_port or 0
        reduction = commande.reduction or 0
        total_ttc = sous_total + frais_port - reduction
        
        # Générer le HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1a1a1a, #2a2a2a); color: #c4a747; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .header h1 {{ margin: 0; font-size: 28px; }}
                .header p {{ color: #fff; margin: 5px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .order-info {{ background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #c4a747; }}
                .order-info h2 {{ color: #1a1a1a; margin-top: 0; }}
                .order-number {{ font-size: 24px; font-weight: bold; color: #c4a747; margin: 10px 0; }}
                .table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .table th {{ background: #1a1a1a; color: #fff; padding: 12px; text-align: left; }}
                .table td {{ padding: 12px; border-bottom: 1px solid #ddd; }}
                .table tr:last-child td {{ border-bottom: none; }}
                .totals {{ background: #fff; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .total-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee; }}
                .total-row.final {{ font-size: 20px; font-weight: bold; color: #c4a747; border-bottom: none; padding-top: 15px; }}
                .footer {{ text-align: center; padding: 30px; color: #666; font-size: 14px; border-top: 1px solid #ddd; margin-top: 30px; }}
                .btn {{ display: inline-block; padding: 12px 30px; background: #c4a747; color: #1a1a1a; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 20px 0; }}
                .company-details {{ background: #f0f0f0; padding: 15px; border-radius: 5px; font-size: 13px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏢 DestockPro</h1>
                    <p>Confirmation de commande</p>
                </div>
                
                <div class="content">
                    <p>Bonjour <strong>{client_nom}</strong>,</p>
                    
                    <p>Nous vous remercions pour votre commande. Celle-ci a bien été enregistrée et sera traitée dans les plus brefs délais.</p>
                    
                    <div class="order-info">
                        <h2>Récapitulatif de votre commande</h2>
                        <div class="order-number">N° {commande.numero}</div>
                        <p><strong>Date :</strong> {commande.date_creation.strftime('%d/%m/%Y à %H:%M')}</p>
                        <p><strong>Mode de paiement :</strong> {self._format_payment_method(commande.mode_paiement)}</p>
                        <p><strong>Statut :</strong> <span style="color: #c4a747;">{self._format_status(commande.statut)}</span></p>
                    </div>
                    
                    <h3>Détail des articles</h3>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Produit</th>
                                <th>Quantité</th>
                                <th>Prix unitaire</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        
        # Ajouter chaque article
        for item in commande.items:
            html += f"""
                            <tr>
                                <td>{item.produit.nom}</td>
                                <td>{item.quantite}</td>
                                <td>{item.prix_unitaire:.2f} €</td>
                                <td>{(item.quantite * item.prix_unitaire):.2f} €</td>
                            </tr>
            """
        
        html += f"""
                        </tbody>
                    </table>
                    
                    <div class="totals">
                        <div class="total-row">
                            <span>Sous-total</span>
                            <span>{sous_total:.2f} €</span>
                        </div>
                        <div class="total-row">
                            <span>Frais de livraison</span>
                            <span>{frais_port:.2f} €</span>
                        </div>
        """
        
        if reduction > 0:
            html += f"""
                        <div class="total-row" style="color: #00b894;">
                            <span>Réduction</span>
                            <span>-{reduction:.2f} €</span>
                        </div>
            """
        
        html += f"""
                        <div class="total-row final">
                            <span>Total TTC</span>
                            <span>{total_ttc:.2f} €</span>
                        </div>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="https://destockpro.fr/suivi-commande?numero={commande.numero}" class="btn">
                            Suivre ma commande
                        </a>
                    </div>
                    
                    <div class="company-details">
                        <p><strong>{self.company_name}</strong><br>
                        {self.company_address}<br>
                        Tél : {self.company_phone}<br>
                        Email : {self.company_email}<br>
                        SIRET : {self.company_siret}</p>
                    </div>
                    
                    <div class="footer">
                        <p>Cet email est un accusé de réception automatique. Merci de ne pas y répondre.</p>
                        <p>© 2024 DestockPro. Tous droits réservés.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _format_payment_method(self, method):
        methods = {
            'carte': 'Carte bancaire',
            'virement': 'Virement bancaire',
            'paypal': 'PayPal'
        }
        return methods.get(method, method)
    
    def _format_status(self, status):
        statuses = {
            'en_attente_paiement': 'En attente de paiement',
            'en_attente_virement': 'En attente de virement',
            'confirmee': 'Confirmée',
            'expediee': 'Expédiée',
            'livree': 'Livrée',
            'annulee': 'Annulée'
        }
        return statuses.get(status, status)