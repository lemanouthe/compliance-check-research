import ssl
import os
import random
import string
import nltk
from collections import defaultdict
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import pickle

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


stop_words = set(stopwords.words("english"))
stop_words.add("said")
stop_words.add("mr")

# nltk.download('punkt')
# nltk.download('stopwords')

# example_string = """
#     Muad'Dib learned rapidly because his first training was in how to learn.
#     And the first lesson of all was the basic trust that he could learn.
#     It's shocking to find how many people do not believe they can learn,
#     and how many more believe learning to be difficult."""

# print(sent_tokenize(example_string))

BASE_DIR = (
    "/Users/mamoutou.doumbia/Desktop/ComplianceCheck/research/requirementsDomain/bbc"
)
LABELS = [
    "artificial intelligence (AI)",
    "cloud computing",
    "data",
    "hardware",
    "internet of things (IoT)",
    "networks",
    "security",
    "software",
]


def create_data_set():
    with open("data_domain.txt", "w", encoding="utf-8") as outfile:
        for label in LABELS:
            dir = "%s/%s" % (BASE_DIR, label)
            for filename in os.listdir(dir):
                fullfilename = "%s/%s" % (dir, filename)
                # print(fullfilename)
                with open(fullfilename, "rb") as file:
                    text = file.read().decode(errors="replace").replace("\n", "")
                    outfile.write("%s\t%s\t%s\n" % (label, filename, text))
                    # outfile.flush()


def setup_docs():
    docs = []  # (label, text)
    with open("data_domain.txt", "r", encoding="utf-8") as datafile:
        for row in datafile:
            parts = row.split("\t")
            doc = (parts[0], parts[2].strip())

            docs.append(doc)
    return docs


def clean_text(text):
    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # convert to lower case
    text = text.lower()
    return text


def get_tokens(text):
    # get individual words
    tokens = word_tokenize(text)
    # remove common words that are useless
    tokens = [t for t in tokens if not t in stop_words]

    return tokens


def print_frequency_dist(docs):
    tokens = defaultdict(list)

    # Lets make a giant list of all the words for each category
    for doc in docs:
        doc_label = doc[0]

        doc_text = clean_text(doc[1])

        doc_tokens = get_tokens(doc_text)

        tokens[doc_label].extend(doc_tokens)

    for category_label, category_tokens in tokens.items():
        print(category_label)
        fd = FreqDist(category_tokens)
        print(fd.most_common(20))

def get_splits(docs):
    # scramble docs
    random.shuffle(docs)
    
    X_train = [] # training documents
    y_train = [] # corresponding training labels
    
    X_test = [] # test documents
    y_test = [] # corresponding test label
    
    pivot = int(.80 * len(docs))
    
    for i in range(0, pivot):
        X_train.append(docs[i][1])
        y_train.append(docs[i][0])
    
    for i in range(pivot, len(docs)):
        X_test.append(docs[i][1])
        y_test.append(docs[i][0])

    return X_train, X_test, y_train, y_test

def evaluate_classifier(title, classifier, vectorizer, X_test, y_test):
    X_test_tfidf = vectorizer.transform(X_test)
    y_pred = classifier.predict(X_test_tfidf)
    
    precision = metrics.precision_score(y_test, y_pred, average='micro')
    recall = metrics.recall_score(y_test, y_pred, average='micro')
    f1 = metrics.f1_score(y_test, y_pred, average='micro')
    
    print("%s\t%f\t%f\t%f\n" % (title, precision, recall, f1))
    
def train_classifier(docs):
    X_train, X_test, y_train, y_test = get_splits(docs)

    # the object that turns text into vectors
    vectorizer = CountVectorizer(
        stop_words="english", ngram_range=(1, 3), min_df=3, analyzer="word"
    )
    
    # create doc-term matrix
    dtm = vectorizer.fit_transform(X_train)
    
    # train Naive Bayes classifier
    naive_bayes_classifier = MultinomialNB().fit(dtm, y_train)
    
    evaluate_classifier("Naive Bayes\tTRAIN\t", naive_bayes_classifier, vectorizer, X_train, y_train)
    evaluate_classifier("Naive Bayes\tTEST\t", naive_bayes_classifier, vectorizer, X_test, y_test)
    
    # store the classifier
    clf_filename = 'naive_bayes_classifier.pkl'
    pickle.dump(naive_bayes_classifier, open(clf_filename, 'wb'))
    
    # also store the vectorizerso we can transform new data
    vec_filename = 'count_vectorizer.pkl'
    pickle.dump(vectorizer, open(vec_filename, 'wb'))


def classify(text):
    # load classifier
    clf_filename = '/Users/mamoutou.doumbia/Desktop/ComplianceCheck/research/requirementsDomain/bbc/naive_bayes_classifier.pkl'
    nb_clf = pickle.load(open(clf_filename, 'rb'))
    
    # vectorize the new text
    vec_filename = '/Users/mamoutou.doumbia/Desktop/ComplianceCheck/research/requirementsDomain/bbc/count_vectorizer.pkl'
    vectorizer = pickle.load(open(vec_filename, 'rb'))
    
    pred = nb_clf.predict(vectorizer.transform([text]))
    
    # print(pred[0].capitalize())
    return pred[0].capitalize()

if __name__ == "__main__":
    # create_data_set()
    # docs = setup_docs()

    # print_frequency_dist(docs)
    # train_classifier(docs)
    
    # deployement in production
    # new_doc = "Update existing databases or spreadsheets as needed." # software
    # new_doc = "Provide one mid-senior level Executive Administrative Support to two Government executives and approximately 40 personnel within the SG5 Capability Development Division, located at Defense Health Headquarters (DHHQ), 7700 Arlington Blvd., Falls Church, VA." # hardware
    # new_doc = "Review, edit, and update documents to ensure proper format, spelling, grammar, capitalization, and punctuation." # cloud computing
    # new_doc = "Prepare and submit documents in appropriate formats in accordance with the latest Air Force Handbook (AFH) 33-337, The Tongue and Quill." # software
    # new_doc = "Handle telephone calls and visitors efficiently, screening for requests that can be handled without assistance." # hardware
    # new_doc = "Reports shall be detailed at the  project level as specified per each task and shall include costs incurred to  date and planned costs to project completion." # security
    # new_doc = "The resulting technology and data should be re-usable by future entities and people whenever possible." # Internet of things
    # new_doc = "The Contractor shall maintain data and information that relates technical components of infrastructure with business requirements." # software
    # new_doc = "The technical component shall focus on areas such as data gathering, requirements definition; technical design; development; testing, installation,  interoperability, operational support, maintenance, and management of software as Government assets." # Hardware
    new_doc = "IT Security Management and Compliance  Security Management services and compliance includes the physical and logical  security of all Government assets, software application components and data, access  protection and other IT related security services and shall be in compliance with ARPAH Security policies and all applicable federal regulatory requirements." # Security
    
    classify(new_doc)

    print("Done !!!")
