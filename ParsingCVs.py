import PyPDF2
import textract

import LoadCVs


def parse_cvs():
    parsedCVs = []
    orderedCVs = []
    # tempPDF = []
    # LIST_OF_FILES = ['Professional-SRSs.docx','test.docx']

    for no, i in enumerate(LoadCVs.loading_cvs()):
        orderedCVs.append(i)
        Temp = i.split(".")

        if Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            print("This is a *.DOCX file: ", i)
            try:
                a = textract.process(i)
                a = a.replace(b'\n', b' ')
                a = a.replace(b'\r', b' ')
                b = str(a)
                c = [b]
                parsedCVs.extend(c)
            except Exception as e:
                print(e)

        if Temp[1] == "doc" or Temp[1] == "Doc" or Temp[1] == "DOC":
            print("This is a *.DOC file: ", i)
            try:
                a = textract.process(i)
                a = a.replace(b'\n', b' ')
                a = a.replace(b'\r', b' ')
                b = str(a)
                c = [b]
                parsedCVs.extend(c)
            except Exception as e:
                print(e)

        if Temp[1] == "pdf" or Temp[1] == "Pdf" or Temp[1] == "PDF":
            try:
                print("This is a *.PDF file:", i)
                with open(i, 'rb') as pdf_file:
                    read_pdf = PyPDF2.PdfFileReader(pdf_file)
                    number_of_pages = read_pdf.getNumPages()
                    for page_number in range(number_of_pages):
                        page = read_pdf.getPage(page_number)
                        page_content = page.extractText()
                        page_content = page_content.replace('\n', ' ')
                        # page_content.replace("\r", "")
                        tempPDF = str(tempPDF) + str(page_content)
                        # Temp_pdf.append(page_content)
                        # print(Temp_pdf)
                    parsedCVs.extend([tempPDF])
                    tempPDF = ''

            except Exception as e:
                print(e)
    print("Parsing finished!")
    # print(parsedCVs)

# parse_cvs()
