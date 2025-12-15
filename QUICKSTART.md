# 🚀 GUIDE DE DÉMARRAGE RAPIDE

## Installation en 3 étapes

### 1️⃣ Prérequis
```bash
# Vérifier Docker
docker --version
docker-compose --version
```

### 2️⃣ Démarrer l'application
```bash
# Dans le dossier du projet
docker-compose up -d

# Attendre 10 secondes pour l'initialisation
```

### 3️⃣ Accéder à l'application
- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Prometheus**: http://localhost:9090

## 📊 Générer des données de test

```bash
# Installer les dépendances (optionnel pour les scripts)
pip install requests

# Générer des candidats et postes de test
python scripts/generate_sample_data.py
```

## 🧪 Tester l'API

### Créer un candidat
```bash
curl -X POST "http://localhost:8000/api/candidates/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jean Dupont",
    "email": "jean@example.com",
    "skills": ["Python", "Docker", "ML"],
    "experience_years": 5
  }'
```

### Créer un poste
```bash
curl -X POST "http://localhost:8000/api/jobs/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Data Engineer",
    "company": "TechCorp",
    "description": "Nous recherchons un Data Engineer...",
    "required_skills": ["Python", "Spark", "Docker"],
    "min_experience": 3
  }'
```

### Obtenir les statistiques
```bash
curl http://localhost:8000/api/analytics/dashboard
```

## 🎯 Utiliser le Matching ML

1. Créer des candidats et des postes (via l'interface ou l'API)
2. Aller dans l'onglet "Matching" sur http://localhost:3000
3. Entrer l'ID d'un poste
4. Cliquer sur "Trouver les Meilleurs Candidats"
5. Voir les scores de matching automatiques !

## 📈 Analytics Big Data

```bash
# Lancer l'analyse batch
cd analytics
python batch_analytics.py
```

## 🛠️ Développement

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Accéder à MongoDB
```bash
docker exec -it enligne_recruitement_app-mongodb-1 mongosh
use recruitment_db
db.candidates.find()
```

### Accéder à Redis
```bash
docker exec -it enligne_recruitement_app-redis-1 redis-cli
KEYS *
```

## 🐛 Dépannage

### Les containers ne démarrent pas
```bash
docker-compose down
docker-compose up -d --build
```

### Voir les logs
```bash
docker-compose logs backend
docker-compose logs mongodb
```

### Réinitialiser complètement
```bash
docker-compose down -v
docker-compose up -d
```

## ✨ Fonctionnalités Principales

✅ **Gestion Candidats** - CRUD complet, upload CV  
✅ **Gestion Postes** - Création, modification, statut  
✅ **Matching ML** - Score automatique TF-IDF + Cosine Similarity  
✅ **Analytics** - Dashboard temps réel, tendances, skills gap  
✅ **Big Data** - Traitement batch, rapports  
✅ **DevOps** - Docker, monitoring, CI/CD ready  
✅ **Distribué** - Redis cache, message queue  

## 📚 Endpoints Principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/candidates/` | POST | Créer candidat |
| `/api/jobs/` | POST | Créer poste |
| `/api/matching/recommend/{job_id}` | GET | Top candidats |
| `/api/analytics/dashboard` | GET | Statistiques |
| `/docs` | GET | Documentation API |

---

## 👥 Contribution

Sami-Malek -
[👥 Lien du projet : enligne_recruitement_app](https://github.com/SamiMalek10/enligne_recruitement_app)

**🎓 Projet Big Data, MLOps & Systèmes Distribués**
