# Brief projet

Pour lancer le projet
``docker compose up --build``

Pour accèder aux tables de la base de donnée
``docker exec -it sqlite_container sqlite3 /data/database.db`` 
``.tables`` 
``SELECT * FROM [table_choisie];`` 
