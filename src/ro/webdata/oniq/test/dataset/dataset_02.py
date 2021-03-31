pairs_02 = [
    {
        # [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome?",
        "result": """
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Casablanca
}
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: [has, been],
			main_vb: married,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: a writer
}
statement: {
	target_chunks: [a writer],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Rome
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer?",
        "result": """
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Casablanca
}
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [married]
	},
	related_chunk: a writer
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer?",
        "result": """
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Casablanca
}
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: [has, been],
			main_vb: married,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: a writer
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome?",
        "result": """
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Casablanca
}
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [married]
	},
	related_chunk: a writer
}
statement: {
	target_chunks: [a writer],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Rome
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Casablanca
}
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: [has, been],
			main_vb: married,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: a writer
}
statement: {
	target_chunks: [a writer],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Rome
}
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: [has],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: three children
}
"""
    },
    {
        # derived from [2]
        "query": "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: played,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Casablanca
}
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [married]
	},
	related_chunk: a writer
}
statement: {
	target_chunks: [a writer],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Rome
}
statement: {
	target_chunks: [Which female actor],
	action: {
		neg: None,
		verb: {
			aux_vbs: [has],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: three children
}
"""
    },
    {
        # derived from [2]
        "query": "Which beautiful female is married to a writer born in Rome and has three children?",
        "result": """
statement: {
	target_chunks: [Which beautiful female],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [married]
	},
	related_chunk: a writer
}
statement: {
	target_chunks: [a writer],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: born,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Rome
}
statement: {
	target_chunks: [Which beautiful female],
	action: {
		neg: None,
		verb: {
			aux_vbs: [has],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: three children
}
"""
    },
    {
        # [2]
        "query": "Which is the longest and shortest river that traverses Mississippi?",
        "result": """
statement: {
	target_chunks: [Which],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the longest and shortest river
}
statement: {
	target_chunks: [the longest and shortest river],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: traverses,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Mississippi
}
"""
    },
    {
        # [2]
        "query": "What is the population and area of the most populated state?",
        "result": """
statement: {
	target_chunks: [What],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the population
}
statement: {
	target_chunks: [What],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: area of the most populated state
}
"""
    }
]
