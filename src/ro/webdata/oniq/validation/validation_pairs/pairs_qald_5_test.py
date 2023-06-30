# TODO: https://github.com/ag-sc/QALD/blob/master/8/data/qald-8-test-multilingual.json
# SOURCE: https://github.com/ag-sc/QALD/blob/master/5/data/qald-5_test.xml

PAIRS_QALD = [
    ### ASK (Aux verb + ...) ###
    #     {
    #         "aggregation": True,
    #         "answertype": bool,
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "Are there man-made lakes in Australia that are deeper than 100 meters?",
    #         "result": """
    # """
    #     },
    {
        "aggregation": False,
        "answertype": bool,
        "hybrid": False,
        "onlydbo": True,
        "query": "Did Arnold Schwarzenegger attend a university?",
        "result": """
ASK
WHERE {
	dbr:Arnold_Schwarzenegger   dbo:almaMater   ?university .
	?university   rdf:type   dbo:University
}
"""
    },
    {
        "aggregation": False,
        "answertype": bool,
        "hybrid": False,
        "onlydbo": True,
        "query": "Is Barack Obama a democrat?",
        "result": """
ASK
WHERE {
	dbr:Barack_Obama   ?property   dbr:Democratic_Party_(United_States)
}
"""
    },
    #     {
    #         "aggregation": False,
    #         "answertype": bool,
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Is Lake Baikal bigger than the Great Bear Lake?",
    #         "result": """
    # """
    #     },
    ### SELECTION ###
    #     {
    #         # FIXME:
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Desserts from which country contain fish?",
    #         "result": """
    # """
    #     },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "In which country is Mecca located?",
        "result": """
SELECT DISTINCT ?country
WHERE {
	dbr:Mecca   dbo:country   ?country .
	?country   rdf:type   dbo:Country
}
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": None,  # False??
        "onlydbo": True,
        "query": "Give me all ESA astronauts.",
        "result": """
SELECT DISTINCT ?astronauts
WHERE {
	?astronauts   ?property   dbr:European_Space_Agency .
	?astronauts   rdf:type   dbo:Astronaut
}
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Give me all Swedish holidays.",
        "result": """
SELECT DISTINCT ?Swedish_holidays
WHERE {
	?Swedish_holidays   dbo:country   dbr:Sweden .
	?Swedish_holidays   rdf:type   dbo:Holiday
}
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Give me the currency of China.",
        "result": """
SELECT DISTINCT ?currency
WHERE {
	dbr:China   dbo:currency   ?currency .
	?currency   rdf:type   dbo:Currency
}
"""
    },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Give me all Swiss non-profit organizations.",
    #         "result": """
    # """
    #     },
    ### WHEN + aux verb ###
    {
        "aggregation": False,
        "answertype": "date",
        "hybrid": False,
        "onlydbo": True,
        "query": "When did the Ming dynasty dissolve?",
        "result": """
SELECT DISTINCT ?Ming_dynasty_dissolve
WHERE {
	dbr:Ming_dynasty   dbp:dateEnd   ?Ming_dynasty_dissolve
}
"""
    },
    ### WHERE + aux verb ####
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "Where was the \"Father of Singapore\" born?",
    #         "result": """
    # """
    #     },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who is the manager of Real Madrid?",
        "result": """
SELECT DISTINCT ?manager
WHERE {
	dbr:Real_Madrid_CF   dbo:manager   ?manager
}
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who were the parents of Queen Victoria?",
        "result": """
SELECT DISTINCT ?parents
WHERE {
	dbr:Queen_Victoria   dbo:parent   ?parents
}
"""
    },
    ### WHO + verb ###
    #     {
    #         # FIXME: dbr:Death_of_John_Lennon instead of dbr:John_Lennon
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Who killed John Lennon?",
    #         "result": """
    # """
    #     },
    ### WHO + aux verb ###
    {
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who is the youngest Pulitzer Prize winner?",
        "result": """
SELECT DISTINCT ?winner
WHERE {
	?winner   dbo:award   dbr:Pulitzer_Prize .
	?winner   dbo:birthDate   ?youngest
}
ORDER BY DESC(?youngest)
"""
    },
    #     {
    #         # FIXME: <?child   prop   dbr:Meryl_Streep>
    #         "aggregation": True,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Who is the oldest child of Meryl Streep?",
    #         "result": """
    # SELECT DISTINCT ?child
    # WHERE {
    #     dbr:Meryl_Streep   ???   ?child .
    #     ?child   dbo:birthDate   ?oldest
    # }
    # ORDER BY ASC(?oldest)
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Who is starring in Spanish movies produced by Benicio del Toro?",
    #         "result": """
    # """
    #     },
    {
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who is the tallest basketball player?",
        "result": """
SELECT DISTINCT ?basketball_player
WHERE {
	?basketball_player   rdf:type   dbo:BasketballPlayer .
	?basketball_player   dbo:height   ?tallest
}
ORDER BY DESC(?tallest)
"""
    },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "Who is the architect of the tallest building in Japan?",
    #         "result": """
    # """
    #     },
    #     ### WHAT + aux verb ###
    {
        "aggregation": False,
        "answertype": "number",
        "hybrid": False,
        "onlydbo": True,
        "query": "What is the net income of Apple?",
        "result": """
SELECT DISTINCT ?net_income
WHERE {
	dbr:Apple_Inc.   dbo:netIncome   ?net_income
}
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "What is the highest mountain in Italy?",
        "result": """
SELECT DISTINCT ?mountain
WHERE {
	?mountain   dbo:locatedInArea   dbr:Italy .
	?mountain   rdf:type   dbo:Mountain .
	?mountain   dbo:elevation   ?highest
}
ORDER BY DESC(?highest)
"""
    },
    #     {
    #         "aggregation": True,
    #         "answertype": "number",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "What is the height difference between Mount Everest and K2?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "string",
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "What is the name of the Viennese newspaper founded by the creator of the croissant?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "string",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "What does the abbreviation FIFA stand for?",
    #         "result": """
    # """
    #     },
    ### HOW + acomp/amod ###
    {
        "aggregation": False,
        "answertype": "number",
        "hybrid": False,  # https://dbpedia.org/page/Yokohama_Marine_Tower
        "onlydbo": True,
        "query": "How high is the Yokohama Marine Tower?",
        "result": """
SELECT DISTINCT ?high
WHERE {
	dbr:Yokohama_Marine_Tower   dbo:height   ?high
}
ORDER BY DESC(?high)
"""
    },
    #     {
    #         "aggregation": False,
    #         "answertype": "number",
    #         "hybrid": False, # True???
    #         "onlydbo": True,
    #         "query": "How many scientists graduated from an Ivy League university?",
    #         "result": """
    # """
    #     },
    {
        "aggregation": True,
        "answertype": "number",
        "hybrid": False,
        "onlydbo": True,
        "query": "How many companies were founded by the founder of Facebook?",
        "result": """
SELECT DISTINCT COUNT(?many_companies)
WHERE {
	?many_companies   dbo:foundedBy   ?founder .
	dbr:Facebook   dbp:founder   ?founder .
	?many_companies   rdf:type   dbo:Company
}
"""
    },
    #     {
    #         "aggregation": True,
    #         "answertype": "number",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "How many companies were founded in the same year as Google?",
    #         "result": """
    # """
    #     },
    #     {
    #         # FIXME: <dbr:Slovenia ethnic_groups ?ethnic_groups>
    #         "aggregation": True,
    #         "answertype": "number",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "How many ethnic groups live in Slovenia?",
    #         "result": """
    # """
    #     },
    ### WHICH + noun ###
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Which animals are critically endangered?",
    #         "result": """
    # """
    #     },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Which soccer players were born on Malta?",
        "result": """
SELECT DISTINCT ?soccer_players
WHERE {
	?soccer_players   dbo:birthPlace   dbr:Malta .
	?soccer_players   rdf:type   dbo:SoccerPlayer
}
"""
    },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Which programming languages were influenced by Perl?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": True,  # False??
    #         "answertype": "date",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Which artists were born on the same date as Rachel Stevens?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Which types of grapes grow in Oregon?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Which movies starring Brad Pitt were directed by Guy Ritchie?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Which subsidiary of Lufthansa serves both Dortmund and Berlin Tegel?",
    #         "result": """
    # """
    #     },
    {
        #  <?musician   dbo:occupation   dbr:Musician>
        #  <?musician   dbo:author   ?books>
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Which musician wrote the most books?",
        "result": """
SELECT DISTINCT ?musician
WHERE {
	?books   rdf:type   dbo:Book .
	?musician   dbp:write   ?books
}
ORDER BY DESC(COUNT(?books))
"""
    },
    {
        # FIXME: dbo:numberOfVisitors instead of dbp:visitors
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Which museum in New York has the most visitors?",
        "result": """
SELECT DISTINCT ?museum
WHERE {
	?museum   dbo:location   dbr:New_York_City .
	?museum   rdf:type   dbo:Museum .
	?museum   dbp:visitors   ?visitors
}
ORDER BY DESC(COUNT(?visitors))
"""
    },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": False,
    #         "onlydbo": True,
    #         "query": "Which Greek parties are pro-European?",
    #         "result": """
    # """
    #     },
    {
        "aggregation": True,  # False??
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Which volcanos in Japan erupted since 2000?",
        "result": """
SELECT DISTINCT ?volcanos
WHERE {
	?volcanos   dbo:eruptionYear   ?erupted .
	?volcanos   dbo:locatedInArea   dbr:Japan .
	?volcanos   rdf:type   dbo:Volcano .
	FILTER (year(?erupted) >= 2000)
}
"""
    },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "Which Secretary of State was significantly involved in the United States' dominance of the Caribbean?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "In which city where Charlie Chaplin's half brothers born?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "Which German mathematicians were members of the von Braun rocket group?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "Which writers converted to Islam?",
    #         "result": """
    # """
    #     },
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "Which movie by the Coen brothers stars John Turturro in the role of a New York City playwright?",
    #         "result": """
    # """
    #     },
    ### WHICH + prep ###
    #     {
    #         "aggregation": False,
    #         "answertype": "resource",
    #         "hybrid": True,
    #         "onlydbo": True,
    #         "query": "Which of the volcanoes that erupted in 1550 is still active?",
    #         "result": """
    # """
    #     }
]
