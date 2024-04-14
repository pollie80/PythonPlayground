import pandas as pd
import ssl
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Required for loading word embeddings
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Load the data
print("loading data")
df = pd.read_csv('../data/twitter_training.csv', usecols=[2, 3], header=None)
df.columns = ['class', 'sentence']

# Preprocessing
print()
stop_words = set(stopwords.words('english'))
df['sentence'] = df['sentence'].apply(lambda x: ' '.join(
    term for term in word_tokenize(x) if term not in stop_words))

# Converting class to numeric values
df['class'] = df['class'].map({'Negative': 0, 'Neutral': 1, 'Positive': 2})

# Splitting into training and testing sets
train, test = train_test_split(df, test_size=0.2, random_state=42)

# Tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(train['sentence'])
vocab_size = len(tokenizer.word_index) + 1

# Sequencing and padding
max_seq_length = max([len(s.split()) for s in train['sentence']])
train_seq = tokenizer.texts_to_sequences(train['sentence'])
train_padded = pad_sequences(train_seq, maxlen=max_seq_length, padding='post')
test_seq = tokenizer.texts_to_sequences(test['sentence'])
test_padded = pad_sequences(test_seq, maxlen=max_seq_length, padding='post')

# Load word embeddings (replace PATH_TO_GLOVE with your path to the GloVe word embeddings)
embeddings_index = {}
with open('PATH_TO_GLOVE/glove.6B.100d.txt') as f:
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs

# Create an embedding matrix
embedding_matrix = np.zeros((vocab_size, 100))  # we chose 100d glove model
for word, i in tokenizer.word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector

# Model architecture
model = Sequential()
model.add(Embedding(vocab_size, 100, weights=[embedding_matrix], input_length=max_seq_length, trainable=False))
model.add(LSTM(100))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))  # 3 classes: Negative, Neutral, Positive

# Compile the model
model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Fit the model
model.fit(train_padded, train['class'], validation_data=(test_padded, test['class']), epochs=5, callbacks=[EarlyStopping(monitor='val_loss', patience=3)])

# Evaluate model on test set
score = model.evaluate(test_padded, test['class'], verbose=1)
print("Test Score:", score[0])
print("Test Accuracy:", score[1])
