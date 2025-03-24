# NLP Enriched News

## Description
Ce projet exécute un pipeline NLP sur 300 articles de presse pour enrichir les données avec des informations sur les entités nommées, les sujets abordés, l'analyse de sentiment et la détection de scandales environnementaux. Les résultats sont sauvegardés dans un fichier CSV `results/enhanced_news.csv`.

## Structure des données générées

Chaque article traité est enregistré avec les informations suivantes :

| Champ               | Type          | Description |
|--------------------|--------------|-------------|
| `uuid`            | `int` ou `str` | Identifiant unique de l'article |
| `url`             | `str` | URL de l'article |
| `date_scraped`    | `date` | Date de récupération de l'article |
| `headline`        | `str` | Titre de l'article |
| `body`            | `str` | Contenu de l'article |
| `organizations`   | `list[str]` | Liste des organisations mentionnées dans l'article |
| `topics`          | `list[str]` | Liste des sujets détectés dans l'article |
| `sentiment`       | `float` | Score de sentiment de l'article (-1 : négatif, 0 : neutre, 1 : positif) |
| `scandal_distance`| `float` | Score indiquant la probabilité d'un scandale environnemental |
| `top_10`          | `bool` | Indique si l'article fait partie des 10 plus susceptibles d'être liés à un scandale |

## Exécution des script

Pour exécuter l'extraction des articles :

```bash
python scrapper.py
```

Pour exécuter le traitement des articles :

```bash
python nlp_enriched_news.py
```

L'exécution affichera des informations détaillées sur chaque étape du pipeline :

```
Enriching <URL>:

Cleaning document ... (optional)

---------- Detect entities ----------
Detected <X> companies which are <company_1> and <company_2>

---------- Topic detection ----------
Text preprocessing ...
The topic of the article is: <topic>

---------- Sentiment analysis ----------
Text preprocessing ... (optional)
The article <title> has a <sentiment> sentiment

---------- Scandal detection ----------
Computing embeddings and distance ...
Environmental scandal detected for <entity>
```

## Explication des choix méthodologiques

### Modèle d'Embeddings
Nous utilisons le modèle **`fr_core_news_md`** de SpaCy, un modèle de taille intermédiaire contenant des représentations vectorielles pour les mots en français. Ce modèle a été choisi car :
- Il offre un bon équilibre entre précision et performance.
- Il fournit des embeddings de mots pré-entraînés utiles pour la détection de similarité sémantique.
- Il intègre une reconnaissance des entités nommées efficace pour extraire les organisations citées.

### Distance de Similarité
Nous avons opté pour **la similarité cosinus** pour comparer les phrases avec les mots-clés liés aux scandales environnementaux. Ce choix repose sur les raisons suivantes :
- La similarité cosinus est particulièrement efficace pour mesurer la proximité sémantique entre des vecteurs de mots ou de phrases.
- Elle est indépendante de la longueur des phrases et est couramment utilisée en NLP.
- Elle permet d'évaluer à quel point une phrase d'un article est proche des concepts de scandale environnemental.

### Détection de Scandale
Pour identifier les articles liés à des scandales environnementaux, nous :
1. Extrayons les organisations mentionnées.
2. Sélectionnons les phrases contenant ces organisations.
3. Comparons leurs embeddings avec ceux des mots-clés liés aux scandales environnementaux.
4. Calculons un score basé sur la similarité cosinus.
5. Classons les articles et sélectionnons les 10 les plus pertinents.

### Analyse de Sentiment
Nous utilisons **VADER (SentimentIntensityAnalyzer de NLTK)** pour classifier les articles en `positif`, `neutre` ou `négatif`. Ce choix est motivé par :
- Son efficacité pour analyser le ton des textes courts et informatifs.
- Sa capacité à gérer les nuances grâce à un score `compound` permettant une classification fine.

### Détection de Topics
Le modèle de détection de sujets est chargé depuis `data/model/topic_classifier.pkl`. Il contient un vectorizer et un classifier entraîné sur des articles en français. Les sujets détectés sont ensuite ajoutés aux métadonnées de chaque article.

## Résultat final
Le script génère un fichier `enhanced_news.csv` contenant toutes les informations enrichies pour chaque article.

---

Si vous avez des questions ou des suggestions, n'hésitez pas à contribuer ! 🚀

