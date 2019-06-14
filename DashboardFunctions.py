from gensim.summarization import summarize
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier

# import ParseCVs


# def start():
    # LoadCVs.loading_cvs()  # Start loading CVs names from their specific location
#     ParseCVs.parse_cvs()  # Start parsing each CV

# start()
dbClient = MongoClient('mongodb://localhost:27017/')
db = dbClient['ACVAS']
CVs = db['CV_Content_Normalized']
Vectorizer = TfidfVectorizer(stop_words='english')


def ranking_cvs(jobDescription):
    cvsNames = []
    cvsVectorArray = []
    cvsScore = []



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
            print('Something went wrong while vectorizing CVs, but I will continue.')
            pass

    # print(cvsVectorArray)

    for i in cvsVectorArray:
        nNeighbors = NearestNeighbors(n_neighbors=1)
        # print(nNeighbors)
        nNeighbors.fit(i)
        # print(nNeighbors)
        # NearestNeighbors(algorithm='auto', leaf_size=30)  # These attributes set by default
        cvsScore.extend(nNeighbors.kneighbors(jobDescriptionVectorArray)[0][0].tolist())
    # print(cvsScore)
    # print(cvNames)

    cvNameScore = [x for _, x in sorted(zip(cvsScore, cvsNames))]
    cvNameScore.reverse()





    # print(Z)
    """
    for r, n in enumerate(cvNameScore):
        cvRank = r + 1
        cvName = fix_file_path(n)
        # print(cvName)
        # print(cvRank)
        resultElement = ResultElement(cvRank, cvName)
        result.append(resultElement)
        print(f"Rank{resultElement.rank} :\t {resultElement.filename}")
    """
    # print(Z)


    cvsNamesTop5 = []
    for r, n in enumerate(cvNameScore):
        cvsNamesTop5.append(n)
    cvsNamesTop5 = cvsNamesTop5[:5]
    # top5_ranking(cvsNamesTop5, jobDescriptionVectorArray)

    # return result
    return top5_ranking(cvsNamesTop5, jobDescriptionVectorArray)


def top5_ranking(top5CVs, jobDescriptionVectorArray):
    cvsVectorArrayTop5 = []
    cvsScoreTop5 = []
    # cvsNamesTop5 = []
    result = []
    # Cursor = CVs.find()
    # print(top5CVs[1])
    for i in range(5):
        cursor = CVs.find_one({'CV_Filename': top5CVs[i]})
        cv = str(cursor['CV_Content_Normalized'])
        # noinspection PyBroadException
        try:
            cvText = [cv]
            cvVector = Vectorizer.transform(cvText)
            cvsVectorArrayTop5.append(cvVector.toarray())
        except:
            print('Something went wrong while vectorizing CVs, but I will continue.')
            pass
    """
    for i in Cursor:
        if i['CV_Filename'] == top5CVs[j]:
            # top5CVs.append(i['CV_Filename'])
            cv = str(i['CV_Content_Normalized'])
            # noinspection PyBroadException
            try:
                cvText = [cv]
                cvVector = Vectorizer.transform(cvText)
                cvsVectorArrayTop5.append(cvVector.toarray())
            except:
                print('Something went wrong while vectorizing CVs, but I will continue.')
                pass
    """
    for i in cvsVectorArrayTop5:
        nNeighbors = NearestNeighbors(n_neighbors=1)
        nNeighbors.fit(i)
        cvsScoreTop5.extend(nNeighbors.kneighbors(jobDescriptionVectorArray)[0][0].tolist())

    cvNameScoreTop5 = [x for _, x in sorted(zip(cvsScoreTop5, top5CVs))]
    cvNameScoreTop5.reverse()

    for r, n in enumerate(cvNameScoreTop5):
        cvRank = r + 1
        cvName = fix_file_path(n)
        # print(cvName)
        # print(cvRank)
        resultElementTop5 = ResultElement(cvRank, cvName)
        result.append(resultElementTop5)
        print(f"Rankkk{resultElementTop5.rank} :\t {resultElementTop5.filename}")

    return result

def fix_file_path(loc):
    temp = str(loc)
    temp = temp.replace('\\', '/')
    return temp

class ResultElement:
    def __init__(self, rank, filename):
        self.rank = rank
        self.filename = filename



job = """
Assistant Manager - Finance
HONG KONG
________________________________________
Due to continued expansion across the group, we are recruiting for an Assistant Manager - Finance in our Hong Kong office.
________________________________________
Job purpose and overall objective
To assist the finance team in compliance with company standards, policies and procedures.
Main or key responsibilities
•	Supervise accounting team to oversee full set of accounts
•	Prepare monthly financial reports and management reporting pack with insightful analysis
•	Prepare balance sheet reconciliations, monitor and take follow up actions for the reconciling items
•	Monitor day to day cash flow and prepare cash flow forecast
•	Assist in budgeting and forecasting process
•	Support system implementation project
•	Liaise with different external parties such as auditors and banks
•	Participate in ad hoc projects assigned by senior management
•	Coordinate with the team on any ad hoc job or project the company has to undertake
•	Ensure compliance with company standards, policies and procedures
Essential experience and qualifications
•	Degree in accounting or related discipline 
•	HKICPA member or equivalent
•	Good experience of handling accounting entries and preparing a full set of accounts
•	At least five years’ experience in accounting preferably gained in a MNC, of which two years managing junior staff
•	Proficient in Microsoft Office (especially Word and Excel)
Desirable experience and qualifications
•	Knowledge in Microsoft Dynamics Navision would be an advantage
Personable attributes
•	Strong command of English (both verbal and written)
•	Able to meet deadlines and drive the team’s performance
•	Good team player who wants to work in an international environment
•	Assertive, approachable individual who can work under pressure
•	A self-motivated individual with a strong desire to deliver the best for the business
•	Possess excellent interpersonal skills
•	Be able to work proactively and collaboratively - as part of a team and individually
•	Be achievement focused whilst maintaining brand and business values
•	Possess a willingness to learn and share knowledge and skills with the business
•	Be proactive and enthusiastic and have excellent organisational skills and a methodical approach to dealing with a wide range of tasks


"""

# ranking_cvs(job)

#for r in flask_return:
#    print(r.rank)
#    print(r.filename)
