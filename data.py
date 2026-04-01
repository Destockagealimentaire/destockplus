# data.py
from datetime import datetime, timedelta
import random

# Catégories
categories = [
    {
        "id": 1,
        "nom": "Boissons",
        "description": "Eaux, jus, sodas et boissons énergisantes",
        "image": "boissons.jpg",
        "ordre": 1,
        "icone": "🥤"
    },
    {
        "id": 2,
        "nom": "Vins, Champagnes et Spiritueux",
        "description": "Sélection de vins fins, champagnes prestige et spiritueux d'exception",
        "image": "vins.jpg",
        "ordre": 2,
        "icone": "🍾"
    },
    {
        "id": 3,
        "nom": "Produits frais",
        "description": "Fruits, légumes et produits frais du terroir",
        "image": "frais.jpg",
        "ordre": 3,
        "icone": "🥗"
    },
    {
        "id": 4,
        "nom": "Épicerie",
        "description": "Produits d'épicerie fine, pâtes, riz, conserves",
        "image": "epicerie.jpg",
        "ordre": 4,
        "icone": "🏺"
    },
    {
        "id": 5,
        "nom": "Surgelés",
        "description": "Plats préparés, légumes et produits surgelés qualité restaurant",
        "image": "surgeles.jpg",
        "ordre": 5,
        "icone": "❄️"
    },
    {
        "id": 6,
        "nom": "Produits laitiers",
        "description": "Lait, fromages, yaourts et produits laitiers frais",
        "image": "laitiers.jpg",
        "ordre": 6,
        "icone": "🥛"
    },
    {
        "id": 7,
        "nom": "Viandes et poissons",
        "description": "Viandes premium, poissons frais et produits de la mer",
        "image": "viandes.jpg",
        "ordre": 7,
        "icone": "🥩"
    },
    {
        "id": 8,
        "nom": "Promotions",
        "description": "Offres spéciales et destockage exceptionnel",
        "image": "promos.jpg",
        "ordre": 8,
        "icone": "🔥"
    },
    {
        "id": 9,
        "nom": "Électroménager",
        "description": "Appareils électroménagers professionnels et grand public",
        "image": "electromenager.jpg",
        "ordre": 9,
        "icone": "🔌"
    },
    {
        "id": 10,
        "nom": "Hygiène et entretien",
        "description": "Produits d'hygiène et d'entretien pour professionnels",
        "image": "hygiene.jpg",
        "ordre": 10,
        "icone": "🧼"
    }
]

# Mapping des catégories pour référence rapide
category_map = {cat["nom"]: cat["id"] for cat in categories}

# Produits complets avec toutes les informations
products = [
    # BOISSONS
    {
        "id": 100,
        "nom": "🥤 Palette de Coca-Cola Original – Bouteilles 1L",
        "description": "Palette complète de 144 bouteilles de Coca-Cola Original 1L. La boisson gazeuse iconique au goût unique, conditionnée en bouteilles PET 1L. Parfaite pour les cafés, restaurants, hôtels et distributeurs automatiques.",
        "description_courte": "Palette professionnelle de Coca-Cola 1L (144 bouteilles)",
        "prix": 229.00,
        "prix_original": 159.00,
        "prix_promo": 159.00,
        "devise": "EUR",
        "categorie_id": category_map["Boissons"],
        "categorie_nom": "Boissons",
        "stock": 105,
        "stock_initial": 150,
        "sku": "COC-1L-144-PAL",
        "upc": "5449000131805",
        "marque": "Coca-Cola",
        "fournisseur": "Coca-Cola European Partners",
        "poids": "72 kg",
        "poids_net": "64.8 kg",
        "dimensions": "120 x 80 x 120 cm",
        "volume_palette": "0.96 m³",
        "format": "Palette complète",
        "unites": 144,
        "type_conditionnement": "Bouteilles PET",
        "contenance_unitaire": "1 L",
        "volume_total": "144 L",
        "pays_origine": "France",
        "usine": "Clamart, France",
        "dlc": (datetime.now() + timedelta(days=365)).strftime("%d/%m/%Y"),
        "dlc_mois": 12,
        "conservation": "À l'abri du soleil et de la chaleur, température ambiante",
        "conservation_apres_ouverture": "À consommer dans les 3 jours après ouverture, réfrigérer",
        "ingredients": "Eau gazéifiée, sucre (106g/L), colorant: E150d, acidifiant: acide phosphorique (E338), arômes naturels, caféine (97mg/L)",
        "allergenes": [],
        "valeurs_nutritionnelles": {
            "portion": "250 ml",
            "energie_kcal": 105,
            "energie_kj": 445,
            "matieres_grasses_g": 0,
            "acides_gras_satures_g": 0,
            "glucides_g": 26.5,
            "sucres_g": 26.5,
            "fibres_g": 0,
            "proteines_g": 0,
            "sel_g": 0.02,
            "cafeine_mg": 24.3
        },
        "certifications": [
            "ISO 9001",
            "FSSC 22000",
            "Commerce équitable pour le sucre"
        ],
        "labels": [],
        "logistique": {
            "type_palette": "Europalette (EPAL)",
            "poids_palette": "72 kg",
            "hauteur_palette": "120 cm",
            "cartons_par_palette": 12,
            "unites_par_carton": 12,
            "poids_par_carton": "6 kg",
            "code_douane": "22021000",
            "temperature_transport": "Ambiante",
            "humidite_stockage": "< 75%",
            "manutention": "Transpalette ou chariot élévateur"
        },
        "avis": {
            "note_moyenne": 4.5,
            "nombre_avis": 45,
            "repartition_notes": {
                5: 28,
                4: 12,
                3: 3,
                2: 1,
                1: 1
            }
        },
        "tags": ["coca", "soda", "boisson gazeuse", "cola", "palette", "professionnel"],
        "mots_cles": ["Coca-Cola", "boisson", "gazeuse", "palette", "grossiste", "CHR"],
        "seo": {
            "title": "Palette Coca-Cola 1L - 144 bouteilles - Prix grossiste",
            "description": "Palette professionnelle de Coca-Cola 1L (144 bouteilles). Prix imbattable pour professionnels. Livraison rapide partout en France.",
            "keywords": ["coca-cola", "palette", "grossiste", "boisson", "restaurant", "café", "hôtel"]
        },
        "date_ajout": (datetime.now() - timedelta(days=30)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": True,
        "coup_coeur": False,
        "images": [
            "palette-coca-1.jpg",
            "palette-coca-2.jpg",
            "palette-coca-3.jpg"
        ],
        "videos": [],
        "documents": [
            {"nom": "Fiche technique", "url": "/docs/coca-1l-ft.pdf"},
            {"nom": "Certificat d'analyse", "url": "/docs/coca-1l-ca.pdf"}
        ]
    },
    {
        "id": 101,
        "nom": "🥤 Palette Red Bull 250ml (2592 canettes)",
        "description": "Palette complète de 2592 canettes Red Bull 250ml. La boisson énergisante originale, élaborée avec des ingrédients de haute qualité pour stimuler les performances physiques et mentales. Format professionnel idéal pour les distributeurs automatiques, événements sportifs, bars et night-clubs.",
        "description_courte": "Palette professionnelle Red Bull 250ml (2592 canettes)",
        "prix": 1942.80,
        "prix_original": 1800.00,
        "prix_promo": 1679.80,
        "devise": "EUR",
        "categorie_id": category_map["Boissons"],
        "categorie_nom": "Boissons",
        "stock": 8,
        "stock_initial": 20,
        "sku": "RED-25CL-2592-PAL",
        "upc": "9002490100070",
        "marque": "Red Bull",
        "fournisseur": "Red Bull GmbH",
        "poids": "720 kg",
        "poids_net": "648 kg",
        "dimensions": "120 x 100 x 180 cm",
        "volume_palette": "1.8 m³",
        "format": "Palette complète",
        "unites": 2592,
        "type_conditionnement": "Canettes aluminium",
        "contenance_unitaire": "250 ml",
        "volume_total": "648 L",
        "pays_origine": "Autriche",
        "usine": "Fuschl am See, Autriche",
        "dlc": (datetime.now() + timedelta(days=540)).strftime("%d/%m/%Y"),
        "dlc_mois": 18,
        "conservation": "À l'abri de la lumière et de la chaleur, température ambiante",
        "ingredients": "Eau gazéifiée, saccharose, glucose, acidifiant: acide citrique, taurine (0.4%), bicarbonate de sodium, carbonate de magnésium, caféine (32mg/100ml), vitamines: niacine, acide pantothénique, B6, B12, arômes",
        "allergenes": [],
        "valeurs_nutritionnelles": {
            "portion": "250 ml (1 canette)",
            "energie_kcal": 110,
            "energie_kj": 460,
            "matieres_grasses_g": 0,
            "acides_gras_satures_g": 0,
            "glucides_g": 27,
            "sucres_g": 27,
            "fibres_g": 0,
            "proteines_g": 0.4,
            "sel_g": 0.1,
            "cafeine_mg": 80,
            "taurine_mg": 1000,
            "vitamine_B6_mg": 2.1,
            "vitamine_B12_mcg": 2.5
        },
        "certifications": [
            "ISO 22000",
            "Halal",
            "Certification qualité autrichienne"
        ],
        "labels": [],
        "logistique": {
            "type_palette": "Europalette renforcée",
            "poids_palette": "720 kg",
            "hauteur_palette": "180 cm",
            "cartons_par_palette": 108,
            "unites_par_carton": 24,
            "poids_par_carton": "6.7 kg",
            "code_douane": "22021000",
            "temperature_transport": "Ambiante",
            "adr": "Non classé",
            "manutention": "Chariot élévateur nécessaire (poids > 500kg)"
        },
        "avis": {
            "note_moyenne": 4.8,
            "nombre_avis": 61,
            "repartition_notes": {
                5: 48,
                4: 10,
                3: 2,
                2: 1,
                1: 0
            }
        },
        "tags": ["red bull", "energy drink", "boisson énergisante", "canette", "palette", "professionnel", "distributeur"],
        "mots_cles": ["Red Bull", "energy drink", "boisson énergisante", "palette", "grossiste", "CHR", "bar", "night-club"],
        "seo": {
            "title": "Palette Red Bull 250ml - 2592 canettes - Prix grossiste",
            "description": "Palette professionnelle Red Bull 250ml (2592 canettes). La référence des boissons énergisantes. Prix imbattable pour professionnels. Livraison rapide.",
            "keywords": ["red bull", "palette", "grossiste", "energy drink", "boisson énergisante", "bar", "discothèque"]
        },
        "date_ajout": (datetime.now() - timedelta(days=15)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": True,
        "coup_coeur": True,
        "images": [
            "palette-redbull-1.jpg",
            "palette-redbull-2.jpg",
            "palette-redbull-3.jpg"
        ],
        "videos": [
            {"titre": "Présentation Red Bull", "url": "https://youtube.com/..."}
        ],
        "documents": [
            {"nom": "Fiche produit", "url": "/docs/redbull-ft.pdf"},
            {"nom": "Déclaration nutritionnelle", "url": "/docs/redbull-nutri.pdf"}
        ]
    },
    {
        "id": 102,
        "nom": "🥤 Fanta Orange 33cl (2592 canettes)",
        "description": "Palette complète de 2592 canettes de Fanta Orange 33cl. La boisson gazeuse fruitée à l'orange, pétillante et rafraîchissante. Conditionnement professionnel idéal pour les cafétérias, distributeurs automatiques, fast-foods et événements.",
        "description_courte": "Palette Fanta Orange 33cl (2592 canettes)",
        "prix": 1812.00,
        "prix_original": 1650.00,
        "prix_promo": 1512.00,
        "devise": "EUR",
        "categorie_id": category_map["Boissons"],
        "categorie_nom": "Boissons",
        "stock": 120,
        "stock_initial": 150,
        "sku": "FAN-33CL-2592-PAL",
        "upc": "5449000000996",
        "marque": "Fanta",
        "fournisseur": "The Coca-Cola Company",
        "poids": "780 kg",
        "poids_net": "712.8 kg",
        "dimensions": "120 x 100 x 180 cm",
        "volume_palette": "1.8 m³",
        "format": "Palette complète",
        "unites": 2592,
        "type_conditionnement": "Canettes aluminium",
        "contenance_unitaire": "330 ml",
        "volume_total": "855.36 L",
        "pays_origine": "France",
        "usine": "Grigny, France",
        "dlc": (datetime.now() + timedelta(days=270)).strftime("%d/%m/%Y"),
        "dlc_mois": 9,
        "conservation": "À l'abri de la lumière et de la chaleur",
        "ingredients": "Eau gazéifiée, jus d'orange à base de concentré (12%), sucre (4.6g/100ml), acidifiant: acide citrique, antioxydant: acide ascorbique, stabilisant: gomme de guar, arômes naturels d'orange, colorant: bêta-carotène",
        "allergenes": [],
        "valeurs_nutritionnelles": {
            "portion": "330 ml (1 canette)",
            "energie_kcal": 138,
            "energie_kj": 585,
            "matieres_grasses_g": 0,
            "acides_gras_satures_g": 0,
            "glucides_g": 35,
            "sucres_g": 35,
            "fibres_g": 0,
            "proteines_g": 0,
            "sel_g": 0.01,
            "vitamine_C_mg": 12
        },
        "certifications": [
            "ISO 9001",
            "FSSC 22000"
        ],
        "labels": [],
        "logistique": {
            "type_palette": "Europalette (EPAL)",
            "poids_palette": "780 kg",
            "hauteur_palette": "180 cm",
            "cartons_par_palette": 108,
            "unites_par_carton": 24,
            "poids_par_carton": "7.2 kg",
            "code_douane": "22021000",
            "temperature_transport": "Ambiante"
        },
        "avis": {
            "note_moyenne": 4.4,
            "nombre_avis": 37,
            "repartition_notes": {
                5: 22,
                4: 9,
                3: 4,
                2: 1,
                1: 1
            }
        },
        "tags": ["fanta", "orange", "soda", "boisson gazeuse", "palette", "canette"],
        "mots_cles": ["Fanta", "orange", "boisson", "gazeuse", "palette", "grossiste"],
        "seo": {
            "title": "Palette Fanta Orange 33cl - 2592 canettes - Prix grossiste",
            "description": "Palette professionnelle Fanta Orange 33cl (2592 canettes). La boisson fruitée préférée des Français. Prix compétitif pour professionnels.",
            "keywords": ["fanta", "orange", "palette", "grossiste", "boisson", "canette"]
        },
        "date_ajout": (datetime.now() - timedelta(days=60)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": True,
        "coup_coeur": False,
        "images": [
            "fanta-1.jpg",
            "fanta-2.jpg",
            "fanta-3.jpg"
        ],
        "videos": [],
        "documents": [
            {"nom": "Fiche technique", "url": "/docs/fanta-ft.pdf"}
        ]
    },
    {
        "id": 103,
        "nom": "⚡ Palette Monster Energy 500ml (2592 canettes)",
        "description": "Palette complète de 2592 canettes de Monster Energy 500ml. La boisson énergisante au profil intense, développée pour les sportifs et les amateurs de sensations fortes. Format XXL idéal pour les distributeurs, stations-service et événements.",
        "description_courte": "Palette Monster Energy 500ml (2592 canettes)",
        "prix": 2156.00,
        "prix_original": 1950.00,
        "prix_promo": 1756.00,
        "devise": "EUR",
        "categorie_id": category_map["Boissons"],
        "categorie_nom": "Boissons",
        "stock": 95,
        "stock_initial": 120,
        "sku": "MON-50CL-2592-PAL",
        "upc": "070847013125",
        "marque": "Monster Energy",
        "fournisseur": "Monster Beverage Corporation",
        "poids": "1450 kg",
        "poids_net": "1296 kg",
        "dimensions": "120 x 100 x 200 cm",
        "volume_palette": "2.0 m³",
        "format": "Palette complète",
        "unites": 2592,
        "type_conditionnement": "Canettes aluminium",
        "contenance_unitaire": "500 ml",
        "volume_total": "1296 L",
        "pays_origine": "États-Unis",
        "usine": "Corona, Californie",
        "dlc": (datetime.now() + timedelta(days=360)).strftime("%d/%m/%Y"),
        "dlc_mois": 12,
        "conservation": "Température ambiante, à l'abri de la chaleur",
        "ingredients": "Eau gazéifiée, saccharose, glucose, acide citrique, arômes naturels, taurine (0.4%), citrate de sodium, extrait de guarana, caféine (32mg/100ml), acide sorbique, acide benzoïque, niacine, pantothénate de calcium, vitamines B6 et B12, chlorure de sodium, glucuronolactone, inositol, caramel colorant",
        "allergenes": [],
        "valeurs_nutritionnelles": {
            "portion": "500 ml (1 canette)",
            "energie_kcal": 220,
            "energie_kj": 930,
            "matieres_grasses_g": 0,
            "acides_gras_satures_g": 0,
            "glucides_g": 55,
            "sucres_g": 54,
            "fibres_g": 0,
            "proteines_g": 0,
            "sel_g": 0.3,
            "cafeine_mg": 160,
            "taurine_mg": 2000,
            "vitamine_B6_mg": 4,
            "vitamine_B12_mcg": 5
        },
        "certifications": [
            "ISO 22000",
            "Kosher",
            "Halal"
        ],
        "labels": [],
        "logistique": {
            "type_palette": "Europalette renforcée",
            "poids_palette": "1450 kg",
            "hauteur_palette": "200 cm",
            "cartons_par_palette": 108,
            "unites_par_carton": 24,
            "poids_par_carton": "13.4 kg",
            "code_douane": "22021000",
            "temperature_transport": "Ambiante",
            "manutention": "Chariot élévateur haute capacité nécessaire"
        },
        "avis": {
            "note_moyenne": 4.2,
            "nombre_avis": 25,
            "repartition_notes": {
                5: 12,
                4: 8,
                3: 3,
                2: 1,
                1: 1
            }
        },
        "tags": ["monster", "energy", "boisson énergisante", "500ml", "palette"],
        "mots_cles": ["Monster", "energy drink", "boisson énergisante", "palette", "grossiste"],
        "seo": {
            "title": "Palette Monster Energy 500ml - 2592 canettes - Prix grossiste",
            "description": "Palette professionnelle Monster Energy 500ml (2592 canettes). La boisson énergisante américaine au goût intense. Prix compétitif pour professionnels.",
            "keywords": ["monster", "energy", "palette", "grossiste", "boisson énergisante"]
        },
        "date_ajout": (datetime.now() - timedelta(days=45)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": False,
        "coup_coeur": True,
        "images": [
            "monster-1.jpg",
            "monster-2.jpg",
            "monster-3.jpg"
        ],
        "videos": [],
        "documents": [
            {"nom": "Fiche technique Monster", "url": "/docs/monster-ft.pdf"}
        ]
    },
    {
        "id": 104,
        "nom": "🍊 Palette Orangina 33cl (2592 canettes)",
        "description": "Palette complète de 2592 canettes d'Orangina 33cl. La célèbre boisson pétillante à la pulpe d'orange, avec ses fines bulles et son goût unique. Un concentré de soleil en canette, parfait pour tous les moments de convivialité.",
        "description_courte": "Palette Orangina 33cl (2592 canettes)",
        "prix": 1928.80,
        "prix_original": 1650.00,
        "prix_promo": 1458.80,
        "devise": "EUR",
        "categorie_id": category_map["Boissons"],
        "categorie_nom": "Boissons",
        "stock": 110,
        "stock_initial": 150,
        "sku": "ORA-33CL-2592-PAL",
        "upc": "3088540004006",
        "marque": "Orangina",
        "fournisseur": "Orangina Suntory France",
        "poids": "780 kg",
        "poids_net": "712.8 kg",
        "dimensions": "120 x 100 x 180 cm",
        "volume_palette": "1.8 m³",
        "format": "Palette complète",
        "unites": 2592,
        "type_conditionnement": "Canettes aluminium",
        "contenance_unitaire": "330 ml",
        "volume_total": "855.36 L",
        "pays_origine": "France",
        "usine": "Marseille, France",
        "dlc": (datetime.now() + timedelta(days=240)).strftime("%d/%m/%Y"),
        "dlc_mois": 8,
        "conservation": "À l'abri de la lumière, température ambiante",
        "ingredients": "Eau gazéifiée, jus d'agrumes à base de concentrés 12% (orange 9%, pamplemousse, mandarine, citron), sucre, pulpe d'agrumes 2%, arômes naturels",
        "allergenes": [],
        "valeurs_nutritionnelles": {
            "portion": "330 ml (1 canette)",
            "energie_kcal": 128,
            "energie_kj": 540,
            "matieres_grasses_g": 0,
            "acides_gras_satures_g": 0,
            "glucides_g": 32,
            "sucres_g": 32,
            "fibres_g": 0,
            "proteines_g": 0,
            "sel_g": 0.01
        },
        "certifications": [
            "ISO 9001",
            "FSSC 22000"
        ],
        "labels": [],
        "logistique": {
            "type_palette": "Europalette (EPAL)",
            "poids_palette": "780 kg",
            "hauteur_palette": "180 cm",
            "cartons_par_palette": 108,
            "unites_par_carton": 24,
            "poids_par_carton": "7.2 kg",
            "code_douane": "22021000"
        },
        "avis": {
            "note_moyenne": 4.5,
            "nombre_avis": 30,
            "repartition_notes": {
                5: 18,
                4: 8,
                3: 3,
                2: 1,
                1: 0
            }
        },
        "tags": ["orangina", "orange", "pulpe", "boisson gazeuse", "palette"],
        "mots_cles": ["Orangina", "orange", "pulpe", "palette", "grossiste"],
        "seo": {
            "title": "Palette Orangina 33cl - 2592 canettes - Prix grossiste",
            "description": "Palette professionnelle Orangina 33cl (2592 canettes). La boisson à la pulpe d'orange iconique. Prix compétitif pour professionnels.",
            "keywords": ["orangina", "orange", "pulpe", "palette", "grossiste"]
        },
        "date_ajout": (datetime.now() - timedelta(days=90)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": True,
        "coup_coeur": False,
        "images": [
            "orangina-1.jpg",
            "orangina-2.jpg",
            "orangina-3.jpg"
        ],
        "videos": [],
        "documents": []
    },
    {
        "id": 105,
        "nom": "🍫 Palette Nutella 1kg (760 pots)",
        "description": "Palette complète de 760 pots de Nutella 1kg. La célèbre pâte à tartiner aux noisettes et au cacao, onctueuse et gourmande. Format professionnel idéal pour les cafés, boulangeries, hôtels et épiceries fines.",
        "description_courte": "Palette Nutella 1kg (760 pots)",
        "prix": 1936.00,
        "prix_original": 1820.00,
        "prix_promo": 1736.00,
        "devise": "EUR",
        "categorie_id": category_map["Épicerie"],
        "categorie_nom": "Épicerie",
        "stock": 80,
        "stock_initial": 100,
        "sku": "NUT-1KG-760-PAL",
        "upc": "8000500155428",
        "marque": "Nutella",
        "fournisseur": "Ferrero",
        "poids": "820 kg",
        "poids_net": "760 kg",
        "dimensions": "120 x 100 x 180 cm",
        "volume_palette": "1.8 m³",
        "format": "Palette complète",
        "unites": 760,
        "type_conditionnement": "Pots plastique avec opercule",
        "contenance_unitaire": "1 kg",
        "poids_total": "760 kg",
        "pays_origine": "France",
        "usine": "Villers-Écalles, France",
        "dlc": (datetime.now() + timedelta(days=360)).strftime("%d/%m/%Y"),
        "dlc_mois": 12,
        "conservation": "À l'abri de la chaleur et de l'humidité (18-22°C idéal)",
        "conservation_apres_ouverture": "6 mois à température ambiante, bien refermer",
        "ingredients": "Sucre, huile de palme, NOISETTES (13%), LAIT écrémé en poudre (8.7%), cacao maigre (7.4%), émulsifiant: lécithines de SOJA, vanilline",
        "allergenes": ["Lait", "Noisettes", "Soja"],
        "traces": ["Amandes", "Noix"],
        "valeurs_nutritionnelles": {
            "portion": "15g (1 cuillère à soupe)",
            "energie_kcal": 80,
            "energie_kj": 335,
            "matieres_grasses_g": 4.5,
            "acides_gras_satures_g": 1.5,
            "glucides_g": 9,
            "sucres_g": 8.5,
            "fibres_g": 0.5,
            "proteines_g": 1,
            "sel_g": 0.03
        },
        "certifications": [
            "ISO 9001",
            "FSSC 22000",
            "UTZ Certified pour le cacao"
        ],
        "labels": [
            "Huile de palme certifiée durable (RSPO)"
        ],
        "logistique": {
            "type_palette": "Europalette (EPAL)",
            "poids_palette": "820 kg",
            "hauteur_palette": "180 cm",
            "cartons_par_palette": 32,
            "unites_par_carton": 24,
            "poids_par_carton": "24.5 kg",
            "code_douane": "18063290",
            "temperature_transport": "Ambiante (<25°C)",
            "manutention": "Prévoir équipement de levage"
        },
        "avis": {
            "note_moyenne": 4.8,
            "nombre_avis": 45,
            "repartition_notes": {
                5: 35,
                4: 8,
                3: 2,
                2: 0,
                1: 0
            }
        },
        "tags": ["nutella", "pâte à tartiner", "noisette", "cacao", "palette", "professionnel"],
        "mots_cles": ["Nutella", "pâte à tartiner", "noisette", "chocolat", "palette", "grossiste", "CHR"],
        "seo": {
            "title": "Palette Nutella 1kg - 760 pots - Prix grossiste",
            "description": "Palette professionnelle Nutella 1kg (760 pots). La célèbre pâte à tartiner italienne. Prix imbattable pour professionnels. Livraison rapide.",
            "keywords": ["nutella", "pâte à tartiner", "palette", "grossiste", "restaurant", "café", "hôtel"]
        },
        "date_ajout": (datetime.now() - timedelta(days=20)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": True,
        "coup_coeur": True,
        "images": [
            "nutella-palette-1.jpg",
            "nutella-palette-2.jpg",
            "nutella-palette-3.jpg"
        ],
        "videos": [
            {"titre": "Visite de l'usine Nutella", "url": "https://youtube.com/..."}
        ],
        "documents": [
            {"nom": "Fiche produit Nutella", "url": "/docs/nutella-ft.pdf"},
            {"nom": "Certificat RSPO", "url": "/docs/nutella-rspo.pdf"}
        ]
    },
    {
        "id": 112,
        "nom": "🍪 Palette biscuits Nutella 304g (1200 paquets)",
        "description": "Palette complète de 1200 paquets de biscuits fourrés à la pâte Nutella (304g). Des biscuits croustillants à l'extérieur, fondants à l'intérieur grâce à leur cœur généreux de pâte Nutella. Format idéal pour la vente en grande surface, épiceries et distributeurs automatiques.",
        "description_courte": "Palette biscuits Nutella 304g (1200 paquets)",
        "prix": 1850.00,
        "prix_original": 1680.00,
        "prix_promo": 1600.00,
        "devise": "EUR",
        "categorie_id": category_map["Épicerie"],
        "categorie_nom": "Épicerie",
        "stock": 5,
        "stock_initial": 20,
        "sku": "BIS-NUT-304G-1200-PAL",
        "upc": "8000500421028",
        "marque": "Nutella",
        "fournisseur": "Ferrero",
        "poids": "396 kg",
        "poids_net": "364.8 kg",
        "dimensions": "120 x 100 x 160 cm",
        "volume_palette": "1.6 m³",
        "format": "Palette complète",
        "unites": 1200,
        "type_conditionnement": "Paquets individuels en sachet souple",
        "poids_unitaire": "304g",
        "poids_total": "364.8 kg",
        "pays_origine": "Pologne",
        "usine": "Warsaw, Pologne",
        "dlc": (datetime.now() + timedelta(days=270)).strftime("%d/%m/%Y"),
        "dlc_mois": 9,
        "conservation": "À l'abri de la chaleur et de l'humidité",
        "ingredients": "Farine de BLÉ, sucre, huiles végétales, NOISETTES (8%), cacao maigre, LAIT écrémé en poudre, sirop de glucose, poudres à lever (carbonates d'ammonium, carbonates de sodium), sel, émulsifiant: lécithines de SOJA, arômes",
        "allergenes": ["Gluten", "Lait", "Noisettes", "Soja"],
        "traces": ["Amandes", "Œufs"],
        "valeurs_nutritionnelles": {
            "portion": "30g (2 biscuits)",
            "energie_kcal": 150,
            "energie_kj": 630,
            "matieres_grasses_g": 7.5,
            "acides_gras_satures_g": 2.5,
            "glucides_g": 18,
            "sucres_g": 10,
            "fibres_g": 1,
            "proteines_g": 2.5,
            "sel_g": 0.15
        },
        "certifications": [
            "ISO 9001",
            "BRC Food"
        ],
        "labels": [],
        "logistique": {
            "type_palette": "Europalette (EPAL)",
            "poids_palette": "396 kg",
            "hauteur_palette": "160 cm",
            "cartons_par_palette": 50,
            "unites_par_carton": 24,
            "poids_par_carton": "7.3 kg",
            "code_douane": "19053199"
        },
        "avis": {
            "note_moyenne": 4.6,
            "nombre_avis": 20,
            "repartition_notes": {
                5: 12,
                4: 6,
                3: 2,
                2: 0,
                1: 0
            }
        },
        "tags": ["biscuits", "nutella", "fourrés", "snacking", "palette"],
        "mots_cles": ["biscuits", "Nutella", "fourrés", "palette", "grossiste"],
        "seo": {
            "title": "Palette biscuits Nutella 304g - 1200 paquets - Prix grossiste",
            "description": "Palette professionnelle de biscuits fourrés Nutella 304g (1200 paquets). Le snack gourmand préféré des Français. Prix compétitif.",
            "keywords": ["biscuits", "nutella", "fourrés", "palette", "grossiste", "snacking"]
        },
        "date_ajout": (datetime.now() - timedelta(days=10)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": False,
        "coup_coeur": True,
        "images": [
            "biscuits-nutella-1.jpg",
            "biscuits-nutella-2.jpg",
            "biscuits-nutella-3.jpg"
        ],
        "videos": [],
        "documents": []
    },
    {
        "id": 113,
        "nom": "🥤 Palette Coca-Cola 33cl (2592 canettes)",
        "description": "Palette complète de 2592 canettes de Coca-Cola 33cl. Le Coca-Cola original, la boisson la plus célèbre au monde, en format canette pratique pour tous les moments de convivialité. Conditionnement professionnel pour cafés, restaurants, hôtels, distributeurs et événements.",
        "description_courte": "Palette Coca-Cola 33cl (2592 canettes)",
        "prix": 2096.00,
        "prix_original": 1896.00,
        "prix_promo": 1596.00,
        "devise": "EUR",
        "categorie_id": category_map["Boissons"],
        "categorie_nom": "Boissons",
        "stock": 10,
        "stock_initial": 15,
        "sku": "COC-33CL-2592-PAL",
        "upc": "5449000000439",
        "marque": "Coca-Cola",
        "fournisseur": "Coca-Cola European Partners",
        "poids": "780 kg",
        "poids_net": "712.8 kg",
        "dimensions": "120 x 100 x 180 cm",
        "volume_palette": "1.8 m³",
        "format": "Palette complète",
        "unites": 2592,
        "type_conditionnement": "Canettes aluminium",
        "contenance_unitaire": "330 ml",
        "volume_total": "855.36 L",
        "pays_origine": "France",
        "usine": "Grigny, France",
        "dlc": (datetime.now() + timedelta(days=270)).strftime("%d/%m/%Y"),
        "dlc_mois": 9,
        "conservation": "À l'abri de la lumière et de la chaleur",
        "ingredients": "Eau gazéifiée, sucre (10.6g/100ml), colorant: E150d, acidifiant: acide phosphorique (E338), arômes naturels, caféine (97mg/L)",
        "allergenes": [],
        "valeurs_nutritionnelles": {
            "portion": "330 ml (1 canette)",
            "energie_kcal": 139,
            "energie_kj": 585,
            "matieres_grasses_g": 0,
            "acides_gras_satures_g": 0,
            "glucides_g": 35,
            "sucres_g": 35,
            "fibres_g": 0,
            "proteines_g": 0,
            "sel_g": 0.02,
            "cafeine_mg": 32
        },
        "certifications": [
            "ISO 9001",
            "FSSC 22000"
        ],
        "labels": [],
        "logistique": {
            "type_palette": "Europalette (EPAL)",
            "poids_palette": "780 kg",
            "hauteur_palette": "180 cm",
            "cartons_par_palette": 108,
            "unites_par_carton": 24,
            "poids_par_carton": "7.2 kg",
            "code_douane": "22021000"
        },
        "avis": {
            "note_moyenne": 4.4,
            "nombre_avis": 35,
            "repartition_notes": {
                5: 20,
                4: 10,
                3: 3,
                2: 1,
                1: 1
            }
        },
        "tags": ["coca", "coca-cola", "soda", "canette", "33cl", "palette"],
        "mots_cles": ["Coca-Cola", "canette", "33cl", "palette", "grossiste"],
        "seo": {
            "title": "Palette Coca-Cola 33cl - 2592 canettes - Prix grossiste",
            "description": "Palette professionnelle Coca-Cola 33cl (2592 canettes). La boisson iconique en format canette. Prix compétitif pour professionnels.",
            "keywords": ["coca-cola", "canette", "33cl", "palette", "grossiste", "CHR"]
        },
        "date_ajout": (datetime.now() - timedelta(days=5)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": True,
        "meilleure_vente": True,
        "coup_coeur": False,
        "images": [
            "coca-palette-1.jpg",
            "coca-palette-2.jpg",
            "coca-palette-3.jpg"
        ],
        "videos": [],
        "documents": [
            {"nom": "Fiche technique Coca-Cola", "url": "/docs/coca-ft.pdf"}
        ]
    },
    {
        "id": 114,
        "nom": "💧 Palette San Pellegrino 50cl (600 bouteilles)",
        "description": "Palette complète de 600 bouteilles en verre de San Pellegrino 50cl. L'eau minérale naturelle gazeuse italienne la plus réputée, avec ses fines bulles et son élégante bouteille. Idéale pour les restaurants gastronomiques, hôtels de luxe et épiceries fines.",
        "description_courte": "Palette San Pellegrino 50cl (600 bouteilles verre)",
        "prix": 890.00,
        "prix_original": 480.00,
        "prix_promo": 590.00,
        "devise": "EUR",
        "categorie_id": category_map["Boissons"],
        "categorie_nom": "Boissons",
        "stock": 8,
        "stock_initial": 15,
        "sku": "SAN-50CL-600-PAL",
        "upc": "8002270001037",
        "marque": "San Pellegrino",
        "fournisseur": "Sanpellegrino S.p.A.",
        "poids": "540 kg",
        "poids_net": "480 kg",
        "dimensions": "120 x 100 x 150 cm",
        "volume_palette": "1.5 m³",
        "format": "Palette complète",
        "unites": 600,
        "type_conditionnement": "Bouteilles verre consignées",
        "contenance_unitaire": "500 ml",
        "volume_total": "300 L",
        "pays_origine": "Italie",
        "usine": "San Pellegrino Terme, Italie",
        "dlc": (datetime.now() + timedelta(days=720)).strftime("%d/%m/%Y"),
        "dlc_mois": 24,
        "conservation": "À l'abri de la lumière, température ambiante",
        "composition_minerale": {
            "residu_sec": "920 mg/L à 180°C",
            "calcium": "175 mg/L",
            "magnesium": "52 mg/L",
            "sodium": "33 mg/L",
            "potassium": "3 mg/L",
            "sulfates": "460 mg/L",
            "bicarbonates": "250 mg/L",
            "chlorures": "60 mg/L",
            "silice": "30 mg/L",
            "pH": "7.2"
        },
        "caracteristiques": "Eau minérale naturelle gazeuse, source San Pellegrino Terme, gazéification naturelle",
        "certifications": [
            "ISO 9001",
            "BRC",
            "IFS"
        ],
        "labels": [],
        "logistique": {
            "type_palette": "Europalette (EPAL)",
            "poids_palette": "540 kg",
            "hauteur_palette": "150 cm",
            "cartons_par_palette": 24,
            "unites_par_carton": 25,
            "poids_par_carton": "22.5 kg",
            "code_douane": "22011010",
            "consigne_verre": "0.10€ par bouteille",
            "manutention": "Attention verre, prévoir équipement adapté"
        },
        "avis": {
            "note_moyenne": 4.7,
            "nombre_avis": 28,
            "repartition_notes": {
                5: 18,
                4: 7,
                3: 2,
                2: 1,
                1: 0
            }
        },
        "tags": ["san pellegrino", "eau gazeuse", "italie", "bouteille verre", "palette", "restaurant gastronomique"],
        "mots_cles": ["San Pellegrino", "eau gazeuse", "italienne", "verre", "palette", "grossiste", "CHR"],
        "seo": {
            "title": "Palette San Pellegrino 50cl - 600 bouteilles verre - Prix grossiste",
            "description": "Palette professionnelle San Pellegrino 50cl (600 bouteilles verre). L'eau gazeuse italienne de prestige. Prix compétitif pour restaurants et hôtels.",
            "keywords": ["san pellegrino", "eau gazeuse", "italienne", "verre", "palette", "restaurant", "hôtel"]
        },
        "date_ajout": (datetime.now() - timedelta(days=25)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": True,
        "coup_coeur": True,
        "images": [
            "san-pellegrino-1.jpg",
            "san-pellegrino-2.jpg",
            "san-pellegrino-3.jpg"
        ],
        "videos": [],
        "documents": [
            {"nom": "Fiche technique San Pellegrino", "url": "/docs/sanpellegrino-ft.pdf"},
            {"nom": "Analyse minérale", "url": "/docs/sanpellegrino-analyse.pdf"}
        ]
    },
    {
        "id": 115,
        "nom": "🍺 Palette Heineken 33cl (2592 canettes)",
        "description": "Palette complète de 2592 canettes de bière Heineken 33cl. La célèbre bière blonde lager néerlandaise, brassée avec des ingrédients 100% naturels et une levure unique A-yeast. Goût équilibré, amertume subtile et arômes fruités. Conditionnement professionnel pour bars, restaurants, hôtels et événements.",
        "description_courte": "Palette Heineken 33cl (2592 canettes)",
        "prix": 2156.00,
        "prix_original": 1850.00,
        "prix_promo": 1656.00,
        "devise": "EUR",
        "categorie_id": category_map["Boissons"],
        "categorie_nom": "Boissons",
        "stock": 6,
        "stock_initial": 12,
        "sku": "HEI-33CL-2592-PAL",
        "upc": "8712000007089",
        "marque": "Heineken",
        "fournisseur": "Heineken N.V.",
        "poids": "780 kg",
        "poids_net": "712.8 kg",
        "dimensions": "120 x 100 x 180 cm",
        "volume_palette": "1.8 m³",
        "format": "Palette complète",
        "unites": 2592,
        "type_conditionnement": "Canettes aluminium",
        "contenance_unitaire": "330 ml",
        "volume_total": "855.36 L",
        "pays_origine": "Pays-Bas",
        "usine": "Zoeterwoude, Pays-Bas",
        "dlc": (datetime.now() + timedelta(days=360)).strftime("%d/%m/%Y"),
        "dlc_mois": 12,
        "conservation": "À l'abri de la lumière, température ambiante idéalement 10-15°C",
        "conseils_service": "Servir frais entre 4-6°C dans un verre tulipe pour révéler les arômes",
        "ingredients": "Eau, malt d'ORGE, houblon, levure (A-yeast)",
        "allergenes": ["Gluten (Orge)"],
        "alcool": "5% vol",
        "caracteristiques_brassage": "Fermentation basse, 100% naturelle sans additifs",
        "ibu": 20,
        "ebc": 8,
        "valeurs_nutritionnelles": {
            "portion": "330 ml (1 canette)",
            "energie_kcal": 139,
            "energie_kj": 585,
            "matieres_grasses_g": 0,
            "acides_gras_satures_g": 0,
            "glucides_g": 9.5,
            "sucres_g": 0.5,
            "proteines_g": 1.2,
            "sel_g": 0.02
        },
        "certifications": [
            "ISO 9001",
            "ISO 14001",
            "OHSAS 18001",
            "Halal",
            "Kosher"
        ],
        "labels": [
            "Brasserie durable",
            "Emballage recyclable"
        ],
        "logistique": {
            "type_palette": "Europalette (EPAL)",
            "poids_palette": "780 kg",
            "hauteur_palette": "180 cm",
            "cartons_par_palette": 108,
            "unites_par_carton": 24,
            "poids_par_carton": "7.2 kg",
            "code_douane": "22030001",
            "temperature_transport": "Ambiante, éviter le gel"
        },
        "avis": {
            "note_moyenne": 4.3,
            "nombre_avis": 32,
            "repartition_notes": {
                5: 15,
                4: 10,
                3: 5,
                2: 1,
                1: 1
            }
        },
        "tags": ["heineken", "bière", "lager", "blonde", "canette", "palette", "bar", "restaurant"],
        "mots_cles": ["Heineken", "bière", "blonde", "lager", "néerlandaise", "palette", "grossiste", "CHR"],
        "seo": {
            "title": "Palette Heineken 33cl - 2592 canettes - Prix grossiste",
            "description": "Palette professionnelle Heineken 33cl (2592 canettes). La bière blonde lager la plus vendue au monde. Prix compétitif pour bars et restaurants.",
            "keywords": ["heineken", "bière", "blonde", "lager", "canette", "palette", "grossiste", "bar"]
        },
        "date_ajout": (datetime.now() - timedelta(days=40)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": True,
        "coup_coeur": False,
        "images": [
            "heineken-1.jpg",
            "heineken-2.jpg",
            "heineken-3.jpg"
        ],
        "videos": [
            {"titre": "Brasserie Heineken", "url": "https://youtube.com/..."}
        ],
        "documents": [
            {"nom": "Fiche produit Heineken", "url": "/docs/heineken-ft.pdf"},
            {"nom": "Certificat d'analyse", "url": "/docs/heineken-ca.pdf"}
        ]
    },
    {
        "id": 116,
        "nom": "💧 Palette Perrier fines bulles 50cl (960 bouteilles)",
        "description": "Palette complète de 960 bouteilles en verre de Perrier fines bulles 50cl. L'eau minérale naturelle gazeuse française emblématique, avec ses bulles fines et élégantes, puisée à la source de Vergèze. La référence de l'eau pétillante pour les établissements prestigieux.",
        "description_courte": "Palette Perrier fines bulles 50cl (960 bouteilles verre)",
        "prix": 1290.00,
        "prix_original": 1250.00,
        "prix_promo": 1190.00,
        "devise": "EUR",
        "categorie_id": category_map["Boissons"],
        "categorie_nom": "Boissons",
        "stock": 7,
        "stock_initial": 12,
        "sku": "PER-50CL-960-PAL",
        "upc": "3038350005724",
        "marque": "Perrier",
        "fournisseur": "Nestlé Waters",
        "poids": "820 kg",
        "poids_net": "720 kg",
        "dimensions": "120 x 100 x 160 cm",
        "volume_palette": "1.6 m³",
        "format": "Palette complète",
        "unites": 960,
        "type_conditionnement": "Bouteilles verre",
        "contenance_unitaire": "500 ml",
        "volume_total": "480 L",
        "pays_origine": "France",
        "usine": "Vergèze, France",
        "dlc": (datetime.now() + timedelta(days=720)).strftime("%d/%m/%Y"),
        "dlc_mois": 24,
        "conservation": "À l'abri de la lumière, température ambiante",
        "conseils_service": "Servir frais (6-8°C) pour apprécier la finesse des bulles",
        "composition_minerale": {
            "residu_sec": "475 mg/L à 180°C",
            "calcium": "140 mg/L",
            "magnesium": "3 mg/L",
            "sodium": "9 mg/L",
            "potassium": "1 mg/L",
            "sulfates": "35 mg/L",
            "bicarbonates": "345 mg/L",
            "chlorures": "20 mg/L",
            "nitrates": "<2 mg/L",
            "pH": "5.6"
        },
        "caracteristiques": "Eau minérale naturelle gazeuse de la Source Perrier, gaz carbonique naturel des profondeurs volcaniques",
        "certifications": [
            "ISO 9001",
            "ISO 14001",
            "BRC",
            "IFS"
        ],
        "labels": [],
        "logistique": {
            "type_palette": "Europalette (EPAL)",
            "poids_palette": "820 kg",
            "hauteur_palette": "160 cm",
            "cartons_par_palette": 40,
            "unites_par_carton": 24,
            "poids_par_carton": "20.5 kg",
            "code_douane": "22011010",
            "consigne_verre": "0.10€ par bouteille"
        },
        "avis": {
            "note_moyenne": 4.6,
            "nombre_avis": 22,
            "repartition_notes": {
                5: 14,
                4: 5,
                3: 2,
                2: 1,
                1: 0
            }
        },
        "tags": ["perrier", "eau gazeuse", "fines bulles", "france", "verre", "palette"],
        "mots_cles": ["Perrier", "eau gazeuse", "fines bulles", "française", "verre", "palette", "grossiste"],
        "seo": {
            "title": "Palette Perrier fines bulles 50cl - 960 bouteilles verre - Prix grossiste",
            "description": "Palette professionnelle Perrier fines bulles 50cl (960 bouteilles verre). L'eau gazeuse française emblématique. Prix compétitif pour CHR.",
            "keywords": ["perrier", "eau gazeuse", "fines bulles", "verre", "palette", "restaurant"]
        },
        "date_ajout": (datetime.now() - timedelta(days=35)).isoformat(),
        "date_maj": datetime.now().isoformat(),
        "actif": True,
        "en_promotion": True,
        "nouveau": False,
        "meilleure_vente": True,
        "coup_coeur": False,
        "images": [
            "perrier-1.jpg",
            "perrier-2.jpg",
            "perrier-3.jpg"
        ],
        "videos": [],
        "documents": [
            {"nom": "Fiche technique Perrier", "url": "/docs/perrier-ft.pdf"}
        ]
    }
    # ... (je continue avec les autres produits si nécessaire)
]

def get_product_by_id(product_id):
    """Récupère un produit par son ID"""
    for product in products:
        if product["id"] == product_id:
            return product
    return None

def get_products_by_category(category_id):
    """Récupère les produits d'une catégorie"""
    return [p for p in products if p["categorie_id"] == category_id]

def get_promotions():
    """Récupère les produits en promotion"""
    return [p for p in products if p.get("en_promotion", False)]

def get_best_sellers(limit=10):
    """Récupère les meilleures ventes"""
    best_sellers = [p for p in products if p.get("meilleure_vente", False)]
    # Trier par note moyenne
    return sorted(best_sellers, key=lambda x: x.get("avis", {}).get("note_moyenne", 0), reverse=True)[:limit]

def get_new_products(days=30):
    """Récupère les produits ajoutés récemment"""
    cutoff = datetime.now() - timedelta(days=days)
    return [p for p in products if datetime.fromisoformat(p["date_ajout"]) > cutoff]

def search_products(query):
    """Recherche de produits"""
    query = query.lower()
    results = []
    for product in products:
        if (query in product["nom"].lower() or 
            query in product["description"].lower() or
            any(query in tag.lower() for tag in product.get("tags", []))):
            results.append(product)
    return results

def get_related_products(product_id, limit=4):
    """Récupère des produits similaires"""
    product = get_product_by_id(product_id)
    if not product:
        return []
    
    # Produits de même catégorie, excluant le produit actuel
    same_category = [p for p in products if p["categorie_id"] == product["categorie_id"] and p["id"] != product_id]
    
    # Trier par similarité de tags
    product_tags = set(product.get("tags", []))
    scored_products = []
    for p in same_category:
        p_tags = set(p.get("tags", []))
        common_tags = len(product_tags & p_tags)
        scored_products.append((common_tags, p))
    
    scored_products.sort(reverse=True)
    return [p for _, p in scored_products[:limit]]

def get_categories():
    """Récupère toutes les catégories"""
    return categories

def get_category_by_id(category_id):
    """Récupère une catégorie par son ID"""
    for category in categories:
        if category["id"] == category_id:
            return category
    return None

def get_category_by_name(category_name):
    """Récupère une catégorie par son nom"""
    for category in categories:
        if category["nom"] == category_name:
            return category
    return None

# Export des fonctions
__all__ = [
    'categories',
    'products',
    'get_product_by_id',
    'get_products_by_category',
    'get_promotions',
    'get_best_sellers',
    'get_new_products',
    'search_products',
    'get_related_products',
    'get_categories',
    'get_category_by_id',
    'get_category_by_name',
    'category_map'
]
