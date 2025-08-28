import random
from datetime import datetime
import json
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import os
import pyjokes

# Download resources if not already downloaded
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')        # Optional but helps WordNet
# nltk.download('averaged_perceptron_tagger')  # Optional for future upgrades


# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Step 3: Load and preprocess data
file_path = os.path.join(os.path.dirname(__file__), "..", "data", "intents.json")
file_path = os.path.abspath(file_path)

with open(file_path, "r") as file:
    intents = json.load(file)

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

# Step 4: Utility functions

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    sentence_words = clean_up_sentence(sentence)
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if any(word in sentence_words for word in nltk.word_tokenize(pattern.lower())):
                return intent["tag"]
    return "unknown"

def get_response(intent_tag):
    for intent in intents["intents"]:
        if intent["tag"] == intent_tag:
            # Special case: return live joke using pyjokes
            if intent_tag == "joke":
                return pyjokes.get_joke()

            # Special case: dynamic time
            response = random.choice(intent["responses"])
            if "{{TIME}}" in response:
                return response.replace("{{TIME}}", datetime.now().strftime("%I:%M %p"))

            return response
    return "Sorry, I didn't get that."


# if __name__ == "__main__":
#     print("Chatbot ready. Type 'quit' to exit.")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == "quit":
#             break
#         tag = predict_class(user_input)
#         response = get_response(tag)
#         print("Bot:", response)
