## app.py
* Le fichier app.py est un programme Python qui utilise le framework Flask pour créer une API web. 
L'API permet à un utilisateur de récupérer et de mettre à jour une liste de 18 valeurs appelée moyenne.

* Lorsqu'un utilisateur envoie une requête GET à la route "/moyenne", l'API renvoie la liste moyenne sous forme de JSON.

* Lorsqu'un utilisateur envoie une requête POST à la route "/moyenne" avec une liste de 18 valeurs, 
l'API met à jour la liste moyenne avec les nouvelles valeurs et renvoie la liste mise à jour sous forme de JSON.

* Le module flask_cors est également utilisé pour permettre l'accès à l'API depuis n'importe quel site web,
en contournant les restrictions de sécurité normalement en place pour les requêtes effectuées à partir de sites tiers.
