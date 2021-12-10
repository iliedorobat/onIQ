WHICH_PAIRS_01 = [
    {
        "query": "Which smart kid is famous?",
        "result": """
statement: {
	target: {
		phrase: which smart kid
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: famous
		question type: None
	}
}
"""
    },
    {
        "query": "Which of the smart kids are famous?",
        "result": """
statement: {
	target: {
		phrase: which of the smart kids
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: famous
		question type: None
	}
}
"""
    },
    {
        "query": "Which of the paintings is the most beautiful?",
        "result": """
statement: {
	target: {
		phrase: which of the paintings
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: the most beautiful
		question type: None
	}
}
"""
    },
    {
        "query": "Which paintings located in Bacau are in good shape?",
        "result": """
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: located,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in good shape
		question type: None
	}
}
"""
    },
    {
        "query": "Which paintings, swords or statues are in Bacau?",
        "result": """
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which swords
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which statues
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "Which paintings, swords, coins or statues are in Bacau?",
        "result": """
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which swords
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which coins
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which statues
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "Which paintings, swords, coins or statues are in Bacau or Bucharest?",
        "result": """
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##or## in Bucharest
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which swords
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which swords
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##or## in Bucharest
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which coins
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which coins
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##or## in Bucharest
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which statues
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which statues
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##or## in Bucharest
		question type: None
	}
}
"""
    },
    {
        "query": "Which museum hosts more than 10 pictures and exposed one sword?",
        "result": """
statement: {
	target: {
		phrase: which museum
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		}
	},
	related: {
		phrase: more than 10 pictures
		question type: None
	}
}
statement: {
	target: {
		phrase: which museum
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		}
	},
	related: {
		phrase: one sword
		question type: None
	}
}
"""
    },
    {
        "query": "Which painting has not been deposited in Bacau?",
        "result": """
statement: {
	target: {
		phrase: which painting
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: deposited,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "Which paintings and statues have not been deposited in Bacau?",
        "result": """
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## which statues
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "Which paintings, swords and statues have not been deposited in Bacau?",
        "result": """
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## which swords
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## which statues
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "Which paintings, sharp swords and tall statues have not been deposited in Bacau?",
        "result": """
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## which sharp swords
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## which tall statues
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		}
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "Which paintings do not have more than three owners?",
        "result": """
statement: {
	target: {
		phrase: which paintings
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [do],
			main_vb: have,
			modal_vb: None
		}
	},
	related: {
		phrase: more than three owners
		question type: None
	}
}
"""
    },
    {
        "query": "Which painting, sharp swords or statues do not have more than three owners?",
        "result": """
statement: {
	target: {
		phrase: which painting
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [do],
			main_vb: have,
			modal_vb: None
		}
	},
	related: {
		phrase: more than three owners
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which sharp swords
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [do],
			main_vb: have,
			modal_vb: None
		}
	},
	related: {
		phrase: more than three owners
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## which statues
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [do],
			main_vb: have,
			modal_vb: None
		}
	},
	related: {
		phrase: more than three owners
		question type: None
	}
}
"""
    }
]

WHICH_PAIRS_02 = [
    {
        "query": "Which of the most beautiful paintings has not been moved to Bacau?",
        "result": """
statement: {
	target: {
		phrase: which of the most beautiful paintings
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		}
	},
	related: {
		phrase: to Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "Which of the most beautiful paintings, artifacts and gorgeous swords has not been moved to Bacau?",
        "result": """
statement: {
	target: {
		phrase: which of the most beautiful paintings
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		}
	},
	related: {
		phrase: to Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## of artifacts
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		}
	},
	related: {
		phrase: to Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## of gorgeous swords
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		}
	},
	related: {
		phrase: to Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "Which one of the most beautiful paintings has not been moved to Bacau?",
        "result": """
statement: {
	target: {
		phrase: which one of the most beautiful paintings
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		}
	},
	related: {
		phrase: to Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "Which one of the most beautiful paintings, artifacts and gorgeous swords has not been moved to Bacau?",
        "result": """
statement: {
	target: {
		phrase: which one of the most beautiful paintings
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		}
	},
	related: {
		phrase: to Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## of artifacts
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		}
	},
	related: {
		phrase: to Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## of gorgeous swords
		question type: which
	},
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		}
	},
	related: {
		phrase: to Bacau
		question type: None
	}
}
"""
    }
]

WHICH_PAIRS_03 = [
    {
        # [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome?",
        "result": """
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		}
	},
	related: {
		phrase: in Casablanca
		question type: None
	}
}
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [has, been],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		phrase: to a writer
		question type: None
	}
}
statement: {
	target: {
		phrase: to a writer
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		}
	},
	related: {
		phrase: in Rome
		question type: None
	}
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer?",
        "result": """
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		}
	},
	related: {
		phrase: in Casablanca
		question type: None
	}
}
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: to a writer
		question type: None
	}
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer?",
        "result": """
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		}
	},
	related: {
		phrase: in Casablanca
		question type: None
	}
}
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [has, been],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		phrase: to a writer
		question type: None
	}
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome?",
        "result": """
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		}
	},
	related: {
		phrase: in Casablanca
		question type: None
	}
}
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: to a writer
		question type: None
	}
}
statement: {
	target: {
		phrase: to a writer
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		}
	},
	related: {
		phrase: in Rome
		question type: None
	}
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		}
	},
	related: {
		phrase: in Casablanca
		question type: None
	}
}
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [has, been],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		phrase: to a writer
		question type: None
	}
}
statement: {
	target: {
		phrase: to a writer
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		}
	},
	related: {
		phrase: in Rome
		question type: None
	}
}
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: has,
			modal_vb: None
		}
	},
	related: {
		phrase: three children
		question type: None
	}
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		}
	},
	related: {
		phrase: in Casablanca
		question type: None
	}
}
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: to a writer
		question type: None
	}
}
statement: {
	target: {
		phrase: to a writer
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		}
	},
	related: {
		phrase: in Rome
		question type: None
	}
}
statement: {
	target: {
		phrase: which female actor
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: has,
			modal_vb: None
		}
	},
	related: {
		phrase: three children
		question type: None
	}
}
"""
    },
    {
        # derived from [2]
        "query": "Which beautiful female is married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target: {
		phrase: which beautiful female
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: to a writer
		question type: None
	}
}
statement: {
	target: {
		phrase: to a writer
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		}
	},
	related: {
		phrase: in Rome
		question type: None
	}
}
statement: {
	target: {
		phrase: which beautiful female
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: has,
			modal_vb: None
		}
	},
	related: {
		phrase: three children
		question type: None
	}
}
"""
    },
    {
        "query": "Which woman is beautiful, generous, tall and rich?",
        "result": """
statement: {
	target: {
		phrase: which woman
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: beautiful
		question type: None
	}
}
statement: {
	target: {
		phrase: which woman
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##and## generous
		question type: None
	}
}
statement: {
	target: {
		phrase: which woman
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##and## tall
		question type: None
	}
}
statement: {
	target: {
		phrase: which woman
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##and## rich
		question type: None
	}
}
"""
    },
    {
        "query": "Which smart woman is beautiful, generous, tall and rich?",
        "result": """
statement: {
	target: {
		phrase: which smart woman
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: beautiful
		question type: None
	}
}
statement: {
	target: {
		phrase: which smart woman
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##and## generous
		question type: None
	}
}
statement: {
	target: {
		phrase: which smart woman
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##and## tall
		question type: None
	}
}
statement: {
	target: {
		phrase: which smart woman
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: ##and## rich
		question type: None
	}
}
"""
    }
]

WHICH_PAIRS_04 = [
    {
        # [6]
        "query": "Which colour do you want?",
        "result": """
statement: {
	target: {
		phrase: which colour
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [do],
			main_vb: want,
			modal_vb: None
		}
	},
	related: {
		phrase: you
		question type: None
	}
}
"""
    }
]

WHICH_PAIRS = WHICH_PAIRS_01 + \
              WHICH_PAIRS_02 + \
              WHICH_PAIRS_03 + \
              WHICH_PAIRS_04
