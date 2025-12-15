# Application de Recrutement en Ligne - Big Data & MLOps

🎥 **Vidéo de démonstration**  
👉 [Voir la démo de l’application](https://drive.google.com/file/d/1ZiWBTrrV6ZNNH1AGdgvTz7ez70Qo8rWj/view)

---
## 🎯 Objectif du Projet
Application intelligente de recrutement utilisant le Machine Learning pour matcher automatiquement les candidats avec les postes, analyser les CV et fournir des insights via Big Data Analytics.

## 🏗️ Architecture

### Technologies Utilisées
- **Backend**: FastAPI (Python) - API REST haute performance
- **ML/Analytics**: Scikit-learn, Pandas, NLTK - Matching intelligent
- **Base de données**: MongoDB - NoSQL pour flexibilité
- **Cache**: Redis - Performance et système distribué
- **Message Queue**: Redis Streams - Traitement asynchrone
- **DevOps**: Docker, Docker Compose
- **Monitoring**: Prometheus metrics
- **CI/CD**: GitHub Actions ready

## 📦 Structure du Projet

```
enligne_recruitement_app/
├── backend/
│   ├── app/
│   │   ├── api/          # Endpoints REST
│   │   ├── models/       # Modèles de données
│   │   ├── ml/           # Modèles ML et analytics
│   │   ├── services/     # Logique métier
│   │   └── utils/        # Utilitaires
│   ├── tests/            # Tests unitaires
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # Interface web
├── analytics/            # Scripts d'analyse Big Data
├── mlops/               # Pipeline ML et monitoring
├── docker-compose.yml
└── .github/workflows/   # CI/CD
```

## 🚀 Fonctionnalités

### 1. Gestion des Candidats
- Upload et parsing de CV (PDF, DOCX, TXT)
- Extraction automatique des compétences
- Profil candidat enrichi

### 2. Gestion des Postes
- Création de postes avec critères requis
- Compétences techniques et soft skills
- Niveau d'expérience

### 3. Matching Intelligent (ML)
- Scoring automatique candidat-poste (TF-IDF + Cosine Similarity)
- Recommandations personnalisées
- Analyse de compatibilité

### 4. Analytics & Big Data
- Dashboard statistiques temps réel
- Analyse des tendances de recrutement
- Insights sur les compétences demandées
- Rapports de performance

### 5. Système Distribué
- Architecture microservices
- Cache distribué (Redis)
- Message queue pour traitement asynchrone
- Scalabilité horizontale

## 🛠️ Installation et Démarrage

### Prérequis
- Docker & Docker Compose
- Python 3.9+
- Git

### Démarrage Rapide

```bash
# Cloner le projet
cd enligne_recruitement_app

# Lancer avec Docker Compose
docker-compose up -d

# L'API sera disponible sur http://localhost:8000
# Documentation API: http://localhost:8000/docs
# Frontend: http://localhost:3000
```

### Développement Local

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
python -m http.server 3000
```

## 📊 API Endpoints

### Candidats
- `POST /api/candidates` - Créer un candidat
- `GET /api/candidates/{id}` - Récupérer un candidat
- `POST /api/candidates/upload-cv` - Upload CV
- `GET /api/candidates/search` - Rechercher candidats

### Postes
- `POST /api/jobs` - Créer un poste
- `GET /api/jobs` - Liste des postes
- `GET /api/jobs/{id}` - Détails d'un poste

### Matching
- `POST /api/matching/score` - Calculer score candidat-poste
- `GET /api/matching/recommend/{job_id}` - Top candidats pour un poste
- `GET /api/matching/jobs-for-candidate/{candidate_id}` - Postes pour candidat

### Analytics
- `GET /api/analytics/dashboard` - Statistiques globales
- `GET /api/analytics/skills-trends` - Tendances compétences
- `GET /api/analytics/hiring-metrics` - Métriques de recrutement

## 🤖 MLOps Pipeline

### 1. Entraînement du Modèle
```bash
python mlops/train_model.py
```

### 2. Évaluation
```bash
python mlops/evaluate_model.py
```

### 3. Déploiement
- Versionnage des modèles
- A/B testing
- Monitoring des prédictions

## 📈 Monitoring

### Métriques Collectées
- Temps de réponse API
- Nombre de requêtes
- Scores de matching
- Taux de conversion
- Performance ML

### Accès Prometheus
```
http://localhost:9090
```

## 🧪 Tests

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Load testing
locust -f tests/load_test.py
```

## 🔐 Sécurité

- Validation des inputs (Pydantic)
- Rate limiting
- JWT Authentication (optionnel)
- Sanitization des uploads

## 📝 Exemples d'Utilisation

### 1. Créer un Candidat et Upload CV

```python
import requests

# Créer candidat
response = requests.post("http://localhost:8000/api/candidates", json={
    "name": "Jean Dupont",
    "email": "jean@example.com",
    "skills": ["Python", "Docker", "ML"],
    "experience_years": 5
})

# Upload CV
files = {'file': open('cv.pdf', 'rb')}
response = requests.post(
    "http://localhost:8000/api/candidates/upload-cv",
    files=files,
    data={'candidate_id': 'xxx'}
)
```

### 2. Créer un Poste

```python
response = requests.post("http://localhost:8000/api/jobs", json={
    "title": "Data Engineer",
    "description": "Nous recherchons un Data Engineer expérimenté...",
    "required_skills": ["Python", "Spark", "Kafka", "Docker"],
    "nice_to_have_skills": ["Airflow", "ML"],
    "min_experience": 3
})
```

### 3. Obtenir les Meilleurs Candidats

```python
response = requests.get(
    f"http://localhost:8000/api/matching/recommend/{job_id}",
    params={"top_n": 10}
)
matches = response.json()
```

## 🎓 Concepts Big Data & Distribués

### 1. Traitement Distribué
- Redis pour cache distribué
- Message queue pour traitement asynchrone
- Prêt pour Kafka/Spark si besoin de scale

### 2. Analytics à Grande Échelle
- Agrégations optimisées MongoDB
- Streaming analytics avec Redis Streams
- Batch processing pour rapports

### 3. MLOps
- Pipeline ML automatisé
- Versionnage des modèles
- Monitoring de drift
- Continuous training

## 🚀 Évolutions Futures

- [ ] Intégration Apache Spark pour Big Data
- [ ] Apache Kafka pour event streaming
- [ ] Elasticsearch pour recherche avancée
- [ ] Deep Learning pour analyse CV (BERT)
- [ ] Kubernetes pour orchestration
- [ ] GraphQL API
- [ ] WebSockets pour notifications temps réel

## 📄 Licence

MIT License

---

## 🎥 Démo Vidéo
👉 **Accéder à la vidéo de démonstration complète** :  
https://drive.google.com/file/d/1ZiWBTrrV6ZNNH1AGdgvTz7ez70Qo8rWj/view

---

## 👥 Contribution

**Sami Malek**  
📧 [sami.malek15@gmail.com](mailto:sami.malek15@gmail.com)

[👥 Lien du projet : enligne_recruitement_app](https://github.com/SamiMalek10/enligne_recruitement_app)

Contributions bienvenues ! Créez une issue ou un PR.

---

**Auteur**: Projet Big Data & MLOps - Application de Recrutement
**Date**: Décembre 2025
