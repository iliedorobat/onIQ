WHAT_IS_PAIRS = [
    {
        # [2]
        "query": "What is the population and area of the most populated state?",
        "result": """

"""
    }
]

WHICH_PAIRS = [
    {
        # [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome?",
        "result": """

"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer?",
        "result": """

"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer?",
        "result": """

"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome?",
        "result": """

"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?",
        "result": """

"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?",
        "result": """

"""
    },
    {
        # derived from [2]
        "query": "Which beautiful female is married to a writer born in Rome and has three children?",
        "result": """

"""
    }
]

WHICH_IS_PAIRS = [
    {
        # [2]
        "query": "Which is the longest and shortest river that traverses Mississippi?",
        "result": """

"""
    }
]

PAIRS_02 = WHAT_IS_PAIRS + \
           WHICH_PAIRS + \
           WHICH_IS_PAIRS
