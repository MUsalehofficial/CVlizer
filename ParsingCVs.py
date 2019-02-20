import re
import unicodedata
import PyPDF2
import textract

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

import LoadCVs


def parse_cvs():
    parsedCVs = []
    orderedCVs = []
    # cvFileNames = []
    tempPDF = ''
    # LIST_OF_FILES = ['Professional-SRSs.docx','test.docx']

    for no, i in enumerate(LoadCVs.load_cvs()):
        orderedCVs.append(i)
        Temp = i.split(".")
        # print(no, i)

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
                parsedCVs.extend(c)
                print("This is a *.DOC file: ", i)
            except Exception as e:
                print(e)

    print("All CVs has been parsed successfully!")
    # print(parsedCVs)
    return parsedCVs


"""
def decode_unicode_chars(words):
    return unicodedata.normalize('NFD', words).encode('ascii', 'ignore')
"""


def decode_non_ascii(words):
    """Decode non-ASCII characters from a list of tokenized words"""
    new_words = []
    for w in words:
        nw = unicodedata.normalize('NFD', w).encode('ascii', 'ignore')
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


def lem_verbs(words):
    """Lemmatize verbs from a list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    new_words = []
    for word in words:
        new_word = lemmatizer.lemmatize(word, pos='v')
        #print(new_word)
        new_words.append(new_word)
        #print(new_words)
        #print(lemmatizer.lemmatize("cats"))
    return new_words


# aa = stem_words(['worked', 'played', 'running'])
# print(aa)

# p = decode_non_ascii(['ÈÀ', 'Æ', 'À'])
# print(p)
