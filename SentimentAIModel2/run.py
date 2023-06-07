import string
import pandas as pd
from gensim.models import Word2Vec
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    # Lowercase the text
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)

    # Remove user @ references and '#' from text
    text = re.sub(r'\@\w+|\#','', text)

    # Remove punctuations
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove stopwords and lemmatize
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

    return tokens


# Load your data
train_df = pd.read_csv('../SentimentAIModel/data/twitter_training.csv')
validation_df = pd.read_csv('../SentimentAIModel/data/twitter_validation.csv')

# Preprocess your data (this will vary depending on your data)
train_df['processed_text'] = train_df['text'].apply(preprocess_text)
validation_df['processed_text'] = validation_df['text'].apply(preprocess_text)

# Train a Word2Vec model
word2vec = Word2Vec(train_df['processed_text'], min_count=2)

# Vectorize your data
vectorizer = TfidfVectorizer(analyzer=lambda x: x)
train_matrix = vectorizer.fit_transform(train_df['processed_text'])
validation_matrix = vectorizer.transform(validation_df['processed_text'])

# Train a classifier
clf = RandomForestClassifier()
clf.fit(train_matrix, train_df['sentiment'])

# Evaluate on validation data
validation_preds = clf.predict(validation_matrix)
print(classification_report(validation_df['sentiment'], validation_preds))

# Function to predict sentiment of new input data
def predict_sentiment(input_data):
    processed_input = your_preprocessing_function(input_data)
    input_matrix = vectorizer.transform([processed_input])
    prediction = clf.predict(input_matrix)
    return prediction
