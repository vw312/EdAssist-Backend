from xml.etree import ElementTree
import nltk
from nltk.corpus import wordnet
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


# holds helper function to carry out nlp operations needed in this project

def extract_document(caption):
    """Extracts documents from the given ttml caption"""
    ns = {'ttml': 'http://www.w3.org/ns/ttml'}
    xml_document = ElementTree.fromstring(caption)
    div = xml_document.find('ttml:body', ns).find('ttml:div', ns)
    ptags = div.findall('ttml:p', ns)
    document = ' '.join(ptag.text for ptag in ptags)

    return document


def preprocessing(document):
    """Removes punctuation, stop words and tokenizes and lemmatizes """
    # Step 1 remove punctuation & numbers and converting to lower case
    document = document.lower()
    doc_no_punct = "".join([c for c in document if c not in string.punctuation and c not in ['0', '1', '2', '3', '4',
                                                                                             '5', '6', '7', '8', '9']])

    # Step 2 tokenization
    tokens = nltk.tokenize.word_tokenize(doc_no_punct)

    # Step 3 remove stop words
    stopwords = nltk.corpus.stopwords.words('english')
    tokens_nostop = [word for word in tokens if word not in stopwords]

    # Step 4 lemmatize
    tokens_tagged = nltk.pos_tag(tokens_nostop)
    wn = nltk.WordNetLemmatizer()
    tokens_clean = [wn.lemmatize(word, nltk_to_wordnet_tag(tag)) for word, tag in tokens_tagged]

    return tokens_clean


def important_words(corpus):
    """Applies tfidf vectorizer on the corpus extracts and returns a list of the top 5 important_words from each
    document """
    tfidf_vect = TfidfVectorizer(analyzer=preprocessing)
    X = tfidf_vect.fit_transform(corpus)
    values_top5 = [np.argsort(array)[::-1][:5] for array in X.toarray()]  # top 5 tidf values (by index) for each
    # document
    words = tfidf_vect.get_feature_names()
    result = []
    for array in values_top5:
        temp = [words[i] for i in array]  # top words for a particular document
        result.append(temp)

    return result


def nltk_to_wordnet_tag(nltk_tag):
    """Converts a nltk pos_tag to a wordnet pos_tag"""
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # default
