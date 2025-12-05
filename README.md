# TP-USCB15
Ce projet a pour objectif de développer une application mobile communiquant avec une API.
L’API est construite sous forme de microservices, chacun disposant de sa propre base de données.

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

- `GET /login/<jwt>` Récupère les informations d'un utilisateur pour se login
- `GET /signup` Crée un utilisateur et lui attribue un JWT

</details>

## Composants de l’application

| Composant | Description |
| :---         |     :---      |
| Application Mobile   | Réalise la collecte de données et renvois les datas vers l'API     | 
| API gateway     | Point d'entrée unique pour interaction avec api/bdd.Ce service servira à authentifier l’utilisateur      |
| Service API   | Reçoit et renvoie les requêtes des utilisateur auth et interagis avec la BDD de questions réponses     | 
| Application Mobile   | Réalise la collecte de données et renvois les datas vers l'API     | 
| Service Agent log     |  stock chiffre et gère la politique de rétention des logs       |
| KMS    | Stock et gere les clef de chiffrement utilisé pour securiser les datas      |


# Schema

<img width="1476" height="1800" alt="Blank diagram(2)" src="https://github.com/user-attachments/assets/282976ce-e8da-40b3-9351-f4f3b610739f" />

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
