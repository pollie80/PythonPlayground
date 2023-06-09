import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

def load_data():
    print("loading data...")
    data = fetch_20newsgroups(subset='all')
    return data

def preprocess_data(data):
    print("preprocessing data...")
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(data.data)
    return vectors, vectorizer

def split_data(vectors, data):
    print("splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(vectors, data.target, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    print("training model...")
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def save_model(model, filename):
    print("saving model...")
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

def load_model(filename):
    print("loading model...")
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    return model

def evaluate_model(model, X_test, y_test):
    print("evaluating...")
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return accuracy

def classify_sentence(model, vectorizer, sentence):
    sentence_vector = vectorizer.transform([sentence])
    prediction = model.predict(sentence_vector)
    return prediction

def main():
    # Load and preprocess data
    data = load_data()
    vectors, vectorizer = preprocess_data(data)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = split_data(vectors, data)

    # Train the model
    model = train_model(X_train, y_train)

    # Save the model
    save_model(model, 'model.pkl')

    # Load the model
    model = load_model('model.pkl')

    # Evaluate the model
    accuracy = evaluate_model(model, X_test, y_test)
    print(f"Model accuracy: {accuracy}")

    # Classify a sentence
    sentence = input("Enter a sentence to classify: ")
    prediction = classify_sentence(model, vectorizer, sentence)
    print(f"Predicted class: {prediction}")

if __name__ == "__main__":
    main()
