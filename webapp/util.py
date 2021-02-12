from webapp import db
from webapp.db_models import Interestarea, Keyword
import re

#TODO TRIVIAL : student_details_id,company_details_id parameter name change as they are obj not str

def get_interest_from_db(i,company_details_id):
    db_instance = Interestarea.query.filter_by(name = i).first()
    if db_instance: #exist in db
        #check if that one already belongs to company, if so don't add again
        if company_details_id in db_instance.companydetails:
            return None
        return db_instance
    return Interestarea(name=i)

def get_keyword_from_db(i, student_details_id):
    db_instance = Keyword.query.filter_by(name = i).first()
    if db_instance: #exist in db
        #check if that one already belongs to company, if so don't add again
        if student_details_id in db_instance.studentdetails:
            return None
        return db_instance
    return Keyword(name=i)


def get_interests(interests_string,company_details_id):
    interests_array = interests_string.split(",")

    for index, i in enumerate(interests_array):
        i = i.lstrip()
        i = i.rstrip()
        interests_array[index] = i

    interest_objects = []

    for i in interests_array:
        if len(i) == 0:continue # do not count empty string
        obj = get_interest_from_db(i,company_details_id)
        if obj:
            interest_objects.append(obj)

    return interest_objects


def get_keywords(keyword_string,student_details_id):
    keywords_array = keyword_string.split(",")

    for index, i in enumerate(keywords_array):
        i = i.lstrip()
        i = i.rstrip()
        keywords_array[index] = i

    keywords_objects = []

    for i in keywords_array:
        if len(i) == 0:continue # do not count empty string
        obj = get_keyword_from_db(i,student_details_id)
        if obj:
            keywords_objects.append(obj)

    return keywords_objects


def get_business_keywords(user):
    ads = user.company_details.advertisements
    
    business_keywords = []
    for ad in ads:
        keys = ad.keywords
        if len(keys)>0:
            for key in keys:
                if key not in business_keywords:
                    business_keywords.append(key)


    if len(business_keywords) > 20:
        return business_keywords[0:20]
    elif len(business_keywords) == 0:
        return None
    else : return business_keywords


def is_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search( regex, email )):
        return True
    return False