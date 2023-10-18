import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


# Chargez les exemples de formation depuis un fichier CSV
training_data = pd.read_csv('confidence_training.csv')  # Remplacez 'votre_fichier.csv' par le nom de votre fichier CSV

# Créez le vecteur TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_train = tfidf_vectorizer.fit_transform(training_data['text'])  # Assurez-vous que la colonne contenant les textes est nommée 'text'
y_train = training_data['category']  # Assurez-vous que la colonne contenant les catégories est nommée 'category'


# Créez le classificateur
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Nouvelle phrase à classifier
new_sentence = "The Contractor shall comply with the following documents, in addition to the documents in Paragraph"

# Transformez la nouvelle phrase en vecteur TF-IDF
X_new = tfidf_vectorizer.transform([new_sentence])

# Prédisez la catégorie de la nouvelle phrase
predicted_category = classifier.predict(X_new)

# Obtenez la probabilité de prédiction
proba = classifier.predict_proba(X_new)
confidence_factor = round(proba.max(), 2) #proba.max()


print("Catégorie prédite :", predicted_category)
print("Facteur de confiance :", confidence_factor)