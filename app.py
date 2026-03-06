"""
API d'Analyse de Sentiment - Serveur Backend Flask
Utilise Hugging Face Transformers (100% gratuit, fonctionne hors ligne)
- Modèle anglais  : distilbert-base-uncased-finetuned-sst-2-english
- Modèle multilingue : tabularisai/multilingual-sentiment-analysis
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import pipeline
import os

# Initialisation de l'application Flask
app = Flask(__name__)

# Autoriser les requêtes cross-origin (depuis le frontend)
CORS(app)

# ─────────────────────────────────────────
# Chargement des modèles Hugging Face
# Les modèles sont téléchargés automatiquement au premier lancement
# puis mis en cache sur le disque pour les prochaines fois
# ─────────────────────────────────────────
print("⏳ Chargement des modèles... (première fois = quelques minutes)")

# Modèle 1 : Anglais uniquement - rapide et précis
model_en = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# Modèle 2 : Multilingue - supporte arabe, français, anglais, espagnol...
model_multi = pipeline(
    "sentiment-analysis",
    model="tabularisai/multilingual-sentiment-analysis"
)

print("✅ Modèles chargés avec succès !")


# ─────────────────────────────────────────
# Fonction utilitaire : normaliser le résultat Hugging Face
# Les modèles retournent des labels différents, on les unifie ici
# ─────────────────────────────────────────
def normalize_result(hf_result, text_lang):
    """
    Convertit le résultat brut de Hugging Face en format unifié pour le frontend.
    hf_result : liste retournée par le pipeline, ex: [{'label': 'POSITIVE', 'score': 0.99}]
    text_lang : langue du texte pour choisir les labels d'affichage
    """

    label_raw = hf_result[0]["label"].upper()
    score     = round(hf_result[0]["score"] * 100)

    # Mapping des labels vers notre format unifié
    if any(p in label_raw for p in ["POSITIVE", "POS", "5 STARS", "4 STARS"]):
        sentiment = "positive"
        emoji     = "😊"
        pos_score = score
        neg_score = 100 - score
        neu_score = 0
    elif any(p in label_raw for p in ["NEGATIVE", "NEG", "1 STAR", "2 STARS"]):
        sentiment = "negative"
        emoji     = "😠"
        pos_score = 100 - score
        neg_score = score
        neu_score = 0
    else:
        sentiment = "neutral"
        emoji     = "😐"
        pos_score = 30
        neg_score = 30
        neu_score = score

    # Labels multilingues selon la langue de l'interface
    labels = {
        "ar": {"positive": "إيجابي", "negative": "سلبي", "neutral": "محايد", "mixed": "مختلط"},
        "fr": {"positive": "Positif", "negative": "Négatif", "neutral": "Neutre", "mixed": "Mixte"},
        "en": {"positive": "Positive", "negative": "Negative", "neutral": "Neutral", "mixed": "Mixed"},
        "es": {"positive": "Positivo", "negative": "Negativo", "neutral": "Neutral", "mixed": "Mixto"},
        "de": {"positive": "Positiv",  "negative": "Negativ",  "neutral": "Neutral", "mixed": "Gemischt"},
    }

    # Langue d'affichage (par défaut français)
    ui_lang  = text_lang if text_lang in labels else "fr"
    lang_map = labels[ui_lang]

    return {
        "sentiment"     : sentiment,
        "emoji"         : emoji,
        "label"         : lang_map[sentiment],
        "sub"           : f"Score de confiance : {score}%",
        "scores"        : {
            "positive"  : pos_score,
            "negative"  : neg_score,
            "neutral"   : neu_score
        },
        "analysis"      : f"Le modèle a détecté un sentiment {lang_map[sentiment].lower()} "
                          f"avec un score de confiance de {score}%. "
                          f"Ce résultat est basé sur l'analyse locale via Hugging Face Transformers.",
        "keywords"      : [],   # Hugging Face ne retourne pas de mots-clés
        "business"      : f"Un sentiment {lang_map[sentiment].lower()} peut être utilisé "
                          f"pour prioriser les retours clients et adapter la stratégie commerciale.",
        "detected_lang" : text_lang if text_lang != "auto" else "Détection automatique"
    }


# ─────────────────────────────────────────
# Route principale : affiche la page HTML
# ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ─────────────────────────────────────────
# Route API : analyse du sentiment
# Méthode : POST
# Corps attendu : { "text": "...", "text_lang": "...", "model": "en"|"multi" }
# ─────────────────────────────────────────
@app.route("/api/analyze", methods=["POST"])
def analyze():
    # Récupération des données JSON envoyées par le frontend
    data = request.get_json()

    # Vérification que le texte est bien présent
    if not data or "text" not in data:
        return jsonify({"error": "Aucun texte fourni"}), 400

    # Extraction des paramètres
    text       = data.get("text", "").strip()
    text_lang  = data.get("text_lang", "auto")
    model_type = data.get("model", "multi")  # "en" ou "multi"

    # Vérification que le texte n'est pas vide
    if not text:
        return jsonify({"error": "Le texte est vide"}), 400

    # Limitation de la taille du texte (les modèles ont une limite de tokens)
    if len(text) > 512:
        text = text[:512]  # On tronque silencieusement

    try:
        # Choix du modèle selon le paramètre reçu
        if model_type == "en":
            # Modèle anglais : rapide, très précis pour l'anglais
            hf_result = model_en(text)
        else:
            # Modèle multilingue : supporte arabe, français, espagnol, etc.
            hf_result = model_multi(text)

        # Normalisation et formatage du résultat
        result = normalize_result(hf_result, text_lang)

        # Ajout du modèle utilisé dans la réponse (utile pour le debug)
        result["model_used"] = "English (DistilBERT)" if model_type == "en" else "Multilingue"

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─────────────────────────────────────────
# Route API : vérification de l'état du serveur
# ─────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status"  : "ok",
        "models"  : {
            "english"     : "distilbert-base-uncased-finetuned-sst-2-english",
            "multilingual": "tabularisai/multilingual-sentiment-analysis"
        }
    })


# ─────────────────────────────────────────
# Point d'entrée : démarrage du serveur
# ─────────────────────────────────────────
if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"🚀 Serveur démarré sur http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
