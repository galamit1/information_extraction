import rdflib
from Create_ontology import *
import re
import copy

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
    if question_type != "How" and question_type != "List":
         if re.search("Who is", question):
             q = broad_question(question, g)
         else:
             q = specific_question(question)
    else:
        q = broad_question(question, g)

    query_result = g.query(q)
    answer_for_question = get_final_result(query_result)

    if re.search("area", question):
        answer_for_question += " squared"

    if re.search("Who is", question):
        if re.search("president", q):
            answer_for_question = "President of " + answer_for_question
        else:
            answer_for_question = "Prime minister of " + answer_for_question
    if re.search("How", question):
        answer_for_question = len(query_result)
    print(answer_for_question)
    return answer_for_question



def get_final_result(query_result):

    results = [' '.join((((str(entity[0])).split("/"))[-1]).split('_'))
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


def broad_question(question, g):
    if re.search("List", question):
            name = (question.split("?")[0]).split(" ")
            name = "_".join(name[9:])
    # TODO: slice the str(?e)
            q = "select * where { ?e" + " <" + ONTOLOGY_PREFIX+"capital_of> ?x. "  + " FILTER(regex(lcase(str(?e))," + "\"" + str(name).lower() + "\"" + "))}"

    if re.search("Who", question):
       name = (question.split("?")[0]).split(" ")
       name = "_".join(name[2:])
       q = "select * where { <" + ONTOLOGY_PREFIX+name + ">" + " <" + ONTOLOGY_PREFIX + "president_of> ?x }"
       if not g.query(q):
         q = "select * where { <" + ONTOLOGY_PREFIX+name + ">" + " <" + ONTOLOGY_PREFIX + "prime_minister_of> ?x }"

    if re.search("also", question):
         name1, name2 = question.split("are also")
         name1 = (name1.split("?")[0]).split()
         name1 = "_".join(name1[2:])
         name2 = (name2.split("?")[0]).split()
         name2 = "_".join(name2)
         q = "select * where {  <" + ONTOLOGY_PREFIX+'/wiki/'+name1 + "> <http://example.org/government_in> ?x. " \
             + "  <" + ONTOLOGY_PREFIX+'/wiki/'+name2+ "> <http://example.org/government_in> ?x. }"

    else:
        if re.search("How", question):
            name = (question.split("?")[0]).split(" ")
            name = "_".join(name[6:])
            q = "select * where { ?e" + " <" + ONTOLOGY_PREFIX+"president_where_born>" + " "
            + " <" + ONTOLOGY_PREFIX+name + "> . }"

    return q

