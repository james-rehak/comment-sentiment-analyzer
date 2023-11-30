import numpy as np
import pickle
import pandas as pd
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.preprocessing.sequence import pad_sequences

VOCAB_SIZE = 10000
MAX_LEN = 250
EMBEDDING_DIM = 16
MODEL_PATH = 'sentiment_analysis_model.h5'

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

model = load_model(MODEL_PATH)


def encode_text(text_list):
    encoded_text = []
    for text in text_list:
        tokens = tf.keras.preprocessing.text.text_to_word_sequence(text)
        tokens = [tokenizer.word_index[word] if word in tokenizer.word_index else 0 for word in tokens]
        encoded_text.append(tokens)
    return pad_sequences(encoded_text, maxlen=MAX_LEN, padding='post', value=VOCAB_SIZE-1)

def predict_sentiment(text_list):
    encoded_inputs = encode_text(text_list)
    predictions = np.argmax(model.predict(encoded_inputs), axis=-1)
    sentiment = []

    for prediction in predictions:
        match prediction:
            case 0:
                sentiment.append("Negative")
            case 1:
                sentiment.append("Neutral")
            case _:
                sentiment.append("Positive")
                
    return sentiment
