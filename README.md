# TP-USCB15
Ce projet a pour objectif de développer une application mobile communiquant avec une API.
L’API est construite sous forme de microservices, chacun disposant de sa/ses propre(s) base(s) de données.

L’accès à l’application et aux fonctionnalités de l’API est protégé par une authentification via JWT, afin de garantir l’identité de l’utilisateur.

Enfin, chaque action effectuée est enregistrée par un agent de logs, qui se charge de chiffrer et de gérer la journalisation pour renforcer la sécurité du système.
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
  
- `GET /question` Affiche toutes les questions
- `POST /question` Crée une question
- `GET /question/<id>` Affiche une question en fonction de son ID
- `POST /answer/<id>` Poste les réponses en fonction de la question
- `POST /photo/<id>` Poste la photo liée à la réponse
</details>

<details>
<summary>Routes des identité</summary>

- `POST /auth` Poste les identifiants rentrés dans l'application mobile. Un retour de JWT est attendu si les identifiants sont valides.

</details>

## Composants de l’application

| Composant | Description |
| :---         |     :---      |
| Application Mobile   | Réalie les appels API pour l'envoi de données (réponses, photos, ...)     | 
| API gateway     | Point d'entrée unique pour les interactions vers l'API et les BDD. Ce service servira également authentifier l’utilisateur et gèrera le TLS     |
| Service API   | Reçoit, traite et renvoie les requêtes des utilisateur authentifiés et interagis avec les bases de données    | 
| Bases de données   | Différentes bases de données sont présentes sur le système. Elles stockent chacune des informations différentes.     | 
| Service Agent log     |  Réceptionne et gère les logs du système entier.       |
| Gestionnaire d'identité    | Génère, stoque et gère les clés et les tokens utilisés par le système entier.      |


# Diagrammes
<details>
  <summary>Diagramme de déploiement</summary>
  Ce diagramme n'est pas au format UML (mais a le même objectif)
  
  <img width="1476" height="1800" alt="Blank diagram(3)" src="https://github.com/user-attachments/assets/3edbde12-41c6-4d69-b5e9-9a45117d8087" />
</details>

<details>
  <summary>Diagramme de séquence</summary>

  <img width="2552" height="2580" alt="Sequence diagram(1)" src="https://github.com/user-attachments/assets/50ff95d8-e573-4ca8-9c98-ff3cc408eae4" />
</details>

<details>
  <summary>Structure de bases de données (Diagramme de classes ?)</summary>

  <img width="1040" height="829" alt="image" src="https://github.com/user-attachments/assets/36a84abd-51f2-4c71-8e9b-fa6a8881f03f" />
</details>



# Installation
## Prérequis
### Docker
#### Ajout du repo Docker:
```
  # Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```
#### Installation des compoosants nécéssaires
```
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
#### Test de bon fonctionnement
```
sudo docker run hello-world
```
