import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("Downloading NLTK data...")
nltk.download('punkt', quiet=False)
nltk.download('wordnet', quiet=False)
nltk.download('omw-1.4', quiet=False)
print("Finished!")
