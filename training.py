import os
import numpy as np
import pickle
import pandas as pd
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras.preprocessing.sequence import pad_sequences
from keras.metrics import SparseCategoricalAccuracy


# Params
VOCAB_SIZE = 10000
MAX_LEN = 250
EMBEDDING_DIM = 16
MODEL_PATH = 'sentiment_analysis_model.h5'

file_path = 'training.1600000.processed.noemoticon.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')
df_shuffled = data.sample(frac=1).reset_index(drop=True)

texts = []
labels = []


for _, row in df_shuffled.iterrows():
    texts.append(row.iloc[-1])
    label = row.iloc[0]
    labels.append(0 if label == 0 else 1 if label == 2 else 2)

texts = np.array(texts)
labels = np.array(labels)


tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=VOCAB_SIZE) #deprecated 
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
padded_sequences = pad_sequences(sequences, maxlen=MAX_LEN, value=VOCAB_SIZE-1, padding='post')

with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

train_data = padded_sequences[:-5000]
test_data = padded_sequences[-5000:]
train_labels = labels[:-5000]
test_labels = labels[-5000:]

if os.path.exists(MODEL_PATH):
    print("Loading saved model...")
    model = load_model(MODEL_PATH)
else:
    print("Training new model...")
    model = Sequential([
        Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=MAX_LEN),
        GlobalAveragePooling1D(),
        Dense(16, activation='relu'),
        Dense(3, activation='softmax') # negative, neutral, positive
    ])

    # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=[SparseCategoricalAccuracy()])

    model.fit(train_data, train_labels, epochs=10, batch_size=10, validation_split=0.2)

    model.save(MODEL_PATH)

# Evaluate Model
loss, accuracy = model.evaluate(test_data, test_labels)
print(f"Test accuracy: {accuracy * 100:.2f}%")

def encode_text(text):
    tokens = tf.keras.preprocessing.text.text_to_word_sequence(text)
    tokens = [tokenizer.word_index[word] if word in tokenizer.word_index else 0 for word in tokens]
    return pad_sequences([tokens], maxlen=MAX_LEN, padding='post', value=VOCAB_SIZE-1)

while True:
    user_input = input("Input a sentence ('exit' to quit):")
    if user_input.lower() == 'exit':
        break

    encoded_input = encode_text(user_input)
    prediction = np.argmax(model.predict(encoded_input))

    match prediction:
        case 0:
            print('Negative')
        case 1:
            print("Neutral")
        case _:
            print("Positive")

