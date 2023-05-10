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
[
	<res:Arnold_Schwarzenegger   attend   ?university>
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
[
	<res:Barack_Obama   Is   res:democrat>
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
[
	<res:Mecca   country   ?country>
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
[
	<?astronaut   rdf:type   dbo:Astronaut>
	<?astronaut   prop   res:ESA>
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
[
	<?holiday   rdf:type   dbo:Holiday>
	<?holiday   country   res:Sweden>
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
[
	<res:China   currency   ?currency>
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
[
	<res:Ming_dynasty   dissolve   ?time>
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
[
	<res:Real_Madrid   manager   ?manager>
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
[
	<res:Queen_Victoria   parents   ?parents>
]
"""
    },
    ### WHO + verb ###
#     {
#         # FIXME: res:Death_of_John_Lennon instead of res:John_Lennon
#         "aggregation": False,
#         "answertype": "resource",
#         "hybrid": False,
#         "onlydbo": True,
#         "query": "Who killed John Lennon?",
#         "result": """
# [
# 	<res:John_Lennon   killed   ?person>
# ]
# """
#     },
    ### WHO + aux verb ###
    {
        # TODO: order by birth date
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who is the youngest Pulitzer Prize winner?",
        "result": """
[
	<?person   winner   res:Pulitzer_Prize>
	<?person   rdf:type   dbo:Person>
]
"""
    },
    {
        # TODO: order by birth date
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who is the oldest child of Meryl Streep?",
        "result": """
[
	<res:Meryl_Streep   child   ?child>
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
        # TODO: order by height
        "aggregation": True,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "Who is the tallest basketball player?",
        "result": """
[
	<?person   rdf:type   dbo:BasketballPlayer>
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
[
	<res:Apple_Inc.   net_income   ?net_income>
]
"""
    },
    {
        # TODO: order by elevation
        "aggregation": False,
        "answertype": "resource",
        "hybrid": False,
        "onlydbo": True,
        "query": "What is the highest mountain in Italy?",
        "result": """
[
	<?mountain   location   res:Italy>
	<?mountain   rdf:type   dbo:Mountain>
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
        # FIXME: <res:Slovenia ethnic_groups ?ethnic_groups>
        # TODO: count
        "aggregation": True,
        "answertype": "number",
        "hybrid": False,
        "onlydbo": True,
        "query": "How many ethnic groups live in Slovenia?",
        "result": """
[
	<?ethnic_groups   live   res:Slovenia>
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
[
	<?players   born   res:Malta>
	<?players   rdf:type   dbo:SoccerPlayer>
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
[
	<?museum   location   res:New_York>
	<?museum   rdf:type   dbo:Museum>
	<?museum   visitors   ?visitors>
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
