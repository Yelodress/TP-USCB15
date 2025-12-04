# TP-USCB15
Ce projet vise à...
## Technologies utilisées
<details>
<summary>Côté serveur</summary>

- Langage de programmation:`Python`
- Principes de fonctionnement:`REST`
- Gestion du serveur WEB:`FLASK`
- Gestion des bases de données:`MySQL`
- Conteneurisation:`Docker`
</details>
<details>
<summary>Côté client</summary>

- Framework:`Flutter`
- Chiffrement des données:`AES-CGM 256`
- Chiffrement homomorphe:`?`
</details>

## Liste des routes disponibles
<details>
<summary>Routes des questions/réponses</summary>

- `GET /question/<id>` Affiche une question en fonction de son ID
- `POST /answer/<id>` Poste la réponse en fonction de la question
- `POST /photo/<id>` Poste la photo liée à la réponse
</details>

<details>
<summary>Routes des identité</summary>

- `GET /login/<jwt>` Récupère les informations d'un utilisateur pour se login
- `GET /signup` Crée un utilisateur et lui attribue un JWT

</details>

## Composants de l’application

| Composant | Description |
| :---         |     :---      |
| Application Mobile   | Réalise la collecte de données et renvois les datas vers l'API     | 
| API gateway     | Point d'entrée unique pour interaction avec api/bdd.Ce service servira à authentifier l’utilisateur      |
| Service API   | Reçoit et renvoie les requêtes des utilisateur auth et interagis avec la BDD de questions réponses     | 
| API gateway     | git diff       |
| Application Mobile   | Réalise la collecte de données et renvois les datas vers l'API     | 
| Service Agent log     |  stock chiffre et gère la politique de rétention des logs       |


# Schema
<img width="1476" height="1800" alt="Blank diagram(1)" src="https://github.com/user-attachments/assets/44026ac0-0763-47a5-a9ae-841b925ff2a0" />
