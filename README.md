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


# Schema
<img width="1476" height="1820" alt="Blank diagram" src="https://github.com/user-attachments/assets/1efdf951-b800-4fbd-9ec5-fc7b736a1b0d" />
