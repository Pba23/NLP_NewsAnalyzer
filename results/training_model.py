import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import learning_curve
import joblib

# Load the training and test datasets
train_data = pd.read_csv("data/db/bbc/bbc_news_train.csv")  # Replace with the correct path
test_data = pd.read_csv("data/db/bbc/bbc_news_tests.csv")    # Replace with the correct path

# Ensure the datasets have the required columns
assert "Text" in train_data.columns and "Category" in train_data.columns, "train.csv must contain 'Text' and 'Category' columns"
assert "Text" in test_data.columns and "Category" in test_data.columns, "test.csv must contain 'Text' and 'Category' columns"

# Separate features and labels
X_train = train_data["Text"]
y_train = train_data["Category"]
X_test = test_data["Text"]
y_test = test_data["Category"]

# Vectorize the Text data
vectorizer = TfidfVectorizer(stop_words="english", max_features=10000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train a Logistic Regression classifier
clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_train_vec, y_train)

# Evaluate the model
y_pred = clf.predict(X_test_vec)
test_accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Ensure test accuracy is > 95%
if test_accuracy < 0.95:
    raise ValueError("Model did not achieve the required accuracy of > 95%.")

# Save the trained model
joblib.dump((vectorizer, clf), "data/model/topic_classifier.pkl")
print("Model saved as topic_classifier.pkl")
# Plot learning curves
train_sizes, train_scores, test_scores = learning_curve(
    clf, X_train_vec, y_train, cv=5, scoring="accuracy", n_jobs=-1, train_sizes=[0.1, 0.2, 0.5, 0.8, 1.0]
)

# Calculate mean and standard deviation for learning curves
train_scores_mean = train_scores.mean(axis=1)
test_scores_mean = test_scores.mean(axis=1)

plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_scores_mean, "o-", color="r", label="Training Score")
plt.plot(train_sizes, test_scores_mean, "o-", color="g", label="Cross-Validation Score")
plt.title("Learning Curves")
plt.xlabel("Training Set Size")
plt.ylabel("Accuracy")
plt.legend(loc="best")
plt.grid()
plt.savefig("data/img/learning_curves.png")
print("Learning curves saved as learning_curves.png")
plt.show()