import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenization
    tokens = word_tokenize(text)
    # Stopwords removal
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    lemmatized_freq = Counter(lemmatized_tokens)
    print("original_tokens", tokens, "\nfiltered_tokens", filtered_tokens,
          "\nstemmed_tokens", stemmed_tokens, "\nnltk_lemmatized_tokens", lemmatized_tokens)
    
    return lemmatized_tokens, lemmatized_freq

# text = "Machine learning is a relevant branch of artificial intelligence"
# processed_text = preprocess_text(text)
# print(processed_text)
