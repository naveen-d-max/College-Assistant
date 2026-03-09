import json
import numpy as np
import random
import pickle
import os
import re
from sklearn.neural_network import MLPClassifier

# Simple internal tokenizer
def tokenize(sentence):
    return re.findall(r'\w+', sentence.lower())

# Simple internal stemmer
def stem(word):
    word = word.lower()
    suffixes = ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word

# Load intents
intents_path = os.path.join(os.path.dirname(__file__), 'intents.json')
with open(intents_path, 'r') as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

# Preprocess patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word
        word_list = tokenize(pattern)
        words.extend(word_list)
        # Add to documents
        documents.append((word_list, intent['tag']))
        # Add to classes if not already there
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Stem and lower each word and remove duplicates
words = [stem(w) for w in words if w not in ignore_letters]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

# Save words and classes
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Create training data
training = []

for doc in documents:
    bag = []
    word_patterns = doc[0]
    word_patterns = [stem(word) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    # Output is index of the class
    output_row = classes.index(doc[1])
    training.append([bag, output_row])

random.shuffle(training)

train_x = np.array([row[0] for row in training])
train_y = np.array([row[1] for row in training])

# Train model
model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=1000, random_state=1, activation='relu', solver='adam')
model.fit(train_x, train_y)

# Save model
pickle.dump(model, open('chatbot_model.pkl', 'wb'))

print("Model created and saved successfully without NLTK dependency!")
