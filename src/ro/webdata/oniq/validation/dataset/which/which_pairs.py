WHICH_PAIRS_01 = [
    {
        "query": "Which smart kid is famous?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which smart kid
		prep_phrase: None
		type: which
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
		operator: None
		phrase: famous
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which of the smart kids are famous?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: the smart kids
		type: which
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
		operator: None
		phrase: famous
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which of the paintings is the most beautiful?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: the paintings
		type: which
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
		operator: None
		phrase: the most beautiful
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which paintings located in Bacau are in good shape?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in good shape
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which paintings, swords or statues are in Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which swords
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which statues
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which paintings, swords, coins or statues are in Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which swords
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which coins
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which statues
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which paintings, swords, coins or statues are in Bacau or Bucharest?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: or
		phrase: in Bucharest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which swords
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which swords
		prep_phrase: None
		type: which
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
		operator: or
		phrase: in Bucharest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which coins
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which coins
		prep_phrase: None
		type: which
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
		operator: or
		phrase: in Bucharest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which statues
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which statues
		prep_phrase: None
		type: which
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
		operator: or
		phrase: in Bucharest
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: ilie.dorobat: exposed one sword => and exposed one sword
        "query": "Which museum hosts more than 10 pictures and exposed one sword?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which museum
		prep_phrase: None
		type: which
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
		operator: None
		phrase: more than 10 pictures
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which museum
		prep_phrase: None
		type: which
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
		operator: None
		phrase: one sword
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which painting has not been deposited in Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which painting
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which paintings and statues have not been deposited in Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: which statues
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which paintings, swords and statues have not been deposited in Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: which swords
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: which statues
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which paintings, sharp swords and tall statues have not been deposited in Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: which sharp swords
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: which tall statues
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which paintings do not have more than three owners?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: more than three owners
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which painting, sharp swords or statues do not have more than three owners?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which painting
		prep_phrase: None
		type: which
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
		operator: None
		phrase: more than three owners
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which sharp swords
		prep_phrase: None
		type: which
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
		operator: None
		phrase: more than three owners
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: which statues
		prep_phrase: None
		type: which
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
		operator: None
		phrase: more than three owners
		prep_phrase: None
		type: None
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
		operator: None
		phrase: which
		prep_phrase: the most beautiful paintings
		type: which
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
		operator: None
		phrase: to Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: ilie.dorobat: of artifacts; of gorgeous swords => which of the artifacts; which of the gorgeous swords
        "query": "Which of the most beautiful paintings, artifacts and gorgeous swords has not been moved to Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: the most beautiful paintings
		type: which
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
		operator: None
		phrase: to Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: of artifacts
		prep_phrase: None
		type: which
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
		operator: None
		phrase: to Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: of gorgeous swords
		prep_phrase: None
		type: which
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
		operator: None
		phrase: to Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which one of the most beautiful paintings has not been moved to Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which one of the most beautiful paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: to Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: ilie.dorobat: of artifacts; of gorgeous swords => which of the artifacts; which of the gorgeous swords
        "query": "Which one of the most beautiful paintings, artifacts and gorgeous swords has not been moved to Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which one of the most beautiful paintings
		prep_phrase: None
		type: which
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
		operator: None
		phrase: to Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: of artifacts
		prep_phrase: None
		type: which
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
		operator: None
		phrase: to Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: of gorgeous swords
		prep_phrase: None
		type: which
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
		operator: None
		phrase: to Bacau
		prep_phrase: None
		type: None
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
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Casablanca
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
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
		operator: None
		phrase: in Rome
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # FIXME: ilie.dorobat:
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Casablanca
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
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
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Casablanca
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # FIXME: ilie.dorobat
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Casablanca
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
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
		operator: None
		phrase: in Rome
		prep_phrase: None
		type: None
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
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Casablanca
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
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
		operator: None
		phrase: in Rome
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: three children
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # FIXME: ilie.dorobat
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: in Casablanca
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
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
		operator: None
		phrase: in Rome
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which female actor
		prep_phrase: None
		type: which
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
		operator: None
		phrase: three children
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # FIXME: ilie.dorobat
        # derived from [2]
        "query": "Which beautiful female is married to a writer born in Rome and has three children?",
        "result": """
	statement: {
	target: {
		operator: None
		phrase: which beautiful female
		prep_phrase: None
		type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: to a writer
		prep_phrase: None
		type: None
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
		operator: None
		phrase: in Rome
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which beautiful female
		prep_phrase: None
		type: which
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
		operator: None
		phrase: three children
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which woman is beautiful, generous, tall and rich?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which woman
		prep_phrase: None
		type: which
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
		operator: None
		phrase: beautiful
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which woman
		prep_phrase: None
		type: which
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
		operator: and
		phrase: generous
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which woman
		prep_phrase: None
		type: which
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
		operator: and
		phrase: tall
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which woman
		prep_phrase: None
		type: which
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
		operator: and
		phrase: rich
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which smart woman is beautiful, generous, tall and rich?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which smart woman
		prep_phrase: None
		type: which
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
		operator: None
		phrase: beautiful
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which smart woman
		prep_phrase: None
		type: which
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
		operator: and
		phrase: generous
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which smart woman
		prep_phrase: None
		type: which
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
		operator: and
		phrase: tall
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which smart woman
		prep_phrase: None
		type: which
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
		operator: and
		phrase: rich
		prep_phrase: None
		type: None
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
		operator: None
		phrase: which colour
		prep_phrase: None
		type: which
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
		operator: None
		phrase: you
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHICH_PAIRS = WHICH_PAIRS_01 + \
              WHICH_PAIRS_02 + \
              WHICH_PAIRS_03 + \
              WHICH_PAIRS_04
