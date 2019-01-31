import glob
import os


def loading_cvs():
    os.chdir('CVs')
    # Listing PDF
    LIST_OF_FILES_PDF = []
    for file in glob.glob('**/*.pdf', recursive=True):
            LIST_OF_FILES_PDF.append(file)

    # Listing DOCX
    LIST_OF_FILES_DOCX = []
    for file in glob.glob('**/*.docx', recursive=True):
            LIST_OF_FILES_DOCX.append(file)

    # Listing DOC
    LIST_OF_FILES_DOC = []
    for file in glob.glob('**/*.doc', recursive=True):
            LIST_OF_FILES_DOC.append(file)

    # Listing All
    LIST_OF_FILES_ALL = LIST_OF_FILES_DOC + LIST_OF_FILES_DOCX + LIST_OF_FILES_PDF
    return LIST_OF_FILES_ALL
