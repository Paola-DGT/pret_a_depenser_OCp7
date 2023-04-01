
# OpenClassrooms Project 7
# Readme
## Pret à depenser: application de Machine Learning à l'analyse de risque pour effectuer des prets

L'objectif de ce projet est de rendre disponible une page web contenant un dashboard. Il sera
utilisé par un conseiller bancaire pour determiner si un client est un bon candidat pour
obtenir un pret. Le conseiller remplit un formulaire et recoit une reponse avec une estimation
du risque. Le dashboar montre aussi des graphs comparant le client aux autres clients ayant
reçu un credit.

## Decoupage des dossiers:
Ce projet est decoupé en dossiers de la facon suivante:
- **.github** - Contient tout le necesaire pour lancer des actions Github de CI/CD;
- **app** - Poséde tout le code de l'application, ce là se divise en 2 fichiers principaux:
  - *prediction_server.py* tout le code du serveur backend en FastAPI
  - *start_page.py* la page de demarrage du dashboard qui appelle elle toutes les pages
    dans **panels**.
- **data** - On trouve ici les fichiers cvs necesaires à l'entrainement du modele sur le
  backend et la manipulation des clients.
- **deployment** - Contient tous les fichiers necesaires au deployement automatique de
  l'application sur le cloud.
- **tests** - Ici on trouve les fichiers des tests unitaires de l'application.

## Deploiement:
- Instance equivalent à un EC2 de AWS;
- Nginx reverse proxy comme point d'entreé avec certificat LetsEncript;
- Services systemd crees pour chaque composant: backend, dashboard et nginx;
- Services backend et dashboard sur *localhost* avec redirection nginx pour le dashboard
- Deploiement du code par GitHub Actions (rsync);
- Lancement par GtiHub Actions d'un script Bash pour que l'instance mets à jour les services;

## Autres infos interesants:
- Utilisation de pre-commit pour la verification en amont du code,
- Integration de linters sur la pipeline CI avec pylint,
- Inspection de securité avec bandit aussi sur la CI.
