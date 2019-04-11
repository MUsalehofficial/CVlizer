import re
import unicodedata
import PyPDF2
import textract
import nltk
# import MySQLdb

from pymongo import MongoClient
from autocorrect import spell
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

import LoadCVs

"""
def decode_unicode_chars(words):
    return unicodedata.normalize('NFD', words).encode('ascii', 'ignore')
"""
def decode_non_ascii(words):
    """Decode non-ASCII characters from a list of tokenized words"""
    new_words = []
    for w in words:
        nw = unicodedata.normalize('NFD', w).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(nw)
    return new_words


def array_to_lowercase(words):
    """Convert all characters to lowercase from a list of tokenized words"""
    return list(map(lambda item: item.lower(), words))


def remove_punctuation(words):
    """Remove punctuation from a list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def remove_stopwords(words):
    """Remove stopwords from a list of tokenized words"""
    stops = set(stopwords.words('english'))
    # words=word_tokenize(sentence)
    filtered_sentence = []
    for w in words:
        if w not in stops:
            filtered_sentence.append(w)
    return filtered_sentence


def stem_words(words):
    """Stem words from a list of tokenized words"""
    stemmer = PorterStemmer()
    list_words = []
    for word in words:
        stem = stemmer.stem(word)
        list_words.append(stem)
    return list_words


def lemmatize_verbs(words):
    """Lemmatize verbs from a list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    new_words = []
    for word in words:
        new_word = lemmatizer.lemmatize(word, pos='v')
        # print(new_word)
        new_words.append(new_word)
        # print(new_words)
        # print(lemmatizer.lemmatize("cats"))
    return new_words


def normalization(words):
    words = decode_non_ascii(words)
    words = array_to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_stopwords(words)
    words = stem_words(words)
    words = lemmatize_verbs(words)
    return words


""" This function will be used while calling the algorithm """
def spell_correct(string):
    # words = string.split(" ")
    words = word_tokenize(string)
    correctWords = []
    for i in words:
        correctWords.append(spell(i))
    return " ".join(correctWords)


# aa = spell_correct("")
# print(aa)
# aa = stem_words(['worked', 'played', 'running'])
# print(aa)
# p = decode_non_ascii(['ÈÀ', 'Æ', 'À'])
# print(p)


def parse_cvs():
    parsedCVs = []
    orderedCVs = []
    # cvFileNames = []
    tempPDF = ''
    # LIST_OF_FILES = ['Professional-SRSs.docx','test.docx']
    tempCV = ''
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ACVAS']
    for no, i in enumerate(LoadCVs.load_cvs()):
        orderedCVs.append(i)
        print(orderedCVs)
        Temp = i.split(".")
        # print(no, i)
        applicant = db['Applicants'].find_one({
            'CV': i
        })
        if not applicant['CV_parsed']:
            if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
                try:
                    with open(i, 'rb') as pdf_file:
                        read_pdf = PyPDF2.PdfFileReader(pdf_file)
                        number_of_pages = read_pdf.getNumPages()
                        for page_number in range(number_of_pages):
                            page = read_pdf.getPage(page_number)
                            page_content = page.extractText()
                            page_content = page_content.replace('\n', ' ')
                            # page_content.replace("\r", "")
                            tempPDF = str(tempPDF) + str(page_content)
                            # print(tempPDF)
                        parsedCVs.extend([tempPDF])
                        tempCV = tempPDF
                        tempPDF = ''
                        print("This is a *.PDF file:", i)
                except Exception as e:
                    print(e)
            if Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
                try:
                    a = textract.process(i)
                    a = a.replace(b'\n', b' ')
                    a = a.replace(b'\r', b' ')
                    b = str(a)
                    c = [b]
                    tempCV = c
                    parsedCVs.extend(c)
                    print("This is a *.DOCX file: ", i)
                except Exception as e:
                    print(e)
            if Temp[1] == "doc" or Temp[1] == "Doc" or Temp[1] == "DOC":
                try:
                    # cwd = os.getcwd()
                    # print(cwd)
                    a = textract.process(i)
                    a = a.replace(b'\n', b' ')
                    a = a.replace(b'\r', b' ')
                    b = str(a)
                    c = [b]
                    # print(c)
                    tempCV = c
                    parsedCVs.extend(c)
                    print("This is a *.DOC file: ", i)
                except Exception as e:
                    print(e)
            print("CV: " + i + ", has been parsed successfully.")

            # applicant = db['Applicants'].find_one({
            #     'CV': i
            # })
            # if not applicant['cv_parsed']:
            # print(id)
            # applicants = db['Applicants']
            db['CV_Content'].insert_one({
                '_id': applicant['_id'],
                'CV_Filename': applicant['CV'],
                'CV_Content': str(tempCV),
                'CV_Normalized': False
            })
            db['Applicants'].update_one({
                '_id': applicant['_id']
            }, {"$set": {
                'CV_parsed': True
            }})
            print("CV: " + i + ", content has been inserted into database successfully.")

        cvContent = db['CV_Content'].find_one({
            'CV_Filename': i
        })
        if not cvContent['CV_Normalized']:
            a = nltk.word_tokenize(str(tempCV))
            b = normalization(a)
            c = ' '.join(b)
            tempCV = c
            print("CV: " + i + ", has been normalized successfully.")
            # print(tempCV)
            db['CV_Content_Normalized'].insert_one({
                '_id': cvContent['_id'],
                'CV_Filename': cvContent['CV_Filename'],
                'CV_Content_Normalized': tempCV,
            })
            db['CV_Content'].update_one({
                '_id': cvContent['_id']
            }, {"$set": {
                'CV_Normalized': True
            }})
            print("CV: " + i + ", normalized content has been inserted into database successfully.")

        # print("All CVs has been normalized successfully!")

        tempCV = ''

    # print("All CVs has been parsed successfully!")

    # for m, i in enumerate(parsedCVs):
    #     parsedCVs[m] = nltk.word_tokenize(parsedCVs[m])
    #     parsedCVs[m] = normalization(parsedCVs[m])
    #     parsedCVs[m] = ' '.join(map(str, parsedCVs[m]))

    # print("All CVs has been normalized successfully!")

    # print(parsedCVs)
    return parsedCVs
