import sqlite3
import requests
import pandas as pd

# Connexion sqlite
conn = sqlite3.connect("/data/database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

url_magasin = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv"
url_produit = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv"
url_vente = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"

def attraper_url(url, type):
    try:
        response = requests.get(url)
        if response.status_code == 200 :
            return pd.read_csv(url)
    except Exception as e:
        print(f"Erreur lors de l'importation de {type} : {e}")

def insert_magasin(data):
    for _, row in data.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO magasin (id_magasin, ville, salaries)
            VALUES (?, ?, ?)
        """, (int(row['ID Magasin']), row['Ville'], int(row['Nombre de salariés'])))
    print("Données insérées dans la table magasin.")

def insert_produit(data):
    for _, row in data.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO produit (id_produit, nom, prix, stock)
            VALUES (?, ?, ?, ?)
        """, (row['ID Référence produit'], row['Nom'], float(row['Prix']), int(row['Stock'])))
    print("Données insérées dans la table produit.")

def insert_vente(data):
    for _, row in data.iterrows():
        cursor.execute("""
            SELECT COUNT(*) FROM vente WHERE date = ? AND id_magasin = ? AND id_produit = ?
        """, (row['Date'], row['ID Magasin'], row['ID Référence produit']))
        exists = cursor.fetchone()[0]
        if not exists:
            cursor.execute("""
                INSERT INTO vente (id_produit, date, quantite, id_magasin)
                VALUES (?, ?, ?, ?)
            """, (row['ID Référence produit'], row['Date'], int(row['Quantité']), int(row['ID Magasin'])))
            print(f"Nouvelle vente insérée : {row['ID Référence produit']} - {row['Date']}")
        else:
            print(f"Vente déjà existante : {row['ID Référence produit']} - {row['Date']}")
            
try:
    # Magasins
    magasins_data = attraper_url(url_magasin, "magasin")
    if magasins_data is not None:
        insert_magasin(magasins_data)

    # Produits
    produits_data = attraper_url(url_produit, "produit")
    if produits_data is not None:
        insert_produit(produits_data)

    # Ventes
    ventes_data = attraper_url(url_vente, "vente")
    if ventes_data is not None:
        insert_vente(ventes_data)

    conn.commit()
    print("Importation terminée avec succès.")

except Exception as e:
    print(f"Erreur lors de l'importation : {e}")


# ANALYSE

def calcul_ca():
    query = """
            SELECT SUM(p.prix * v.quantite) AS chiffre_affaires_total
            FROM vente v
            JOIN produit p ON v.id_produit = p.id_produit;
        """
    cursor.execute(query)
    result = cursor.fetchone()
    total_ca = result[0] if result[0] is not None else 0.0

    cursor.execute("""
                    INSERT INTO total_ca (chiffre_affaire)
                    VALUES (?)
                """, (total_ca,))
    print(f"Chiffre d'affaires total inséré dans la table `total_ca` : {total_ca} €")

def calcul_vente_pdt():
    query = """
            SELECT p.nom, SUM(v.quantite) AS total_quantite, SUM(p.prix * v.quantite) AS chiffre_affaires
            FROM vente v
            JOIN produit p ON v.id_produit = p.id_produit
            GROUP BY p.nom
            ORDER BY chiffre_affaires DESC;
        """
    cursor.execute(query)
    results = cursor.fetchall()

    for idx, row in enumerate(results, start=1):
        cursor.execute("""
                        INSERT OR REPLACE INTO vente_pdt (id, produit, ventes)
                        VALUES (?, ?, ?)
                    """, (idx, row[0], row[2]))
    print("Ventes par produit insérées dans la table `vente_pdt`.")

def calcul_vente_pdv():
    query = """
            SELECT m.ville, SUM(v.quantite) AS total_quantite, SUM(p.prix * v.quantite) AS chiffre_affaires
            FROM vente v
            JOIN magasin m ON v.id_magasin = m.id_magasin
            JOIN produit p ON v.id_produit = p.id_produit
            GROUP BY m.ville
            ORDER BY chiffre_affaires DESC;
        """
    cursor.execute(query)
    results = cursor.fetchall()

    for idx, row in enumerate(results, start=1):
        cursor.execute("""
                        INSERT OR REPLACE INTO vente_pdv (id, magasin, ventes)
                        VALUES (?, ?, ?)
                    """, (idx, row[0], row[2]))
    print("Ventes par région insérées dans la table `vente_pdv`.")

# Exécution des requêtes
calcul_ca()
conn.commit()
calcul_vente_pdt()
conn.commit()
calcul_vente_pdv()
conn.commit()
print("Analyse terminée.")

# Fermer la connexion à la base de données
conn.close()