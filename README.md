# TP-USCB15
Ce projet a pour objectif de développer une application mobile communiquant avec une API.
L’API est construite sous forme de microservices, chacun disposant de sa/ses propre(s) base(s) de données.

L’accès à l’application et aux fonctionnalités de l’API est protégé par une authentification via JWT, afin de garantir l’identité de l’utilisateur.
Tous les appels à l’API sont gérés par une API Gateway, qui se charge de router les requêtes vers les différents microservices.
Cette passerelle applique également des règles de sécurité et de contrôle d’accès, configurables à l’aide de décorateurs tels que @requireJwt ou @requireAdmin.
Ces mécanismes permettent de définir si une route est accessible publiquement ou soumise à une gestion des droits basée sur les rôles (RBAC).

De plus, grâce à l’utilisation de SQLAlchemy, toutes les valeurs fournies à la base de données sont systématiquement sérialisées et nettoyées, ce qui permet de prévenir efficacement les attaques par injection SQL.

Le l'upload de fichiers est également sécurisé par plusieurs mécanismes : une vérification stricte des extensions autorisées, le nettoyage du nom des fichiers, ainsi que l’attribution d’un identifiant unique à chaque image. Cette approche permet d’éviter les conflits de noms et empêche, par exemple, qu’un utilisateur puisse écraser ou supprimer le fichier d’un autre utilisateur.

Par ailleurs, l’ensemble des données entrantes est soumis à une validation systématique afin de garantir leur conformité et leur intégrité avant traitement.

Le service intègre également une logique de rate limiting, visant à limiter le nombre de requêtes par utilisateur et à se protéger contre les attaques de type brute force.

Concernant la gestion des mots de passe, ceux-ci ne sont jamais stockés en clair. Ils sont protégés par un mécanisme de hachage sécurisé, utilisé lors de la vérification de l’authentification.

De plus, les réponses de l’API sont volontairement peu explicites, afin de limiter les risques d’énumération d’utilisateurs via des messages d’erreur trop détaillés.

Les JWT ont une durée de validité limitée à 15 minutes. Afin de permettre une authentification fluide sans avoir à ressaisir le mot de passe, un refresh token est également mis en place.

Enfin, en cas de déconnexion via la route logout, le serveur procède


Enfin, chaque action effectuée est enregistrée par un agent de logs, qui se charge de gérer la journalisation pour renforcer la réslience du système.

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
- `GET /answer/<id>` Récupère les réponses à une question
- `GET /answer` Récupère toutes les réponses et l'ID des questions concernées
</details>

<details>
<summary>Routes des identité</summary>

- `POST /auth` Poste les identifiants rentrés dans l'application mobile. Un retour de JWT est attendu si les identifiants sont valides.

</details>

## Composants de l’application

| Composant | Description |
| :---         |     :---      |
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



# Installation 🚧 (en cours de rédaction)
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

#### Téléchargement de la branche principale (stable)
```
git clone https://github.com/Yelodress/TP-USCB15
```

#### Lancement du conteneur
```
docker compose up --build
```

#### Après arrêt du docker, vous pouvez effacer les informations laissées en mémoire avec
```
docker compose down -v
```
#### TODO
- Faire en sorte que l'application sub une réponse (la route réponses est fonctionnelle manque juste le / à protéger)
- Permettre à l'admin de créer des utilisateurs auxquels on ajoute les token normalement c'est gérer de façon auto pour les token
- Peut être une interface web pour avoir une visu des réponse
- Sécuriser les routes seulement visible par rôle admin exemple answer qui ne doit pas être visible par les user
- Limiter les appels API uniquement par la gateway (proxi ?). Pour se faire, potentiellement foutre un certificat ou cloisonner les réseaux du Docker. Objectif: empecher de bypass la gateway
