import nltk
nltk.download('movie_reviews')
nltk.download('punkt')

from textblob import TextBlob

while True:
    # Ask the user for input
    user_input = input("Enter a sentence (or 'exit' to quit): ")

    # Check if the user wants to exit
    if user_input.lower() == 'exit':
        break

    # Create a TextBlob object
    blob = TextBlob(user_input)

    # Get sentiment polarity
    sentiment_score = blob.sentiment.polarity

    # Classify sentiment
    if sentiment_score > 0:
        sentiment = "positive"
    elif sentiment_score < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    print(f"Sentiment: {sentiment}")
