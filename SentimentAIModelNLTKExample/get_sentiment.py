import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')

analyzer = SentimentIntensityAnalyzer()


def get_sentiment(sentence):
    sentiment_scores = analyzer.polarity_scores(sentence)
    compound_score = sentiment_scores['compound']
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


example_sentences = [
    'I love this movie!',
    'I hate Mondays.',
    'He is standing..',
]

for sentence in example_sentences:
    sentiment = get_sentiment(sentence)
    print(f'Sentence: {sentence}')
    print(f'Sentiment: {sentiment}\n')

user_sentence = input('Enter a sentence: ')
user_sentiment = get_sentiment(user_sentence)
print(f'Sentence: {user_sentence}')
print(f'Sentiment: {user_sentiment}')
