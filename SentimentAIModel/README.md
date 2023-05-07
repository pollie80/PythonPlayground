# To run the code
`python sentiment_analysis.py`

# Next steps
Model is trained on built in dataset from package i.e. data folder is not used.
The accuracy can be improved, and to do so Word2Vec can be used and actually use the data folder.

# Operation

`load_data()`: Loads the movie_reviews dataset from NLTK and returns a list of tuples containing tokenized documents and their corresponding categories (positive or negative).

`preprocess_data(docs)`: Takes the raw documents as input and applies preprocessing techniques such as lowercasing and filtering out non-alphanumeric characters. Returns the preprocessed documents.

`build_word2vec_model(processed_docs, vector_size=100, window=5, min_count=1, workers=4)`: Trains a Word2Vec model on the preprocessed documents and returns the trained model.

`document_vector(word2vec_model, doc)`: Takes a trained Word2Vec model and a document as input, and returns the average of word vectors in the document.

`extract_features(processed_docs, word2vec_model)`: Uses the Word2Vec model to extract features from the preprocessed documents and returns the feature matrix (X) and corresponding labels (y).

`split_data(X, y, val_size=0.2, test_size=0.2, random_state=None)`: Splits the data into training, validation, and test sets.

`train_model(X_train, y_train)`: Trains a logistic regression model on the training dataset and returns the trained model.

`save_model(model, filename)`: Saves the trained model to a specified file.

`load_model(filename)`: Loads the saved model from a specified file and returns the loaded model.

`evaluate_model(model, X, y)`: Evaluates the performance of a trained model on a given dataset (X, y) and returns accuracy, precision, recall, and F1 scores.

`display_results(dataset_name, accuracy, precision, recall, f1)`: Displays the evaluation metrics for a given dataset.

`process_input(text, word2vec_model)`: Processes the user input by tokenizing and converting it into a document vector using the Word2Vec model.

`predict_sentiment(loaded_model, text, word2vec_model)`: Predicts the sentiment of the user input using the loaded model and returns the prediction (positive or negative).

[//]: # (https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis)
[//]: # (data/twitter_training.csv data/twitter_validation.csv "I love this new phone" "phone")