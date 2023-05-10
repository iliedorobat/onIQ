# https://github.com/SmartDataAnalytics/ARCANA/blob/master/ARCANA%20Questions/Test_Data_Set/q4000.txt

# FIXME:
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
QUERY_08 = "What is the population and area of the most populated state?"
QUERY_09 = "Where is Fort Knox located?"
QUERY_10 = "Who is the builder of Atamurat-Kerkichi Bridge ?"
QUERY_11 = "What is the nationality of Aishath Saffa ?"
QUERY_12 = "What is the denomination of S. H. Kapadia ?"
QUERY_13 = "What is the city whose mayor is Anne Hidalgo?"
QUERY_14 = "What is the religion of the person who founded the Emel magazine?"
QUERY_15 = "Who is the spouse of Daniel Gibson? "
QUERY_17 = "Where was the designer of REP Parasol born?"
QUERY_18 = "What is the operator of SR class 3Sub ?"
TEST_3 = "Where was the person whose successor studied law born?"  # poss
TEST_5 = "What is the tallest building in Romania?"
TEST_6 = "Where was the person who won the oscar born?"
TEST_7 = "Who is the leader of the USA?"
TEST_8 = "Whose successor is Le Hong Phong?"


QUERY_0PAIRS = [
    {
        "query": QUERY_01,
        "result": """
[
	<?person   born   ?location>
	<?person   rdf:type   dbo:Person>
	<?person   successor   res:Le_Hong_Phong>
]
"""
    },
    {
        "query": QUERY_02,
        "result": """
[
	<?person   successor   res:Le_Hong_Phong>
]
"""
    },
    {
        "query": QUERY_03,
        "result": """
[
	<res:New_York_Times   published   ?location>
]
"""
    },
    {
        "query": QUERY_04,
        "result": """
[
	<?father   die   ?location>
	<res:Mashhur_bin_Abdulaziz_Al_Saud   father   ?father>
]
"""
    },
    {
        "query": QUERY_05,
        "result": """
[
	<?town   leader   ?leader>
	<?town   rdf:type   dbo:Town>
	<res:Myntdu_river   originates   ?town>
]
"""
    },
    {
        "query": QUERY_08,
        "result": """
[
	<?populated_state   population   ?population>
	<?populated_state   rdf:type   dbo:State>
]
"""
    },
    {
        "query": QUERY_09,
        "result": """
[
	<res:Fort_Knox   located   ?location>
]
"""
    },
    {
        "query": QUERY_10,
        "result": """
[
	<res:Kerkichi_Bridge   builder   ?builder>
]
"""
    },
    {
        "query": QUERY_11,
        "result": """
[
	<res:Aishath_Saffa   nationality   ?nationality>
]
"""
    },
    {
        "query": QUERY_12,
        "result": """
[
	<res:S._H._Kapadia   denomination   ?denomination>
]
"""
    },
    {
        "query": QUERY_13,
        "result": """
[
	<?city   mayor   res:Anne_Hidalgo>
]
"""
    },
    {
        "query": QUERY_14,
        "result": """
[
	<?person   religion   ?religion>
	<?person   rdf:type   dbo:Person>
	<res:Emel_magazine   founded   ?person>
]
"""
    },
    {
        "query": QUERY_15,
        "result": """
[
	<res:Daniel_Gibson   spouse   ?spouse>
]
"""
    },
    {
        "query": QUERY_17,
        "result": """
[
	<?designer   born   ?location>
	<?designer   designer   res:REP_Parasol>
]
"""
    },
    {
        "query": QUERY_18,
        "result": """
[
	<res:SR_class   operator   ?operator>
]
"""
    },
]

TEST_PAIRS = [
    {
        "query": TEST_3,
        "result": """
[
	<?person   location   ?location>
	<?person   successor   ?successor>
	<?successor   studied   ?law>
]
"""
    },
    {
        "query": TEST_5,
        "result": """
[
	<?building   location   res:Romania>
	<?building   rdf:type   dbo:Building>
]
"""
    },
    {
        "query": TEST_6,
        "result": """
[
	<?person   born   ?location>
	<?person   rdf:type   dbo:Person>
	<?person   won   ?oscar>
]
"""
    },
    {
        "query": TEST_7,
        "result": """
[
	<res:USA   leader   ?leader>
]
"""
    },
    {
        "query": TEST_8,
        "result": """
[
	<?person   successor   res:Le_Hong_Phong>
	<?person   rdf:type   dbo:Person>
]
"""
    },
]

PAIRS = QUERY_0PAIRS + TEST_PAIRS
