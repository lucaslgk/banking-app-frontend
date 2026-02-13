# Banking App Frontend

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.1.4-150458?style=flat&logo=pandas&logoColor=white)
![Reflex](https://img.shields.io/badge/Reflex-0.6.0%2B-black?style=flat&logo=reflex&logoColor=white)


Une application web pour l'analyse de données bancaires, construite avec [Reflex](https://reflex.dev). Ce frontend offre une interface intuitive pour visualiser les transactions, gérer les relations clients et détecter les fraudes potentielles grâce à des modèles prédictifs.

**Ce projet est la partie frontend de l'API développée et partagée sur ce repo : https://github.com/lucaslgk/projet_python_2_mba**

---

## Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Interface & Pages](#interface--pages)
- [Installation](#installation)
- [Démarrage](#démarrage)
- [Structure du Projet](#structure-du-projet)
- [Technologies](#technologies)

---

## Fonctionnalités

- **Tableau de Bord** : Visualisation immédiate des indicateurs clés (KPIs) et des tendances.
- **Exploration des Transactions** : Recherche avancée, filtres dynamiques et export de données.
- **Intelligence Client** : Profils clients détaillés avec historique et analyse comportementale.
- **Détection de Fraude** : Identification des transactions suspectes en temps réel.

---

## Interface & Pages

L'application est composée de 4 sections principales, accessibles via la barre latérale de navigation :

### 1. Dashboard (Tableau de Bord)
Le point d'entrée de l'application. Il affiche une vue d'ensemble de l'activité bancaire :
- **KPIs en temps réel** : Volume total des transactions, montant total échangé, nombre d'alertes fraude.
- **Graphiques** : Évolution temporelle des transactions et répartition par catégorie.

<img width="1885" height="684" alt="image" src="https://github.com/user-attachments/assets/64675e37-5055-4947-8df8-893ee818ca2e" />
<img width="1888" height="933" alt="image" src="https://github.com/user-attachments/assets/5fa3b329-9ae1-4a2f-b52c-9a67beaa9b81" />


### 2. Transactions
Une interface puissante pour explorer l'historique des opérations :
- **Tableau de données interactif** : Tri, filtrage et pagination.
- **Filtres Avancés** : Par plage de dates, montant minimum/maximum, et catégorie de marchand.
- **Recherche** : Recherche textuelle instantanée.

<img width="1881" height="932" alt="image" src="https://github.com/user-attachments/assets/96aedcfb-001c-433a-8083-b9ba5802aab4" />


### 3. Customers (Clients)
Gestion et analyse de la base client :
- **Liste des Clients** : Vue synthétique avec indicateurs de risque.
- **Profil Détaillé** : En cliquant sur un client, accédez à son historique complet, ses habitudes de dépenses et son score de risque.

<img width="1880" height="934" alt="image" src="https://github.com/user-attachments/assets/47c1967c-0d2f-4823-97b4-e480c5294aff" />


### 4. Fraud Detection (Détection de Fraude)
Module spécialisé pour les analystes de sécurité :
- **Prédiction en Direct** : Formulaire permettant de tester des paramètres de transaction (montant, heure, lieu) pour obtenir un score de probabilité de fraude.
- **Analyse des Facteurs** : Visualisation des critères ayant le plus influencé la décision du modèle.

<img width="1877" height="689" alt="image" src="https://github.com/user-attachments/assets/7478a398-ef58-4521-af22-d078076e9d2e" />
<img width="1874" height="515" alt="image" src="https://github.com/user-attachments/assets/ea8a242c-9831-4bcc-94d1-4e14ecf75862" />
<img width="1874" height="819" alt="image" src="https://github.com/user-attachments/assets/835a489c-0598-4943-85ce-e12a39fef913" />


---

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Un accès au backend de l'API (local ou distant) accessible via ce projet https://github.com/lucaslgk/projet_python_2_mba

### Étapes d'installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/lucaslgk/banking-app-frontend
   ```

2. **Créer un environnement virtuel** (recommandé) :
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

---

## Démarrage

### Option 1 : Script Automatique
Pour un démarrage rapide, double-cliquez simplement sur le fichier `start.bat` situé à la racine du projet. Ce script se charge de lancer l'application avec les bonnes configurations, en vérifiant en amont que l'API a bien été lancée.

### Option 2 : Lancement Manuel
1. Assurez-vous que votre API Backend est lancée et accessible (par défaut sur `http://localhost:8000`).
2. Lancez le serveur de développement Reflex :
   ```bash
   reflex run
   ```
3. L'application sera accessible dans votre navigateur à l'adresse : [http://localhost:3000](http://localhost:3000)

---

## Structure du Projet

```
banking-app-frontend/
├── banking_app/            # Code source principal
│   ├── components/         # Composants UI réutilisables (Layout, Cards...)
│   ├── pages/              # Définition des pages (Dashboard, Transactions...)
│   ├── services/           # Connecteurs API et logique métier
│   ├── state/              # Gestion de l'état (State Management)
│   └── banking_app.py      # Point d'entrée de l'application Reflex
├── assets/                 # Images et ressources statiques
├── requirements.txt        # Dépendances Python
├── rxconfig.py             # Configuration du projet Reflex
└── start.bat               # Script de démarrage rapide
```

---

## Technologies

Ce projet s'appuie sur les technologies suivantes :

- **[Reflex](https://reflex.dev)** : Framework web full-stack en Python pur.
- **[Pandas](https://pandas.pydata.org/)** : Manipulation et analyse de données performante.
- **[Httpx](https://www.python-httpx.org/)** : Client HTTP asynchrone pour la communication avec le backend.
- **[Plotly](https://plotly.com/python/)** (via Reflex) : Visualisations de données interactives.
