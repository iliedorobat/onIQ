PAIRS_QALD = [
    {
        "id": 1,
        "answertype": "resource",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "What is the alma mater of the chancellor of Germany Angela Merkel?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?alma_mater
WHERE {
	dbr:Angela_Merkel   dbo:almaMater   ?alma_mater
}
"""
    },
    {
        "id": 2,
        "answertype": "number",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": True,
        "query": "How large is the area of UK?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?area
WHERE {
	dbr:United_Kingdom   dbo:area   ?area
}
"""
    },
    {
        "id": 3,
        "answertype": "resource",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "Who is the author of the interpretation of dreams?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?author
WHERE {
	dbr:The_Interpretation_of_Dreams   dbo:author   ?author
}
"""
    },
    {
        "id": 4,
        "answertype": "string",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "What is the birth name of Adele?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?birth_name
WHERE {
	dbr:Adele   dbo:birthName   ?birth_name
}
"""
    },
    {
        "id": 6,
        "answertype": "number",
        "aggregation": True,
        "hybrid": False,
        "onlydbo": False,
        "query": "How many awards has Bertrand Russell?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT COUNT(?many_awards)
WHERE {
	dbr:Bertrand_Russell   dbp:awards   ?many_awards .
	?many_awards   rdf:type   dbo:Award
}
"""
    },
    {
        "id": 7,
        "answertype": "string",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "Who is Dan Jurafsky?",
        "result": """
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT *
WHERE {
	VALUES   ?Jurafsky   { dbr:Daniel_Jurafsky }
}
"""
    },
    {
        "id": 10,
        "answertype": "number",
        "aggregation": True,
        "hybrid": False,
        "onlydbo": False,
        "query": "how much is the elevation of Düsseldorf Airport ?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?elevation
WHERE {
	dbr:Düsseldorf_Airport   dbo:elevation   ?elevation
}
"""
    },
    {
        "id": 11,
        "answertype": "number",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": True,
        "query": "how much is the total population of  european union?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?total_population
WHERE {
	dbr:European_Union   dbo:populationTotal   ?total_population
}
"""
    },
#     {
#         # TODO: property not found
#         "id": 12,
#         "answertype": "number",
#         "aggregation": True,
#         "hybrid": False,
#         "onlydbo": True,
#         "query": "when was the founding date of french fifth republic?",
#         "result": """
# SELECT DISTINCT ?date
# WHERE {
# 	dbr:French_Fifth_Republic   dbp:dateFormat   ?date
# }
# """
#     },
    {
        "id": 13,
        "answertype": "string",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "Who are the founders of  BlaBlaCar?",
        "result": """
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?founders
WHERE {
	dbr:BlaBlaCar   dbp:founder   ?founders
}
"""
    },
    {
        "id": 16,
        "answertype": "resource",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "Where is the birthplace of Goethe?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?birthplace
WHERE {
	dbr:Johann_Wolfgang_von_Goethe   dbo:birthPlace   ?birthplace
}
"""
    },
    {
        "id": 17,
        "answertype": "string",
        "aggregation": True,
        "hybrid": False,
        "onlydbo": False,
        "query": "Where is the origin of Carolina reaper?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?origin
WHERE {
	dbr:Carolina_Reaper   dbo:origin   ?origin
}
"""
    },
    {
        "id": 18,
        "answertype": "number",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": True,
        "query": "How much is the population of Mexico City ?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?population
WHERE {
	dbr:Mexico_City   dbo:populationTotal   ?population
}
"""
    },
    {
        "id": 19,
        "answertype": "string",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "What is the nick name of Baghdad?",
        "result": """
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT DISTINCT ?nick_name
WHERE {
	dbr:Baghdad   foaf:nick   ?nick_name
}
"""
    },
    {
        "id": 22,
        "answertype": "string",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "How much is the population of Iraq?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?population
WHERE {
	dbr:Iraq   dbo:populationTotal   ?population
}
"""
    },
    {
        "id": 24,
        "answertype": "number",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": True,
        "query": "What is the population of Cairo?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?population
WHERE {
	dbr:Cairo   dbo:populationTotal   ?population
}
"""
    },
#     {
#         # FIXME: dbo:populationTotal => dbp:populationDensityRank
#         "id": 25,
#         "answertype": "number",
#         "aggregation": True,
#         "hybrid": False,
#         "onlydbo": False,
#         "query": "How much is the population density rank of Germany?",
#         "result": """
# SELECT DISTINCT ?population_density_rank
# WHERE {
# 	dbr:Germany   dbo:populationTotal   ?population_density_rank
# }
# """
#     },
    {
        "id": 27,
        "answertype": "number",
        "aggregation": True,
        "hybrid": False,
        "onlydbo": False,
        "query": "How large is the total area of North Rhine-Westphalia?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?total_area
WHERE {
	dbr:North_Rhine-Westphalia   dbo:areaTotal   ?total_area
}
"""
    },
    {
        "id": 31,
        "answertype": "date",
        "aggregation": True,
        "hybrid": False,
        "onlydbo": False,
        "query": "When was the death  of  Shakespeare?",
        "result": """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT DISTINCT ?death
WHERE {
	dbr:William_Shakespeare   dbo:deathDate   ?death
}
"""
    },
]
