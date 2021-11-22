WHAT_IS_PAIRS = [
    {
        # [2]
        # TODO: the population => the population of the most populated state
        "query": "What is the population and area of the most populated state?",
        "result": """
statement: {
	target: {
		phrase: what
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: the population
		question type: None
	}
}
statement: {
	target: {
		phrase: what
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: ##and## area of the most populated state
		question type: None
	}
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: [married]
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: [married]
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: [married]
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: [married]
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: [generous, tall, rich]
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
		},
		acomp_list: [generous, tall, rich]
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
		},
		acomp_list: [generous, tall, rich]
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
		},
		acomp_list: [generous, tall, rich]
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
		},
		acomp_list: [generous, tall, rich]
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
		},
		acomp_list: [generous, tall, rich]
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
		},
		acomp_list: [generous, tall, rich]
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
		},
		acomp_list: [generous, tall, rich]
	},
	related: {
		phrase: ##and## rich
		question type: None
	}
}
"""
    }
]

WHICH_IS_PAIRS = [
    {
        # derived from [2]
        "query": "Which is the longest and shortest river?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [shortest, longest]
	},
	related: {
		phrase: the longest and shortest river
		question type: None
	}
}
"""
    },
    {
        # [2]
        "query": "Which is the longest and shortest river that traverses Mississippi?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [shortest, longest]
	},
	related: {
		phrase: the longest and shortest river
		question type: None
	}
}
statement: {
	target: {
		phrase: the longest and shortest river
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: traverses,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: Mississippi
		question type: None
	}
}
"""
    }
]

PAIRS_02 = WHAT_IS_PAIRS + \
           WHICH_PAIRS + \
           WHICH_IS_PAIRS
