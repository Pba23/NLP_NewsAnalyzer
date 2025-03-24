import joblib
import spacy
import json
import nltk
import numpy as np
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.metrics.pairwise import cosine_similarity

# Charger le modèle SpaCy français avec les embeddings
nlp = spacy.load("fr_core_news_md")

# Initialiser l'analyseur de sentiment VADER
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()

# Charger le modèle de détection de topics
vectorizer, classifier = joblib.load("data/model/topic_classifier.pkl")

# Définition des mots-clés des scandales environnementaux
SCANDAL_KEYWORDS = ["pollution", "déforestation", "marée noire", "déchet toxique", "émission de CO2"]

# Calcul des embeddings des mots-clés
keyword_embeddings = np.array([nlp(word).vector for word in SCANDAL_KEYWORDS])

# Fonction pour détecter les organisations dans un texte
def detect_organizations(text):
    doc = nlp(text)
    return list(set(ent.text for ent in doc.ents if ent.label_ == "ORG"))

# Fonction pour détecter un scandale environnemental
def detect_scandal(text, organizations):
    sentences = [sent.text for sent in nlp(text).sents if sent]
    
    # Récupérer les phrases contenant une organisation
    relevant_sentences = [s for s in sentences if any(org in s for org in organizations)]

    if not relevant_sentences:
        return 0  # Aucun scandale détecté

    print("\n---------- Scandal detection ----------")
    print("Computing embeddings and distance ...")

    # Calcul des embeddings des phrases pertinentes
    sentence_embeddings = np.array([nlp(sent).vector for sent in relevant_sentences])

    # Calculer la similarité entre chaque phrase et les mots-clés
    similarities = cosine_similarity(sentence_embeddings, keyword_embeddings)
    
    # Score basé sur la similarité moyenne
    scandal_score = np.mean(similarities)
    
    return scandal_score

# Fonction pour détecter les topics
def detect_topic(text):
    print("\n---------- Topic detection ----------")
    print("Text preprocessing ...")

    text_vectorized = vectorizer.transform([text])
    topic = classifier.predict(text_vectorized)[0]

    print(f"The topic of the article is: {topic}")
    return topic

# Processus des articles
def process_news_articles(input_file, output_csv):
    with open(input_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    results = []
    
    for i, article in enumerate(articles):
        url = article.get("url", "")
        date_scraped = article.get("date", "")
        title = article.get("title", "")
        body = article.get("content", "")

        print(f"\nEnriching {url}:\n")
        print("Cleaning document ... (optional)")

        # Détection des organisations
        print("\n---------- Detect entities ----------")
        orgs_in_body = detect_organizations(body)
        orgs_in_headline = detect_organizations(title)
        organizations = list(set(orgs_in_body + orgs_in_headline))
        print(f"Detected {len(organizations)} companies which are {', '.join(organizations) if organizations else 'None'}")

        # Détection du topic
        topic = detect_topic(body)

        # Analyse de sentiment
        print("\n---------- Sentiment analysis ----------")
        print("Text preprocessing ... (optional)")
        sentiment_scores = sia.polarity_scores(body)
        sentiment_score = sentiment_scores["compound"]
        sentiment = "positive" if sentiment_score > 0.05 else "negative" if sentiment_score < -0.05 else "neutral"
        print(f"The article '{title}' has a {sentiment} sentiment.")

        # Détection de scandale
        scandal_score = float(detect_scandal(body, organizations))

        # Stocker les résultats
        results.append({
            "uuid": i + 1,
            "url": url,
            "date_scraped": date_scraped,
            "headline": title,
            "body": body,
            "org": organizations,
            "topics": topic,
            "sentiment": sentiment_score,
            "scandal_distance": scandal_score,
            "top_10": False  # Ajouté plus tard après tri
        })

    # Trier les articles selon leur score de scandale et garder les 10 plus élevés
    results = sorted(results, key=lambda x: x["scandal_distance"], reverse=True)
    for r in results[:10]:
        r["top_10"] = True

    # Sauvegarde dans un CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False, encoding="utf-8")

    print(f"\nProcessing complete! Results saved in '{output_csv}'.")

# Exécution
if __name__ == "__main__":
    input_file = "data/db/senego/senego_articles.json"
    output_csv = "data/db/results/enhanced_news.csv"
    
    print("Processing articles...")
    process_news_articles(input_file, output_csv)
