import glob
import os


# TODO: Please check this error there, when you comment this it works well in parsing
# TODO: but in sending application it throws an error!!!
os.chdir('./CVs')


def load_cvs():
    # Listing PDF
    PDFs = []
    for file in glob.glob("**/*.pdf", recursive=True):
        PDFs.append(file)

    # Listing DOCX
    DOCXs = []
    for file in glob.glob("**/*.docx", recursive=True):
        DOCXs.append(file)

    # Listing DOC
    DOCs = []
    for file in glob.glob("**/*.doc", recursive=True):
        DOCs.append(file)

    # Listing All
    ALL = PDFs + DOCXs + DOCs
    print("All CVs has been loaded successfully!")
    return ALL

# cvList = load_cvs()
