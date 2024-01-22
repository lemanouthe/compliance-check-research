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
from sklearn.metrics import confusion_matrix, classification_report

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

BASE_DIR = "/Users/mamoutou.doumbia/Desktop/ComplianceCheck/research/rfp_domain/bbc"
LABELS = [
    "construction",
    "energy",
    "engineering",
    "environmental",
    "healthcare",
    "information technology (IT)",
    "logistics",
    "manufacturing",
    "scientific",
]


def create_data_set():
    with open("data_rfp_domain.txt", "w", encoding="utf-8") as outfile:
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
    with open("data_rfp_domain.txt", "r", encoding="utf-8") as datafile:
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

    X_train = []  # training documents
    y_train = []  # corresponding training labels

    X_test = []  # test documents
    y_test = []  # corresponding test label

    pivot = int(0.80 * len(docs))

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
    
    cm = confusion_matrix(y_test, y_pred)

    precision = metrics.precision_score(y_test, y_pred, average="micro")
    recall = metrics.recall_score(y_test, y_pred, average="micro")
    f1 = metrics.f1_score(y_test, y_pred, average="micro")

    print("%s\t%f\t%f\t%f\n" % (title, precision, recall, f1))
    # print(cm)
    print(classification_report(y_test, y_pred))


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

    evaluate_classifier(
        "Naive Bayes\tTRAIN\t", naive_bayes_classifier, vectorizer, X_train, y_train
    )
    evaluate_classifier(
        "Naive Bayes\tTEST\t", naive_bayes_classifier, vectorizer, X_test, y_test
    )

    # store the classifier
    clf_filename = "naive_bayes_classifier.pkl"
    pickle.dump(naive_bayes_classifier, open(clf_filename, "wb"))

    # also store the vectorizerso we can transform new data
    vec_filename = "count_vectorizer.pkl"
    pickle.dump(vectorizer, open(vec_filename, "wb"))


def classify(text):
    # load classifier
    clf_filename = "/Users/mamoutou.doumbia/Desktop/ComplianceCheck/research/rfp_domain/bbc/naive_bayes_classifier.pkl"
    nb_clf = pickle.load(open(clf_filename, "rb"))

    # vectorize the new text
    vec_filename = "/Users/mamoutou.doumbia/Desktop/ComplianceCheck/research/rfp_domain/bbc/count_vectorizer.pkl"
    vectorizer = pickle.load(open(vec_filename, "rb"))

    pred = nb_clf.predict(vectorizer.transform([text]))

    # print(pred[0].capitalize())
    return pred[0].capitalize()


if __name__ == "__main__":
    # create_data_set()
    docs = setup_docs()

    # print_frequency_dist(docs)
    train_classifier(docs)

    # deployement in production
    # new_doc = """
    # 1. Background
    # Recent advances in biomedical and health sciences—from immunotherapy to treat
    # cancer, to the highly effective COVID-19 vaccines—demonstrate the strengths and
    # successes of the U.S. biomedical enterprise. Such advances present an opportunity to
    # revolutionize how to prevent, treat, and even cure a range of diseases including cancer,
    # infectious diseases, Alzheimer’s disease, and many others that together affect a
    # significant number of Americans.
    # To improve the U.S. Government’s capabilities to speed research that can improve the
    # health of all Americans, the White House has created the Advanced Research Projects
    # Agency for Health (ARPA-H). Included in the President’s FY2022 budget was a
    # component of the National Institutes of Health (NIH) with a funding level of $1B
    # available for three years. ARPA-H will be tasked with building high-risk, high-reward
    # capabilities (or platforms) to drive biomedical breakthroughs—ranging from molecular
    # to societal—that would provide transformative solutions for all patients.
    # Congress has funded the Advanced Research Project Agency (Health) which is led as an
    # initiative by the Office of Science and Technology Policy (OSTP). ARPA-H is viewed
    # as an approach to support quick scientific research in the biomedical arena and is an
    # agency within the Department of Human and Health Services (HHS).
    # During the rapid start of ARPA-H, CIT services were leveraged, such as the
    # ServiceNow instance for incident management, while relying on other service area
    # capabilities provided by CIT (e.g., NIH network, Identity and Access Management
    # (IAM) Facilities, and STRIDES, etc.) as well as other critical administrative services
    # (e.g., Acquisitions/Contracting, Financial Management, HR, onboarding, Property
    # Management, etc.) and Technology Management and Customer Support (Helpdesk,
    # Training, etc.).
    # As ARPA-H continues to mature as an organization, ARPA-H and NIH executives want
    # to ensure that ARPA-H can develop a full range of IT services, systems or capabilities,
    # equipment, and technical support that is specific to performing the mission of ARPA-H
    # as an independent organization. Over time ARPA-H will in some cases necessitate a
    # move away from some CIT provided services to tools and services that better fit the
    # unique mission of the agency.
    # It is expected that ARPA-H, having its beginnings as a start-up federal agency, will grow
    # exponentially in size (personnel, facility, and equipment) as research projects are added.
    # As it does, the service delivery architecture will diverge from CIT’s support and the
    # ARPA-H Information Technology (IT) will increasingly become a stand-alone
    # environment. This document seeks to establish the initial Scope of IT Services and
    # means for creating a baseline of services to support the agency’s mission. The
    # Contractor understands and agrees that over time ARPA-H may require different
    # approaches for its support.
    # """

    # classify(new_doc)

    print("Done !!!")
