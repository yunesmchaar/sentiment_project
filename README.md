#  Analyseur de Sentiments | Sentiment Analyzer

Application web permettant **d’analyser le sentiment de textes dans plus de 20 langues  **Flask**.

Ce projet a été réalisé dans le cadre de l’apprentissage du **Traitement Automatique du Langage Naturel (NLP)** et de l’**Intelligence Artificielle appliquée à l’analyse de texte**.

---

#  Structure du projet

```
sentiment_project/
├── app.py                 ← Backend (serveur Flask)
├── requirements.txt       ← Dépendances Python
├── Procfile               ← Configuration pour le déploiement (Render / Railway)
├── .env.example           ← Exemple de variables d’environnement
├── .gitignore             ← Fichiers ignorés par Git
├── README.md              ← Documentation du projet
└── templates/
    └── index.html         ← Interface utilisateur
```

---

#  Installation et exécution locale

## 1 Cloner le projet

```
git clone https://github.com/username/sentiment-analyzer.git
cd sentiment-analyzer
```

---

## 2 Créer un environnement virtuel

```
python -m venv venv
```

Activation :

Mac / Linux

```
source venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

---

## 3 Installer les dépendances

```
pip install -r requirements.txt

##  Lancer le serveur

```
python app.py
```

Puis ouvrir dans le navigateur :

```
http://localhost:5000
```

---

# ☁️ Déploiement sur Render (gratuit)

##  Publier sur GitHub

```
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/sentiment-analyzer.git
git push -u origin main
```

⚠️ Vérifiez que le fichier `.env` n’est pas publié sur GitHub.

---

##  Créer un compte Render

Accéder à :

https://render.com

Puis se connecter avec GitHub.

---

##  Créer un Web Service

Configuration :

| Paramètre     | Valeur                          |
| ------------- | ------------------------------- |
| Build Command | pip install -r requirements.txt |
| Start Command | gunicorn app:app                |
| Environment   | Python                          |

---

##  Ajouter les variables d’environnement

Dans **Environment Variables** :

```
ANTHROPIC_API_KEY = sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXXX
```

---

##  Déployer

Render générera une URL publique comme :

```
https://sentiment-analyzer.onrender.com
```

---

#  Sécurité de la clé API

| Bonne pratique            | À éviter                               |
| ------------------------- | -------------------------------------- |
| Utiliser `.env`           | Mettre la clé directement dans le code |
| Variables d’environnement | Stocker la clé dans HTML               |
| Backend sécurisé          | Publier la clé sur GitHub              |

---

#  Technologies utilisées

Backend

* Python
* Flask
* Anthropic SDK

Frontend

* HTML
* CSS
* JavaScript

Intelligence artificielle

* Claude AI (Modèle : claude-sonnet-4)

Déploiement

* Render
* Railway
* Heroku

Domaine

* Natural Language Processing (NLP)
* Analyse de sentiments multilingue

---

# API Endpoints

| Méthode | Route        | Description             |
| ------- | ------------ | ----------------------- |
| GET     | /            | Page principale         |
| POST    | /api/analyze | Analyse du sentiment    |
| GET     | /api/health  | Vérification du serveur |

---

## Exemple d’appel API

```
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Le produit est excellent!", "text_lang": "fr", "response_lang": "French"}'
```

---

 Développeur

Projet réalisé dans le cadre de l’apprentissage de :

* Data Science
* Natural Language Processing (NLP)
* Intelligence Artificielle

Développé par :

**Youness Mchaar**
Étudiant en Génie Informatique & Data Science

