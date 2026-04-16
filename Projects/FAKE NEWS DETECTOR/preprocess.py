# import re
# import contractions
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer

# # Download required NLTK data (runs once)
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# stop_words = set(stopwords.words('english'))
# lemmatizer = WordNetLemmatizer()

# def preprocess_input(text):

#     # 1. Expand contractions
#     text = contractions.fix(text)

#     # 2. Lowercase
#     text = text.lower()

#     # 3. Remove punctuation
#     text = re.sub(r'[^\w\s]', '', text)

#     # 4. Remove URLs + words with digits
#     text = re.sub(r'http\S+|www\S+', '', text)
#     text = re.sub(r'\w*\d\w*', '', text)

#     # 5. Tokenization + stopword removal
#     words = word_tokenize(text)
#     words = [word for word in words if word not in stop_words]

#     # 6. Lemmatization
#     words = [lemmatizer.lemmatize(word) for word in words]

#     # 7. Join back
#     text = " ".join(words)

#     # 8. Clean spaces
#     text = re.sub(r'\s+', ' ', text).strip()

#     return text

import re
import contractions
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# -------- SAFE DOWNLOAD (only if missing) --------
def setup_nltk():
    resources = [
        ('tokenizers/punkt', 'punkt'),
        ('tokenizers/punkt_tab', 'punkt_tab'),
        ('corpora/stopwords', 'stopwords'),
        ('corpora/wordnet', 'wordnet')
    ]

    for path, name in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(name)

setup_nltk()
# -----------------------------------------------

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def preprocess_input(text):

    # 1. Expand contractions
    text = contractions.fix(text)

    # 2. Lowercase
    text = text.lower()

    # 3. Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # 4. Remove URLs + words with digits
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\w*\d\w*', '', text)

    # 5. Tokenization + stopword removal
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words]

    # 6. Lemmatization
    words = [lemmatizer.lemmatize(word) for word in words]

    # 7. Join back
    text = " ".join(words)

    # 8. Clean spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text