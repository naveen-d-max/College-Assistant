import nltk
try:
    print("Downloading punkt...")
    nltk.download('punkt', quiet=True)
    print("Downloading wordnet...")
    nltk.download('wordnet', quiet=True)
    print("Downloading omw-1.4...")
    nltk.download('omw-1.4', quiet=True)
    print("Test Tokenization: ", nltk.word_tokenize("Hello how are you?"))
except Exception as e:
    print("Error: ", e)
