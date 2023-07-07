PAIRS_QALD = [
    {
        "id": 1,
        "answertype": "resource",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "What is the alma mater of the chancellor of Germany Angela Merkel?",
        "result": """
raw_triples = [
	<dbr:Angela_Merkel   alma_mater   ?alma_mater>
]
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
raw_triples = [
	<dbr:United_Kingdom   area   ?area>
]
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
raw_triples = [
	<dbr:The_Interpretation_of_Dreams   author   ?author>
]
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
raw_triples = [
	<dbr:Adele   birth_name   ?birth_name>
]
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
raw_triples = [
	<dbr:Bertrand_Russell   awards   ?many_awards>
]
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
raw_triples = [
	<VALUES   ?Jurafsky   { dbr:Daniel_Jurafsky }>
]
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
raw_triples = [
	<dbr:Düsseldorf_Airport   elevation   ?elevation>
]
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
raw_triples = [
	<dbr:European_Union   total_population   ?total_population>
]
"""
    },
    {
        "id": 12,
        "answertype": "number",
        "aggregation": True,
        "hybrid": False,
        "onlydbo": True,
        "query": "when was the founding date of french fifth republic?",
        "result": """
raw_triples = [
	<dbr:French_Fifth_Republic   date   ?date>
]
"""
    },
    {
        "id": 13,
        "answertype": "string",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "Who are the founders of  BlaBlaCar?",
        "result": """
raw_triples = [
	<dbr:BlaBlaCar   founders   ?founders>
]
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
raw_triples = [
	<dbr:Johann_Wolfgang_von_Goethe   birthplace   ?birthplace>
]
"""
    },
    {
        "id": 17,
        "answertype": "string",
        "aggregation": True,
        "hybrid": False,
        "onlydbo": False,
        "query": "Where is the birthplace of Goethe?",
        "result": """
raw_triples = [
	<dbr:Carolina_Reaper   origin   ?origin>
]
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
raw_triples = [
	<dbr:Mexico_City   population   ?population>
]
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
raw_triples = [
	<dbr:Baghdad   nick_name   ?nick_name>
]
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
raw_triples = [
	<dbr:Iraq   population   ?population>
]
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
raw_triples = [
	<dbr:Cairo   population   ?population>
]
"""
    },
    {
        "id": 25,
        "answertype": "number",
        "aggregation": True,
        "hybrid": False,
        "onlydbo": False,
        "query": "What is the population of Cairo?",
        "result": """
raw_triples = [
	<dbr:Germany   population_density_rank   ?population_density_rank>
]
"""
    },
    {
        "id": 27,
        "answertype": "number",
        "aggregation": True,
        "hybrid": False,
        "onlydbo": False,
        "query": "How large is the total area of North Rhine-Westphalia?",
        "result": """
raw_triples = [
	<dbr:North_Rhine-Westphalia   total_area   ?total_area>
]
"""
    },
    {
        "id": 28,
        "answertype": "string",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": False,
        "query": "How large is the total area of North Rhine-Westphalia?",
        "result": """
raw_triples = [
	<dbr:The_Interpretation_of_Dreams   original_title   ?original_title>
]
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
raw_triples = [
	<dbr:William_Shakespeare   death   ?death>
]
"""
    },
    {
        "id": 37,
        "answertype": "string",
        "aggregation": False,
        "hybrid": False,
        "onlydbo": True,
        "query": "Who is the current federal minister of finance in Germany?",
        "result": """
raw_triples = [
	<dbr:Federal_Ministry_of_Finance_(Germany)   federal_minister   ?federal_minister>
]
"""
    },
]
