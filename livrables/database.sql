
CREATE TABLE magasin
(
  id_magasin INTEGER NOT NULL,
  ville      VARCHAR NOT NULL,
  salaries   INTEGER NOT NULL,
  PRIMARY KEY (id_magasin)
);

CREATE TABLE produit
(
  id_produit VARCHAR NOT NULL,
  nom        VARCHAR NOT NULL,
  prix       REAL    NOT NULL,
  stock      INTEGER NOT NULL,
  PRIMARY KEY (id_produit)
);

CREATE TABLE total_ca
(
  id              INTEGER NOT NULL,
  chiffre_affaire REAL    NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE vente
(
  id_vente   INTEGER  NOT NULL,
  date       DATETIME NOT NULL,
  quantite   INTEGER  NOT NULL,
  id_magasin INTEGER  NOT NULL,
  id_produit VARCHAR  NOT NULL,
  PRIMARY KEY (id_vente)
);

CREATE TABLE vente_pdt
(
  id      INTEGER NOT NULL,
  produit VARCHAR NOT NULL,
  ventes  INTEGER NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE vente_pdv
(
  id      INTEGER NOT NULL,
  magasin VARCHAR NOT NULL,
  ventes  INTEGER NOT NULL,
  PRIMARY KEY (id)
);

ALTER TABLE vente
  ADD CONSTRAINT FK_magasin_TO_vente
    FOREIGN KEY (id_magasin)
    REFERENCES magasin (id_magasin);

ALTER TABLE vente
  ADD CONSTRAINT FK_produit_TO_vente
    FOREIGN KEY (id_produit)
    REFERENCES produit (id_produit);
