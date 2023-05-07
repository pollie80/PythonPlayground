import nltk
from nltk.corpus import movie_reviews
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def load_data():
    nltk.download('movie_reviews')
    docs = [(list(movie_reviews.words(fileid)), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]
    return docs


def preprocess_data(docs):
    # This is a simple example of text preprocessing. You can customize it as needed.
    processed_docs = []
    for words, label in docs:
        # Join words to form a single string
        text = ' '.join(words)
        processed_docs.append((text, label))
    return processed_docs


def extract_features(processed_docs):
    X, y = zip(*processed_docs)
    vectorizer = CountVectorizer(stop_words='english')
    X_counts = vectorizer.fit_transform(X)
    tfidf_transformer = TfidfTransformer()
    X_tfidf = tfidf_transformer.fit_transform(X_counts)
    return X_tfidf, y


def split_data(X, y, val_size=0.2, test_size=0.2, random_state=None):
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=(val_size + test_size), random_state=random_state)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=(test_size / (val_size + test_size)), random_state=random_state)
    return X_train, X_val, X_test, y_train, y_val, y_test


def train_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model


def save_model(model, filename):
    joblib.dump(model, filename)


def load_model(filename):
    return joblib.load(filename)


def evaluate_model(model, X, y):
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, average='weighted')
    recall = recall_score(y, y_pred, average='weighted')
    f1 = f1_score(y, y_pred, average='weighted')
    return accuracy, precision, recall, f1


def display_results(dataset_name, accuracy, precision, recall, f1):
    print(f'{dataset_name} results:')
    print(f'  Accuracy: {accuracy:.4f}')
    print(f'  Precision: {precision:.4f}')
    print(f'  Recall: {recall:.4f}')
    print(f'  F1-score: {f1:.4f}\n')


if __name__ == "__main__":
    docs = load_data()
    processed_docs = preprocess_data(docs)
    X, y = extract_features(processed_docs)
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(X, y)

    # Train and save the model
    model = train_model(X_train, y_train)
    save_model(model, 'sentiment_analysis_model.joblib')

    # Load the saved model
    loaded_model = load_model('sentiment_analysis_model.joblib')

    # Evaluate the model on the validation and test datasets
    val_accuracy, val_precision, val_recall, val_f1 = evaluate_model(loaded_model, X_val, y_val)
    test_accuracy, test_precision, test_recall, test_f1 = evaluate_model(loaded_model, X_test, y_test)

    # Display the results
    display_results('Validation', val_accuracy, val_precision, val_recall, val_f1)
    display_results('Test', test_accuracy, test_precision, test_recall, test_f1)