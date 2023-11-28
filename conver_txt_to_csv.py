import csv

# Ouvrir le fichier data.txt
with open('requirementsDomain/bbc/data_domain.txt', 'r') as file:
    lines = file.readlines()

# Séparer les catégories et les textes
data = [line.strip().split('\t') for line in lines]

# Écrire dans un fichier CSV
with open('data_domain.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['category', 'filename', 'text'])  # Écriture des en-têtes
    writer.writerows(data)
