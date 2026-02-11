# Banking App Frontend

Interface frontend moderne pour l'API de transactions bancaires, construite avec [Reflex](https://reflex.dev).

## Fonctionnalités

- 📊 **Dashboard** : Vue d'ensemble des statistiques et de l'état du système
- 💳 **Transactions** : Historique complet avec filtres avancés et recherche
- 👥 **Clients** : Top clients et profils détaillés
- 🛡️ **Fraude** : Analyse et détection prédictive de fraude

## Installation

1. Assurez-vous d'avoir Python 3.8+ installé
2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Démarrage

### Option 1 : Script automatique (Recommandé)

Double-cliquez simplement sur `start.bat` à la racine du projet.

### Option 2 : Manuel

1. **Terminal 1 (Backend)** : Assurez-vous que l'API backend tourne sur `http://localhost:8000`
2. **Terminal 2 (Frontend)** : Lancez le frontend :

```bash
reflex run
```

L'application sera accessible sur `http://localhost:3000`.

## Structure du Projet

- `banking_app/` : Code source de l'application
  - `pages/` : Pages de l'interface (Dashboard, Transactions, etc.)
  - `components/` : Composants réutilisables (Layout, Cards, etc.)
  - `services/` : Client API et intégration
  - `state/` : Gestion de l'état de l'application
- `assets/` : Images et ressources statiques
