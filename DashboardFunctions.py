from gensim.summarization import summarize
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

import ParseCVs


def start():
    # LoadCVs.loading_cvs()  # Start loading CVs names from their specific location
    ParseCVs.parse_cvs()  # Start parsing each CV

# start()


def ranking_cvs(jobDescription):
    cvsNames = []
    cvsVectorArray = []
    cvsScore = []

    Vectorizer = TfidfVectorizer(stop_words='english')

    dbClient = MongoClient('mongodb://localhost:27017/')
    db = dbClient['ACVAS']
    CVs = db['CV_Content_Normalized']

    result = []

    # noinspection PyBroadException
    try:
        jobDescriptionText = str(jobDescription)
        jobDescriptionText = summarize(jobDescriptionText, word_count=100)
        jobDescriptionText = [jobDescriptionText]
    except:
        jobDescriptionText = 'None'
    # print(jobDescriptionText)

    Vectorizer.fit(jobDescriptionText)
    # print(Vectorizer.fit(jobDescriptionText))

    jobDescriptionVector = Vectorizer.transform(jobDescriptionText)
    # print(jobDescriptionVector)

    jobDescriptionVectorArray = jobDescriptionVector.toarray()
    # print(jobDescriptionVectorArray)

    Cursor = CVs.find()
    for i in Cursor:
        cvsNames.append(i['CV_Filename'])

        # print(i['CV_Content_Normalized'])
        cv = str(i['CV_Content_Normalized'])
        # print(cv)

        # noinspection PyBroadException
        try:
            # cv = summarize(cv, word_count=100)

            cvText = [cv]
            # print(cvText)

            # Vectorizer.fit(cvText)  # I can't use Vectorizer.fit for a second time because it'll be incompatible
            # print(Vectorizer.fit(cvText))

            cvVector = Vectorizer.transform(cvText)
            # print(cvVector)

            cvsVectorArray.append(cvVector.toarray())
        except:
            print('Something went wrong while vectorizing CVs, but it will continue.')
            pass

    # print(cvsVectorArray)

    for i in cvsVectorArray:
        nNeighbors = NearestNeighbors(n_neighbors=1)
        # print(nNeighbors)
        nNeighbors.fit(i)
        # print(nNeighbors)
        # NearestNeighbors(algorithm='auto', leaf_size=30)  # These attributes set by default
        cvsScore.extend(nNeighbors.kneighbors(jobDescriptionVectorArray)[0][0].tolist())
    print(cvsScore)

    # print(cvNames)
    cvNameScore = [x for _, x in sorted(zip(cvsScore, cvsNames))]
    cvNameScore.reverse()
    # print(Z)
    for r, n in enumerate(cvNameScore):
        cvRank = r + 1
        cvName = fix_file_path(n)
        # print(cvName)
        # print(cvRank)
        resultElement = ResultElement(cvRank, cvName)
        result.append(resultElement)
        print(f"Rank{resultElement.rank} :\t {resultElement.filename}")

    return result


def fix_file_path(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp

class ResultElement:
    def __init__(self, rank, filename):
        self.rank = rank
        self.filename = filename



#job = """IT technicians diagnose computer problems, monitor computer processing systems, install software and perform tests on computer equipment and programs. Technicians may also set up computer equipment, schedule maintenance and  teach clients to use programs. Other job duties can include minor repairs and computer parts ordering. IT technicians need strong knowledge of computers and how they operate, which includes having a broad understanding of hardware and software, operating systems and basic computer programming. Familiarity with electronic equipment,  Internet applications and security may also be required. Technicians may also need good communication skills because this position requires frequent interaction with clients. Certification While not all companies require IT technicians to be certified, taking the extra step to earn a certification can show employers that technicians have the required skills and training to fulfill job requirements. Common certifications for IT technicians include A+ and Linux+ certifications offered by CompTIA. IT technicians can also pursue Microsoft Certified IT Professional and Cisco Certified Network Associate credentials. The International Information Systems Security Certification Consortium offers a variety of certifications for IT professionals pursuing information security positions. The certification process may include passing an exam and completing continuing education courses to maintain or renew credentials."""

#print(ranking_cvs(job))

#for r in flask_return:
#    print(r.rank)
#    print(r.filename)
