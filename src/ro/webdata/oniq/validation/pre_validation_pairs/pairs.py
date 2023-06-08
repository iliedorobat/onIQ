# https://github.com/SmartDataAnalytics/ARCANA/blob/master/ARCANA%20Questions/Test_Data_Set/q4000.txt

# FIXME:
QUERY_08 = "What is the population and area of the most populated state?"
QUERY_06 = "Where did William Jones from the British Raj die?"  # NER
QUERY_07 = "Which is the longest river that flows through the states neighbouring Mississippi?"
TEST_1 = "Where does Shirley Chisholm work that is bordered by Arlington County?"  # TODO: work - is a NOUN!?!?!
TEST_2 = "Where is the National Bank of Romania located?"  # "National Bank of Romania" is not identified as being an named entity
TEST_4 = "How many paintings are on display at the Amsterdam Museum?"
QUERY_16 = "What is the common party of the Manthena Venkata Raju and  B. Shiva Rao?"

QUERY_01 = "Where was the person born whose successor was Le Hong Phong?"
QUERY_02 = "Who is the person whose successor was Le Hong Phong?"  # poss
QUERY_03 = "Where is the New York Times published?"
QUERY_04 = "Where did Mashhur bin Abdulaziz Al Saud's father die?"
QUERY_05 = "Who is the leader of the town where the Myntdu river originates?"
QUERY_09 = "Where is Fort Knox located?"
QUERY_10 = "Who is the builder of Atamurat-Kerkichi Bridge ?"
QUERY_11 = "What is the nationality of Aishath Saffa ?"
QUERY_12 = "What is the denomination of S. H. Kapadia ?"
QUERY_13 = "What is the city whose mayor is Anne Hidalgo?"
QUERY_14 = "What is the religion of the person who founded the Emel magazine?"
QUERY_15 = "Who is the spouse of Daniel Gibson? "
QUERY_17 = "Where was the designer of REP Parasol born?"
QUERY_18 = "What is the operator of SR class 3Sub ?"
QUERY_19 = "Which species does an elephant belong?"
QUERY_20 = "What is the highest mountain in the Bavarian Alps?"
QUERY_21 = "What is the largest city in america?"
TEST_3 = "Where was the person whose successor studied law born?"  # poss
TEST_5 = "What is the tallest building in Romania?"
TEST_6 = "Where was the person who won the oscar born?"
TEST_7 = "Who is the leader of the USA?"
TEST_8 = "Whose successor is Le Hong Phong?"


QUERY_0PAIRS = [
    {
        "query": QUERY_01,
        "result": """
query_type = SELECT
target_nouns = [
	?location
]
raw_triples = [
	<?person   born   ?location>
	<?person   rdf:type   dbo:Person>
	<?person   successor   dbr:Le_Hong_Phong>
]
"""
    },
    {
        "query": QUERY_02,
        "result": """
query_type = SELECT
target_nouns = [
	?person
]
raw_triples = [
	<?person   successor   dbr:Le_Hong_Phong>
]
"""
    },
    {
        "query": QUERY_03,
        "result": """
query_type = SELECT
target_nouns = [
	?location
]
raw_triples = [
	<dbr:New_York_Times   published   ?location>
]
"""
    },
    {
        "query": QUERY_04,
        "result": """
query_type = SELECT
target_nouns = [
	?location
]
raw_triples = [
	<?father   die   ?location>
	<dbr:Mashhur_bin_Abdulaziz_Al_Saud   father   ?father>
]
"""
    },
    {
        # TODO: check with QUERY_14
        "query": QUERY_05,
        "result": """
query_type = SELECT
target_nouns = [
	?leader
]
raw_triples = [
	<?town   leader   ?leader>
	<?town   rdf:type   dbo:Town>
	<dbr:Myntdu_river   originates   ?town>
]
"""
    },
#     {
#         # TODO: order by
#         # TODO: and area
#         "query": QUERY_08,
#         "result": """
# query_type = SELECT
# target_nouns = [
# 	?population
# ]
# raw_triples = [
# 	<?populated_state   population   ?population>
# 	<?populated_state   rdf:type   dbo:State>
# ]
# """
#     },
    {
        "query": QUERY_09,
        "result": """
query_type = SELECT
target_nouns = [
	?location
]
raw_triples = [
	<dbr:Fort_Knox   located   ?location>
]
"""
    },
    {
        "query": QUERY_10,
        "result": """
query_type = SELECT
target_nouns = [
	?builder
]
raw_triples = [
	<dbr:Kerkichi_Bridge   builder   ?builder>
]
"""
    },
    {
        "query": QUERY_11,
        "result": """
query_type = SELECT
target_nouns = [
	?nationality
]
raw_triples = [
	<dbr:Aishath_Saffa   nationality   ?nationality>
]
"""
    },
    {
        "query": QUERY_12,
        "result": """
query_type = SELECT
target_nouns = [
	?denomination
]
raw_triples = [
	<dbr:S._H._Kapadia   denomination   ?denomination>
]
"""
    },
    {
        "query": QUERY_13,
        "result": """
query_type = SELECT
target_nouns = [
	?city
]
raw_triples = [
	<?city   mayor   dbr:Anne_Hidalgo>
]
"""
    },
    {
        "query": QUERY_14,
        "result": """
query_type = SELECT
target_nouns = [
	?religion
]
raw_triples = [
	<?person   religion   ?religion>
	<?person   rdf:type   dbo:Person>
	<dbr:Emel_magazine   founded   ?person>
]
"""
    },
    {
        "query": QUERY_15,
        "result": """
query_type = SELECT
target_nouns = [
	?spouse
]
raw_triples = [
	<dbr:Daniel_Gibson   spouse   ?spouse>
]
"""
    },
    {
        "query": QUERY_17,
        "result": """
query_type = SELECT
target_nouns = [
	?location
]
raw_triples = [
	<?designer   born   ?location>
	<?designer   designer   dbr:REP_Parasol>
]
"""
    },
    {
        # TODO: SR class 3Sub
        "query": QUERY_18,
        "result": """
query_type = SELECT
target_nouns = [
	?operator
]
raw_triples = [
	<dbr:SR_class   operator   ?operator>
]
"""
    },
    {
        "query": QUERY_19,
        "result": """
query_type = SELECT
target_nouns = [
	?elephant
]
raw_triples = [
	<?elephant   belong   ?thing>
]
"""
    },
    {
        "query": QUERY_20,
        "result": """
query_type = SELECT
target_nouns = [
	?mountain
]
raw_triples = [
	<?mountain   locatedInArea   dbr:Bavarian_Alps>
	<?mountain   rdf:type   dbo:Mountain>
	<?mountain   highest   ?highest>
]
order_modifier = DESC
order_items = [
	?highest
]
"""
    },
    {
        "query": QUERY_21,
        "result": """
query_type = SELECT
target_nouns = [
	?city
]
raw_triples = [
	<?city   location   dbr:america>
	<?city   rdf:type   dbo:City>
	<?city   largest   ?largest>
]
order_modifier = DESC
order_items = [
	?largest
]
"""
    },
]

TEST_PAIRS = raw_triples = [
    {
        "query": TEST_3,
        "result": """
query_type = SELECT
target_nouns = [
	?location
]
raw_triples = [
	<?person   location   ?location>
	<?person   successor   ?successor>
	<?successor   studied   ?law>
]
"""
    },
    {
        "query": TEST_5,
        "result": """
query_type = SELECT
target_nouns = [
	?building
]
raw_triples = [
	<?building   location   dbr:Romania>
	<?building   rdf:type   dbo:Building>
	<?building   tallest   ?tallest>
]
order_modifier = DESC
order_items = [
	?tallest
]
"""
    },
    {
        "query": TEST_6,
        "result": """
query_type = SELECT
target_nouns = [
	?location
]
raw_triples = [
	<?person   born   ?location>
	<?person   rdf:type   dbo:Person>
	<?person   won   ?oscar>
]
"""
    },
    {
        "query": TEST_7,
        "result": """
query_type = SELECT
target_nouns = [
	?leader
]
raw_triples = [
	<dbr:USA   leader   ?leader>
]
"""
    },
    {
        "query": TEST_8,
        "result": """
query_type = SELECT
target_nouns = [
	?person
]
raw_triples = [
	<?person   successor   dbr:Le_Hong_Phong>
	<?person   rdf:type   dbo:Person>
]
"""
    },
]

PAIRS = QUERY_0PAIRS + TEST_PAIRS
