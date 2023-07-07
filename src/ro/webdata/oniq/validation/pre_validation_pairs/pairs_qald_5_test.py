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
raw_triples = [
	<dbr:Arnold_Schwarzenegger   attend   ?university>
]
"""
    },
    {
        "aggregation": False,
        "answertype": bool,
        "hybrid": False,
        "onlydbo": True,
        "query": "Is Barack Obama a democrat?",
        "result": """
raw_triples = [
	<dbr:Barack_Obama   ?property   dbr:Democratic_Party_(United_States)>
]
"""
    },
#     {
#         # TODO: order by
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
raw_triples = [
	<dbr:Mecca   country   ?country>
]
"""
    },
    {
        # TODO: city => <?headquartered   rdf:type   dbo:City>
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": False,
        "query": "In which city is Air China headquartered?",
        "result": """
raw_triples = [
	<dbr:Air_China   headquartered   ?headquartered>
]
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": None,  # False??
        "onlydbo": True,
        "query": "Give me all ESA astronauts.",
        "result": """
raw_triples = [
	<?astronauts   ?property   dbr:European_Space_Agency>
]
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Give me all Swedish holidays.",
        "result": """
raw_triples = [
	<?Swedish_holidays   country   dbr:Sweden>
]
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Give me the currency of China.",
        "result": """
raw_triples = [
	<dbr:China   currency   ?currency>
]
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Give me all Swiss non-profit organizations.",
        "result": """
raw_triples = [
	<?profit_organizations   country   dbr:Switzerland>
]
"""
    },
    ### WHEN + aux verb ###
    {
        "aggregation": False,
        "answertype": "date",
        "hybrid": False,
        "onlydbo": True,
        "query": "When did the Ming dynasty dissolve?",
        "result": """
raw_triples = [
	<dbr:Ming_dynasty   dissolve   ?Ming_dynasty_dissolve>
]
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
raw_triples = [
	<dbr:Real_Madrid_CF   manager   ?manager>
]
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": False,
        "query": "Who is the mayor of Rotterdam?",
        "result": """
raw_triples = [
	<dbr:Rotterdam   mayor   ?mayor>
]
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who were the parents of Queen Victoria?",
        "result": """
raw_triples = [
	<dbr:Queen_Victoria   parents   ?parents>
]
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
# raw_triples = [
# 	<dbr:John_Lennon   killed   ?person>
# ]
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
raw_triples = [
	<?winner   winner   dbr:Pulitzer_Prize>
	<?winner   youngest   ?youngest>
]
"""
    },
    {
        # FIXME:
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who is the oldest child of Meryl Streep?",
        "result": """
raw_triples = [
	<dbr:Meryl_Streep   child   ?child>
	<?child   oldest   ?oldest>
]
"""
    },
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
raw_triples = [
	<?basketball_player   tallest   ?tallest>
]
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
raw_triples = [
	<dbr:Apple_Inc.   net_income   ?net_income>
]
"""
    },
    {
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "What is the highest mountain in Italy?",
        "result": """
raw_triples = [
	<?mountain   location   dbr:Italy>
	<?mountain   highest   ?highest>
]
"""
    },
#     {
#         # TODO: order by
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
raw_triples = [
	<dbr:Yokohama_Marine_Tower   high   ?high>
]
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
        "aggregation": False,
        "answertype": "number",
        "hybrid": False,
        "onlydbo": False,
        "query": "How many children does Eddie Murphy have?",
        "result": """
raw_triples = [
	<dbr:Eddie_Murphy   children   ?many_children>
]
"""
    },
    {
        "aggregation": True,
        "answertype": "number",
        "hybrid": False,
        "onlydbo": True,
        "query": "How many companies were founded by the founder of Facebook?",
        "result": """
raw_triples = [
	<?many_companies   founded   ?founder>
	<dbr:Facebook   founder   ?founder>
]
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
    {
        # FIXME: <dbr:Slovenia ethnic_groups ?ethnic_groups>
        # TODO: count
        "aggregation": True,
        "answertype": "number",
        "hybrid": False,
        "onlydbo": True,
        "query": "How many ethnic groups live in Slovenia?",
        "result": """
raw_triples = [
	<?ethnic_groups   live   dbr:Slovenia>
]
"""
    },
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
raw_triples = [
	<?soccer_players   born   dbr:Malta>
]
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
        # TODO: ?musician dbo:occupation dbr:Musician
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Which musician wrote the most books?",
        "result": """
raw_triples = [
	<?musician   wrote   ?books>
]
"""
    },
    {
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Which museum in New York has the most visitors?",
        "result": """
raw_triples = [
	<?museum   has   ?visitors>
	<?museum   location   dbr:New_York_City>
]
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
raw_triples = [
	<?volcanos   erupted   ?erupted>
	<?volcanos   location   dbr:Japan>
]
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
