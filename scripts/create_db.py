print("Hello, World !")

import sqlite3

# Connexion sqlite
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS magasin (
    id_magasin INTEGER NOT NULL,
    ville      VARCHAR NOT NULL,
    salaries   INTEGER NOT NULL,
    PRIMARY KEY (id_magasin)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produit (
    id_produit VARCHAR NOT NULL,
    nom        VARCHAR NOT NULL,
    prix       REAL    NOT NULL,
    stock      INTEGER NOT NULL,
    PRIMARY KEY (id_produit)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS total_ca (
    id              INTEGER NOT NULL,
    chiffre_affaire REAL    NOT NULL,
    PRIMARY KEY (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vente (
    id_vente   INTEGER  NOT NULL,
    date       DATETIME NOT NULL,
    quantite   INTEGER  NOT NULL,
    id_magasin INTEGER  NOT NULL,
    id_produit VARCHAR  NOT NULL,
    PRIMARY KEY (id_vente),
    FOREIGN KEY (id_magasin) REFERENCES magasin (id_magasin),
    FOREIGN KEY (id_produit) REFERENCES produit (id_produit)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vente_pdt (
    id      INTEGER NOT NULL,
    produit VARCHAR NOT NULL,
    ventes  INTEGER NOT NULL,
    PRIMARY KEY (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS vente_pdv (
    id      INTEGER NOT NULL,
    magasin VARCHAR NOT NULL,
    ventes  INTEGER NOT NULL,
    PRIMARY KEY (id)
    );
""")

# Commit et fermeture
conn.commit()
conn.close()

print("Tables créées avec succès.")
