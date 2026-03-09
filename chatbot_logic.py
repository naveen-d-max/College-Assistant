import json
import pickle
import numpy as np
import random
import os
import re

# Internal simple tokenizer & stemmer
def tokenize(sentence):
    return re.findall(r'\w+', sentence.lower())

def stem(word):
    word = word.lower()
    suffixes = ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word

# Load model and preprocessed data
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = pickle.load(open('chatbot_model.pkl', 'rb'))

# Load intents
intents_path = os.path.join(os.path.dirname(__file__), 'intents.json')
with open(intents_path, 'r') as file:
    intents = json.load(file)

def bag_of_words(sentence):
    sentence_words = [stem(w) for w in tokenize(sentence)]
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    # Predict probabilities
    res = model.predict_proba(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    if not intents_list:
        return "I'm sorry, I didn't quite understand that. Could you rephrase your question?"
    
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def get_chatbot_response(message):
    ints = predict_class(message)
    res = get_response(ints, intents)
    return res
