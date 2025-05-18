# NLP Enriched News

## Description
This project runs an NLP pipeline on 300 news articles to enrich the data with information about named entities, covered topics, sentiment analysis, and detection of environmental scandals. The results are saved in a CSV file `results/enhanced_news.csv`.

## Generated Data Structure

Each processed article is recorded with the following information:

| Field               | Type          | Description |
|--------------------|--------------|-------------|
| `uuid`            | `int` or `str` | Unique identifier of the article |
| `url`             | `str` | URL of the article |
| `date_scraped`    | `date` | Date when the article was retrieved |
| `headline`        | `str` | Article title |
| `body`            | `str` | Article content |
| `organizations`   | `list[str]` | List of organizations mentioned in the article |
| `topics`          | `list[str]` | List of topics detected in the article |
| `sentiment`       | `float` | Sentiment score of the article (-1: negative, 0: neutral, 1: positive) |
| `scandal_distance`| `float` | Score indicating the probability of an environmental scandal |
| `top_10`          | `bool` | Indicates if the article is among the 10 most likely to be related to a scandal |

## Script Execution

To run the article extraction:

```bash
python scrapper.py
```

To run the article processing:

```bash
python nlp_enriched_news.py
```

The execution will display detailed information about each step of the pipeline:

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

## Explanation of Methodological Choices

### Embeddings Model
We use the **`fr_core_news_md`** model from SpaCy, a medium-sized model containing vector representations for French words. This model was chosen because:
- It offers a good balance between accuracy and performance.
- It provides pre-trained word embeddings useful for semantic similarity detection.
- It integrates efficient named entity recognition to extract cited organizations.

### Similarity Distance
We opted for **cosine similarity** to compare sentences with keywords related to environmental scandals. This choice is based on the following reasons:
- Cosine similarity is particularly effective for measuring semantic proximity between word or sentence vectors.
- It is independent of sentence length and is commonly used in NLP.
- It allows evaluation of how close a sentence in an article is to environmental scandal concepts.

### Scandal Detection
To identify articles related to environmental scandals, we:
1. Extract mentioned organizations.
2. Select sentences containing these organizations.
3. Compare their embeddings with those of keywords related to environmental scandals.
4. Calculate a score based on cosine similarity.
5. Rank the articles and select the 10 most relevant ones.

### Sentiment Analysis
We use **VADER (SentimentIntensityAnalyzer from NLTK)** to classify articles as `positive`, `neutral`, or `negative`. This choice is motivated by:
- Its effectiveness in analyzing the tone of short and informative texts.
- Its ability to handle nuances thanks to a `compound` score allowing for fine classification.

### Topic Detection
The topic detection model is loaded from `data/model/topic_classifier.pkl`. It contains a vectorizer and a classifier trained on French articles. The detected topics are then added to the metadata of each article.

## Final Result
The script generates an `enhanced_news.csv` file containing all enriched information for each article.

---

If you have any questions or suggestions, feel free to contribute! 🚀
