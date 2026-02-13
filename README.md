# Banking App Frontend

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.1.4-150458?style=flat&logo=pandas&logoColor=white)
![Reflex](https://img.shields.io/badge/Reflex-0.6.0%2B-black?style=flat&logo=reflex&logoColor=white)


Une application web moderne et performante pour l'analyse de données bancaires, construite avec [Reflex](https://reflex.dev). Ce frontend offre une interface intuitive pour visualiser les transactions, gérer les relations clients et détecter les fraudes potentielles grâce à des modèles prédictifs.

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

- **Tableau de Bord Synoptique** : Visualisation immédiate des indicateurs clés (KPIs) et des tendances.
- **Exploration des Transactions** : Recherche avancée, filtres dynamiques et export de données.
- **Intelligence Client** : Profils clients détaillés avec historique et analyse comportementale.
- **Détection de Fraude** : Algorithmes de Machine Learning pour identifier les transactions suspectes en temps réel.

---

## Interface & Pages

L'application est composée de 4 sections principales, accessibles via la barre latérale de navigation :

### 1. Dashboard (Tableau de Bord)
Le point d'entrée de l'application. Il affiche une vue d'ensemble de l'activité bancaire :
- **KPIs en temps réel** : Volume total des transactions, montant total échangé, nombre d'alertes fraude.
- **Graphiques** : Évolution temporelle des transactions et répartition par catégorie.

### 2. Transactions
Une interface puissante pour explorer l'historique des opérations :
- **Tableau de données interactif** : Tri, filtrage et pagination.
- **Filtres Avancés** : Par plage de dates, montant minimum/maximum, et catégorie de marchand.
- **Recherche** : Recherche textuelle instantanée.

### 3. Customers (Clients)
Gestion et analyse de la base client :
- **Liste des Clients** : Vue synthétique avec indicateurs de risque.
- **Profil Détaillé** : En cliquant sur un client, accédez à son historique complet, ses habitudes de dépenses et son score de risque.

### 4. Fraud Detection (Détection de Fraude)
Module spécialisé pour les analystes de sécurité :
- **Prédiction en Direct** : Formulaire permettant de tester des paramètres de transaction (montant, heure, lieu) pour obtenir un score de probabilité de fraude.
- **Analyse des Facteurs** : Visualisation des critères ayant le plus influencé la décision du modèle.

> *Note : Des captures d'écran de l'interface seront ajoutées prochainement.*

---

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Un accès au backend de l'API (local ou distant) accessible via ce projet https://github.com/lucaslgk/projet_python_2_mba

### Étapes d'installation

1. **Cloner le dépôt** (si applicable) ou télécharger les sources.

2. **Créer un environnement virtuel** (recommandé) :
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur macOS/Linux
   .venv\Scripts\activate     # Sur Windows
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

---

## Démarrage

### Option 1 : Script Automatique (Windows)
Pour un démarrage rapide, double-cliquez simplement sur le fichier `start.bat` situé à la racine du projet. Ce script se charge de lancer l'application avec les bonnes configurations.

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

Ce projet s'appuie sur une stack technique moderne et robuste :

- **[Reflex](https://reflex.dev)** : Framework web full-stack en Python pur.
- **[Pandas](https://pandas.pydata.org/)** : Manipulation et analyse de données performante.
- **[Httpx](https://www.python-httpx.org/)** : Client HTTP asynchrone pour la communication avec le backend.
- **[Plotly](https://plotly.com/python/)** (via Reflex) : Visualisations de données interactives.
