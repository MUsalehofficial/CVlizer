import PyPDF2
import textract
import os
import string
from nltk.tokenize import SpaceTokenizer
from nltk.tokenize import word_tokenize
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
                cwd = os.getcwd()
                # os.chdir('../CVs')
                print(cwd)
                a = textract.process(i)
                cwd = os.getcwd()
                # os.chdir('../CVs')
                print(cwd)
                a = a.replace(b'\n', b' ')
                a = a.replace(b'\r', b' ')
                b = str(a)
                c = [b]
                # print(c)
                parsedCVs.extend(c)
                print("This is a *.DOC file: ", i)
            except Exception as e:
                print(e)
    # This part for word tokenizing
    try:
        for m, i in enumerate(parsedCVs):
            print(word_tokenize(parsedCVs[m]))


    except Exception as error:

        print('Caught this error: ' + repr(error))


    # This part for joining again
    try:

        print(" ".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in parsedCVs]).strip())


    except Exception as error:

        print('Caught this error: ' + repr(error))



    print("All CVs has been parsed successfully!")
    # print(parsedCVs)
    return parsedCVs


parse_cvs()
