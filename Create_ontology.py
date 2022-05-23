import requests
import lxml.html
import rdflib
import re

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

# TODO: delete in the end
def dummy_create_ontology():
        ontology_graph = rdflib.Graph()
        response = requests.get(WIKIPEDIA_URL_PREFIX + "/wiki/Lesotho")
        doc = lxml.html.fromstring(response.content)
        country_infobox = doc.xpath("//table[contains(./@class, 'infobox')]")

        country_infobox = country_infobox[0]
        president = country_infobox.xpath("//tr[th//a[text() = 'Prime Minister']]/td//a/@href")
        country_entity = create_ontology_entity("Lesotho")

        curr_president = get_page(president[0])

        if curr_president != -1:
                president_when_born = curr_president.xpath("//table//tr[th[text()='Born']]//span[@class='bday']//text()")
                president_where_born = curr_president.xpath("//tr[th[contains(., 'Born')]]/td//text()")

                if len(president_when_born) > 0:
                     president_when_born = president_when_born[0]
                     date_entity = create_ontology_entity(president_when_born)
                     president_entity = create_ontology_entity("president_when_born")
                     ontology_graph.add(
                           (date_entity, president_entity, country_entity))

                if len(president_where_born) > 0:
                     president_country = [x for x in president_where_born if re.search('[a-zA-Z]', str(x))][-1]
                     president_country = "_".join(re.findall("[a-zA-Z]+", president_country))
                     president_entity = create_ontology_entity("president_where_born")
                     place_entity = create_ontology_entity(president_country)
                     ontology_graph.add(
                                       (place_entity, president_entity, country_entity))


        ontology_graph.serialize(ONTOLOGY_PATH, format="nt")

def get_page(url):
        response = requests.get(WIKIPEDIA_URL_PREFIX + url)
        doc = lxml.html.fromstring(response.content)
        country_infobox = doc.xpath("//table[contains(./@class, 'infobox')]")
        if len(country_infobox) == 0:
            return -1

        return country_infobox[0]


def create_ontology():
    ontology_graph = rdflib.Graph()
    for country, country_url in get_countries().items():
        country_infobox = get_page(country_url)
        if country_infobox == -1:
            continue
        president = country_infobox.xpath("//tr[th//a[text() = 'President']]/td//a/@href")
        prime_minister = country_infobox.xpath("//tr[th//a[text() = 'Prime Minister']]/td//a/@href")
        population = country_infobox.xpath("//tr[th[contains(., 'census')]]/td//text()")
        area = country_infobox.xpath("//tr[th[contains(., 'Total')]]/td//text()")
        gov = country_infobox.xpath("//tr[th[contains(., 'Government')]]/td//a/@href")
        capital = country_infobox.xpath("//tr[th[contains(., 'Capital')]]/td//a/@href")



        #if population == 0:
            # TODO: fix this option
        #    population = country_infobox.xpath("//tr[th[contains(., 'estimate')]]/td//text()")
        country_entity = create_ontology_entity(country)

        if len(president) > 0:
            name_entity = create_ontology_entity(get_name_from_url(president[0]))
            president_entity = create_ontology_entity("president_of")
            ontology_graph.add(
                (name_entity, president_entity, country_entity))

            curr_president = get_page(president[0])

            if curr_president != -1:
                    president_when_born = curr_president.xpath("//table//tr[th[text()='Born']]//span[@class='bday']//text()")
                    president_where_born = curr_president.xpath("//tr[th[contains(., 'Born')]]/td//text()")

                    if len(president_when_born) > 0:
                         president_when_born = president_when_born[0]
                         date_entity = create_ontology_entity(president_when_born)
                         president_entity = create_ontology_entity("president_when_born")
                         ontology_graph.add(
                               (date_entity, president_entity, country_entity))

                    if len(president_where_born) > 0:
                         president_country = [x for x in president_where_born if re.search('[a-zA-Z]', str(x))][-1]
                         president_country = "_".join(re.findall("[a-zA-Z]+", president_country))
                         president_entity = create_ontology_entity("president_where_born")
                         place_entity = create_ontology_entity(president_country)
                         ontology_graph.add(
                                           (place_entity, president_entity, country_entity))



        if len(prime_minister) > 0:
            name_entity = create_ontology_entity(get_name_from_url(prime_minister[0]))
            prime_minister_entity = create_ontology_entity("prime_minister_of")
            ontology_graph.add(
                (name_entity, prime_minister_entity, country_entity))

            curr_prime = get_page(prime_minister[0])

            if curr_prime != -1:
                    prime_when_born = curr_prime.xpath("//table//tr[th[text()='Born']]//span[@class='bday']//text()")
                    prime_where_born = curr_prime.xpath("//tr[th[contains(., 'Born')]]/td//text()")

                    if len(prime_when_born) > 0:
                         prime_when_born = prime_when_born[0]
                         date_entity = create_ontology_entity(prime_when_born)
                         prime_entity = create_ontology_entity("prime_when_born")
                         ontology_graph.add(
                               (date_entity, prime_entity, country_entity))

                    if len(prime_where_born) > 0:
                         prime_country = [x for x in prime_where_born if re.search('[a-zA-Z]', str(x))][-1]
                         prime_country = "_".join(re.findall("[a-zA-Z]+", prime_country))
                         prime_entity = create_ontology_entity("president_where_born")
                         place_entity = create_ontology_entity(prime_country)
                         ontology_graph.add(
                                           (place_entity, prime_entity, country_entity))

        if len(population) > 0:
           entity = (population[0]).split(" ")[-1]
           name_entity = create_ontology_entity(entity)
           population_entity = create_ontology_entity("population_of")
           ontology_graph.add(
                (name_entity, population_entity, country_entity))
        
        if len(area) > 0:
           area = area[0]
           area = (area.split(' '))[0]
           area = (area.split("\xa0"))
           area = "_".join(area)

           name_entity = create_ontology_entity((area))
           area_entity = create_ontology_entity("area_of")
           ontology_graph.add(
                (name_entity, area_entity, country_entity))
        
        if len(gov) > 0:
           for i in gov:
               name_entity = create_ontology_entity(i)
               gov_entity = create_ontology_entity("government_in")
               ontology_graph.add(
                    (name_entity, gov_entity, country_entity))
        
        if len(capital) > 0:
               name_entity = create_ontology_entity(capital[0])
               capital_entity = create_ontology_entity("capital_of")
               ontology_graph.add(
                    (name_entity, capital_entity, country_entity))

    ontology_graph.serialize(ONTOLOGY_PATH, format="nt")


