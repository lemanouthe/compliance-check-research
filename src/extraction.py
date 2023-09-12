import re
import os
import json
import PyPDF2
from docx import Document


def clean_text(text):
    # Supprimer les caractères spéciaux, les sauts de ligne inutiles et les espaces en double
    cleaned_text = re.sub(r"[^\w\s]", "", text)
    cleaned_text = re.sub(r"\n+", "\n", cleaned_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text.strip()


def segment_sentences(text):
    # Segmenter le texte en phrases
    sentences = re.findall(r"[^.!?]+[.!?]", text)
    # sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    return sentences


def segment_paragraphs(text):
    # Remplacer les sauts de ligne par des espaces pour nettoyer les paragraphes
    cleaned_text = re.sub(r"\n", " ", text)
    cleaned_text = re.sub(r"–", "", cleaned_text).strip()
    # Segmenter le texte en paragraphes
    paragraphs = re.split(r"\n\n+", cleaned_text)
    return paragraphs


def is_requirement(sentence):
    # Définissez ici vos critères pour identifier une phrase comme étant une exigence
    # Par exemple, vous pouvez vérifier si la phrase contient certains mots clés ou motifs spécifiques.
    keywords = [
        "shall",
        "must",
        "should",
        "have to",
        "need to",
        "review",
        "edit",
        "update",
        "ensure",
        "prepare and submit",
        "handle",
    ]  # Liste de mots clés à rechercher

    # return any(keyword in sentence.lower() for keyword in keywords) and sentence.strip().endswith('.')
    return any(keyword in sentence.lower() for keyword in keywords)


def read_pdf(file_path):
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()

    return text


def read_docx(file_path):
    doc = Document(file_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text


def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as txt_file:
        text = txt_file.read()
    return text


def extract_requirements_from_text_file(file_path):
    extension = file_path.split(".")[-1]
    if extension == "pdf":
        content = read_pdf(file_path)
    elif extension == "docx":
        content = read_docx(file_path)
    elif extension == "txt":
        content = read_txt(file_path)
    else:
        print("Extension de fichier non prise en charge.")
        # return
    # Lire le texte du fichier et effectuer le nettoyage
    # with open(file_path, 'r', encoding='utf-8') as file:
    #     content = file.read()
    # cleaned_text = clean_text(content)

    paragraphs = segment_paragraphs(content)

    segmented_text = []
    for paragraph in paragraphs:
        # print(paragraph)
        sentences = segment_sentences(paragraph)
        # print(sentences)
        segmented_text.extend(sentences)

        # Segmenter le texte en phrases
        # sentences = segment_sentences(cleaned_text)
        # print(segmented_text)

        # requirements = re.findall(r'(?:^|\n)(.*?)(?=\n|$)', cleaned_text)
        # requirements = re.findall(r'\bshall\b\s*(.*?)\n', content, re.IGNORECASE)
        # return requirements
    return segmented_text


# if __name__ == "__main__":
#     main()
