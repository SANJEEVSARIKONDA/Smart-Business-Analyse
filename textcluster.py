from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
import numpy as np
from collections import Counter
import sys
def text_clust(test):
    
    ''''sys.setdefaultencoding("utf-8")
    reload(sys)'''
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    # Cleaning the text sentences so that punctuation marks, stop words & digits are removed  
    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        processed = re.sub(r"\d+","",normalized)
        y = processed.split()
        return y
    path = "sente.txt"

    train_clean_sentences = []
    fp = open(path,'r')
    for line in fp:
        line = line.strip()
        cleaned = clean(line)
        cleaned = ' '.join(cleaned)
        train_clean_sentences.append(cleaned)
           
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(train_clean_sentences)

    # Creating true labels for 30 training sentences 
    y_train = np.zeros(24)
    y_train[12:24] = 2

    # Clustering the document with KNN classifier
    modelknn = KNeighborsClassifier(n_neighbors=5)
    modelknn.fit(X,y_train)

    # Clustering the training 30 sentences with K-means technique 
    
    modelkmeans = KMeans(n_clusters=2, init='k-means++', max_iter=200, n_init=100)
    modelkmeans.fit(X)

    test_clean_sentence = []
    cleaned_test = clean(test)
    cleaned = ' '.join(cleaned_test)
    cleaned = re.sub(r"\d+","",cleaned)
    test_clean_sentence.append(cleaned)
        
    Test = vectorizer.transform(test_clean_sentence) 
    predicted_labels_kmeans = modelkmeans.predict(Test)
    pre = predicted_labels_kmeans
    print(pre)
    if pre == [0]:
        cat = "food"
    elif pre == [1]:
        cat = "rooms"
    else:
        cat = "no_cat"
    return cat