WHAT_IS_PAIRS = [
    {
        # [2]
        # TODO: improve the statement structure
        "query": "What is the population and area of the most populated state?",
        "result": """
statement: {
	target phrase: what,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the population
}
statement: {
	target phrase: what,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##and## area
}
statement: {
	target phrase: the population,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: of the most populated state
}
statement: {
	target phrase: ##and## area,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: of the most populated state
}
"""
    }
]

WHICH_PAIRS = [
    {
        # [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome?",
        "result": """
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Casablanca
}
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: [has, been],
			main_vb: married,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: to a writer
}
statement: {
	target phrase: to a writer,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Rome
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer?",
        "result": """
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Casablanca
}
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [married]
	},
	related phrase: to a writer
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer?",
        "result": """
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Casablanca
}
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: [has, been],
			main_vb: married,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: to a writer
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome?",
        "result": """
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Casablanca
}
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [married]
	},
	related phrase: to a writer
}
statement: {
	target phrase: to a writer,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Rome
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Casablanca
}
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: [has, been],
			main_vb: married,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: to a writer
}
statement: {
	target phrase: to a writer,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Rome
}
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: [has],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: three children
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Casablanca
}
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [married]
	},
	related phrase: to a writer
}
statement: {
	target phrase: to a writer,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Rome
}
statement: {
	target phrase: which female actor,
	action: {
		neg: None,
		verb: {
			aux_vbs: [has],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: three children
}
"""
    },
    {
        # derived from [2]
        "query": "Which beautiful female is married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target phrase: which beautiful female,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [married]
	},
	related phrase: to a writer
}
statement: {
	target phrase: to a writer,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Rome
}
statement: {
	target phrase: which beautiful female,
	action: {
		neg: None,
		verb: {
			aux_vbs: [has],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: three children
}
"""
    }
]

WHICH_IS_PAIRS = [
    {
        # [2]
        "query": "Which is the longest and shortest river that traverses Mississippi?",
        "result": """
statement: {
	target phrase: which,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [shortest, longest]
	},
	related phrase: the longest and shortest river
}
statement: {
	target phrase: the longest and shortest river,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: traverses,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: Mississippi
}
"""
    }
]

PAIRS_02 = WHAT_IS_PAIRS + \
           WHICH_PAIRS + \
           WHICH_IS_PAIRS
