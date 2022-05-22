import rdflib
from Create_ontology import *
import re

LIST_OF_COUNTRIES_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
WIKIPEDIA_URL_PREFIX = "https://en.wikipedia.org"
ONTOLOGY_PREFIX = "http://example.org/"
ONTOLOGY_PATH = "ontology.nt"


def answer_question(question):
     # TODO: input validity
    g = rdflib.Graph()
    g.parse("ontology.nt")

    question = str(question)
    question_type = str(((question.split()))[0])
    if question_type != "How" or question_type != "List":
         if re.search("Who is", question):
             q = broad_question(question)
         else:
             q = specific_question(question)
    else:
        q = broad_question(question)

    query_result = g.query(q)
    answer_for_question = get_final_result(query_result)
    if re.search("area", question):
        answer_for_question += " squared"
    print(answer_for_question)
    return answer_for_question



def get_final_result(query_result):
    results = [' '.join((((entity[0]).split("/"))[-1]).split('_'))
               for entity in tuple(query_result)]
    final_string = ', '.join(results)
    return final_string


def specific_question(question):
    # TODO: dont forget slice all
    country = question.split()[-1].split("?")
    country = country[:-1]
    country = "_".join(country)

    if re.search("president", question):
        attribute = "president_of>"


    if re.search("prime", question):
        attribute = "prime_minister_of>"

    if re.search("population", question):
        country = (question.split("?")[0]).split(" ")
        country = "_".join(country[5: ])
        attribute = "population_of>"


    if re.search("area", question):
        country = (question.split("?")[0]).split(" ")
        country = "_".join(country[5: ])
        attribute = "area_of>"


    if re.search("government", question):
        country = (question.split("?")[0]).split(" ")
        country = "_".join(country[7: ])
        attribute = "government_in>"


    if re.search("capital", question):
        country = (question.split("?")[0]).split(" ")
        country = "_".join(country[5: ])
        attribute = "capital_of>"

    if re.search("born", question):
        if re.search("president", question):
            if re.search("When", question):
                 country = (question.split("?")[0]).split(" ")
                 country = "_".join(country[5: -1])
                 attribute = "president_when_born>"
            if re.search("Where", question):
                  country = (question.split("?")[0]).split(" ")
                  country = "_".join(country[5: -1])
                  attribute = "president_where_born>"
        else:
            if re.search("When", question):
                 country = (question.split("?")[0]).split(" ")
                 country = "_".join(country[5: -1])
                 attribute = "prime_when_born>"
            if re.search("Where", question):
                  country = (question.split("?")[0]).split(" ")
                  country = "_".join(country[5: -1])
                  attribute = "prime_where_born>"


    q = "select ?e where { ?e" + " <" + ONTOLOGY_PREFIX+attribute + " "  + " <" + ONTOLOGY_PREFIX+country + "> . }"
    return q


def broad_question(question):
    if re.search("Who", question):
       name = (question.split("?")[0]).split(" ")
       name = "_".join(name[2:])
       q = "select ?e ?c where { ?e" + " <" + ONTOLOGY_PREFIX+name + "> ?c " +"}"


    return q


