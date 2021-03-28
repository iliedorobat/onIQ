pairs_02 = [
    {
        # [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome?",
        "result": """
statement: {
	target_phrase: which female actor,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: played,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Casablanca

statement: {
	target_phrase: which female actor,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [has, been],
			acomp: None,
			main_vb: married,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: to a writer

statement: {
	target_phrase: to a writer,
	action: {
		dep: acl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: born,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Rome
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome?",
        "result": """
statement: {
	target_phrase: which female actor,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: played,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Casablanca

statement: {
	target_phrase: which female actor,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: married,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: to a writer

statement: {
	target_phrase: to a writer,
	action: {
		dep: acl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: born,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Rome
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target_phrase: which female actor,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: played,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Casablanca

statement: {
	target_phrase: which female actor,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [has, been],
			acomp: None,
			main_vb: married,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: to a writer

statement: {
	target_phrase: to a writer,
	action: {
		dep: acl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: born,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Rome

statement: {
	target_phrase: to a writer,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [has],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: three children
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target_phrase: which female actor,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: played,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Casablanca

statement: {
	target_phrase: which female actor,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: married,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: to a writer

statement: {
	target_phrase: to a writer,
	action: {
		dep: acl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: born,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Rome

statement: {
	target_phrase: to a writer,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [has],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: three children
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer?",
        "result": """
statement: {
	target_phrase: which female actor,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: played,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Casablanca

statement: {
	target_phrase: which female actor,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: married,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: to a writer
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer?",
        "result": """
statement: {
	target_phrase: which female actor,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: played,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Casablanca

statement: {
	target_phrase: which female actor,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [has, been],
			acomp: None,
			main_vb: married,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: to a writer
"""
    },
    {
        # derived from [2]
        "query": "Which beautiful female is married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target_phrase: beautiful female,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: married,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: to a writer

statement: {
	target_phrase: to a writer,
	action: {
		dep: acl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: born,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Rome

statement: {
	target_phrase: to a writer,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [has],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: three children
"""
    },
    {
        # [2]
        "query": "Which is the longest and shortest river that traverses Mississippi?",
        "result": """
statement: {
	target_phrase: which,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the longest and shortest river

statement: {
	target_phrase: the longest and shortest river,
	action: {
		dep: relcl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: traverses,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: Mississippi
"""
    },
    {
        # [2]
        "query": "What is the population and area of the most populated state?",
        "result": """
statement: {
	target_phrase: what,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the population

statement: {
	target_phrase: what,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: and,
	related_phrases: area of the most populated state
"""
    }
]
