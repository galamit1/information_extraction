import sys

import requests
import lxml.html
import re
import rdflib

LIST_OF_COUNTRIES_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
WIKIPEDIA_URL_PREFIX = "https://en.wikipedia.org"

ONTOLOGY_PREFIX = "http://example.org/"
ONTOLOGY_PATH = "ontology.nt"


def get_countries():
    response = requests.get(LIST_OF_COUNTRIES_URL)
    doc = lxml.html.fromstring(response.content)
    countries = doc.xpath("//table[1]//tr/td[1]//@href")
    return {get_name_from_url(country): str(country) for country in countries if str(country).startswith("/wiki")}


def create_ontology_entity(entity):
    return rdflib.URIRef(ONTOLOGY_PREFIX + entity)


def get_name_from_url(wiki_url):
    return wiki_url[wiki_url.rindex("/") + 1:]


def create_ontology():
    ontology_graph = rdflib.Graph()
    for country, country_url in get_countries().items():
        response = requests.get(WIKIPEDIA_URL_PREFIX + country_url)
        doc = lxml.html.fromstring(response.content)
        country_entity = create_ontology_entity(country)
        country_infobox = doc.xpath("//table[contains(./@class, 'infobox')]")
        if len(country_infobox) == 0:
            continue  # TODO: handle it

        country_infobox = country_infobox[0]
        president = country_infobox.xpath("//tr[th//a[text() = 'President']]/td//a/@href")
        if len(president) > 0:
            ontology_graph.add(
                (country_entity, create_ontology_entity("president_of"), create_ontology_entity(get_name_from_url(president[0]))))

    ontology_graph.serialize(ONTOLOGY_PATH, format="nt")


def answer_question(question):
    ontology_graph = rdflib.Graph()
    ontology_graph.parse(ONTOLOGY_PATH, format="nt")
    #TODO: continue


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] != "create":
            print("Wrong input!")
            return
        create_ontology()
        return

    if len(sys.argv) == 3:
        if sys.argv[1] != "question":
            print("Wrong input!")
            return
        answer_question(sys.argv[2])
        return

    print("Wrong input!")


if __name__ == '__main__':
    main()
