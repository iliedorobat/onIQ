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
query_type = ASK
target_nouns = []
raw_triples = [
	<dbr:Arnold_Schwarzenegger   attend   ?university>
	<?university   rdf:type   dbo:University>
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
query_type = ASK
target_nouns = []
raw_triples = [
	<dbr:Barack_Obama   Is   dbr:democrat>
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
query_type = SELECT
target_nouns = [
	?country
]
raw_triples = [
	<dbr:Mecca   country   ?country>
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
query_type = SELECT
target_nouns = [
	?astronaut
]
raw_triples = [
	<?astronaut   rdf:type   dbo:Astronaut>
	<?astronaut   ?prop   dbr:ESA>
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
query_type = SELECT
target_nouns = [
	?holiday
]
raw_triples = [
	<?holiday   rdf:type   dbo:Holiday>
	<?holiday   country   dbr:Sweden>
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
query_type = SELECT
target_nouns = [
	?currency
]
raw_triples = [
	<dbr:China   currency   ?currency>
]
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
query_type = SELECT
target_nouns = [
	?time
]
raw_triples = [
	<dbr:Ming_dynasty   dissolve   ?time>
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
query_type = SELECT
target_nouns = [
	?manager
]
raw_triples = [
	<dbr:Real_Madrid   manager   ?manager>
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
query_type = SELECT
target_nouns = [
	?parents
]
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
query_type = SELECT
target_nouns = [
	?person
]
raw_triples = [
	<?person   rdf:type   dbo:Person>
	<?person   award   dbr:Pulitzer_Prize>
	<?person   youngest   ?youngest>
]
order_modifier = ASC
order_items = [
	?youngest
]
"""
    },
    {
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who is the oldest child of Meryl Streep?",
        "result": """
query_type = SELECT
target_nouns = [
	?child
]
raw_triples = [
	<dbr:Meryl_Streep   child   ?child>
	<?child   oldest   ?oldest>
]
order_modifier = DESC
order_items = [
	?oldest
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
query_type = SELECT
target_nouns = [
	?person
]
raw_triples = [
	<?person   rdf:type   dbo:BasketballPlayer>
	<?person   tallest   ?tallest>
]
order_modifier = DESC
order_items = [
	?tallest
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
query_type = SELECT
target_nouns = [
	?net_income
]
raw_triples = [
	<dbr:Apple_Inc\.   net_income   ?net_income>
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
query_type = SELECT
target_nouns = [
	?mountain
]
raw_triples = [
	<?mountain   locatedInArea   dbr:Italy>
	<?mountain   rdf:type   dbo:Mountain>
	<?mountain   highest   ?highest>
]
order_modifier = DESC
order_items = [
	?highest
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
#     {
#         "aggregation": False,
#         "answertype": "number",
#         "hybrid": False,  # True?? https://dbpedia.org/page/Yokohama_Marine_Tower
#         "onlydbo": True,
#         "query": "How high is the Yokohama Marine Tower?",
#         "result": """
# """
#     },
#     {
#         "aggregation": False,
#         "answertype": "number",
#         "hybrid": False, # True???
#         "onlydbo": True,
#         "query": "How many scientists graduated from an Ivy League university?",
#         "result": """
# """
#     },
#     {
#         "aggregation": True,
#         "answertype": "number",
#         "hybrid": False,
#         "onlydbo": True,
#         "query": "How many companies were founded by the founder of Facebook?",
#         "result": """
# """
#     },
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
query_type = COUNT
target_nouns = [
	?ethnic_groups
]
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
query_type = SELECT
target_nouns = [
	?soccer_players
]
raw_triples = [
	<?soccer_players   born   dbr:Malta>
	<?soccer_players   rdf:type   dbo:SoccerPlayer>
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
#     {
#         "aggregation": True,
#         "answertype": "resource",
#         "hybrid": False,
#         "onlydbo": True,
#         "query": "Which musician wrote the most books?",
#         "result": """
# """
#     },
    {
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Which museum in New York has the most visitors?",
        "result": """
query_type = SELECT
target_nouns = [
	?museum
]
raw_triples = [
	<?museum   location   dbr:New_York>
	<?museum   rdf:type   dbo:Museum>
	<?museum   visitors   ?visitors>
]
order_modifier = ASC
order_items = [
	?visitors
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
#     {
#         "aggregation": True,  # False??
#         "answertype": "resource",
#         "hybrid": False,
#         "onlydbo": True,
#         "query": "Which volcanos in Japan erupted since 2000?",
#         "result": """
# """
#     },
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
