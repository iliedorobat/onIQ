pairs_00 = [
    {
        "query": "Which is the noisiest and the largest city?",
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
	related_phrases: the noisiest

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
	conjunction: and,
	related_phrases: the largest city
"""
    },
    {
        "query": "Which is the noisiest and the most beautiful city?",
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
	related_phrases: the noisiest

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
	conjunction: and,
	related_phrases: the most beautiful city
"""
    },
    {
        "query": "What museums are in Bacau, Iasi or Bucharest?",
        "result": """
statement: {
	target_phrase: what museums,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Bacau

statement: {
	target_phrase: what museums,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: or,
	related_phrases: in Iasi

statement: {
	target_phrase: what museums,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: or,
	related_phrases: in Bucharest
"""
    },
    {
        "query": "What museums are in Bacau or Bucharest?",
        "result": """
statement: {
	target_phrase: what museums,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Bacau

statement: {
	target_phrase: what museums,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: or,
	related_phrases: in Bucharest
"""
    },
    {
        "query": "Which museum hosts more than 10 pictures and exposed one sword?",
        "result": """
statement: {
	target_phrase: which museum,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: hosts,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: more than 10 pictures

statement: {
	target_phrase: which museum,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: exposed,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: one sword
"""
    },
    {
        "query": "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?",
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
	related_phrases: the name of the largest museum

statement: {
	target_phrase: the name of the largest museum,
	action: {
		dep: relcl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: hosts,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: more than 10 pictures

statement: {
	target_phrase: the name of the largest museum,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: exposed,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: one sword
"""
    },
    {
        "query": "Which is the museum which hosts more than 10 pictures and exposed one sword?",
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
	related_phrases: the museum

statement: {
	target_phrase: the museum,
	action: {
		dep: relcl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: hosts,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: more than 10 pictures

statement: {
	target_phrase: the museum,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: exposed,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: one sword
"""
    },
    {
        "query": "When does the museum open?",
        "result": """
statement: {
	target_phrase: when,
	action: {
		dep: aux,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [does],
			acomp: open,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the museum
"""
    },
    {
        "query": "Which painting has not been deposited in Bacau?",
        "result": """
statement: {
	target_phrase: which painting,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [has, been],
			acomp: None,
			main_vb: deposited,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Bacau

"""
    },
    {
        "query": "Which paintings and statues have not been deposited in Bacau?",
        "result": """
statement: {
	target_phrase: which paintings,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [have, been],
			acomp: None,
			main_vb: deposited,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Bacau

statement: {
	target_phrase: which statues,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [have, been],
			acomp: None,
			main_vb: deposited,
			modal_vb: None
		}
	},
	conjunction: and,
	related_phrases: in Bacau
"""
    },
    {
        "query": "Which paintings, sharp swords and tall statues have not been deposited in Bacau?",
        "result": """
statement: {
	target_phrase: which paintings,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [have, been],
			acomp: None,
			main_vb: deposited,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Bacau

statement: {
	target_phrase: which sharp swords,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [have, been],
			acomp: None,
			main_vb: deposited,
			modal_vb: None
		}
	},
	conjunction: and,
	related_phrases: in Bacau

statement: {
	target_phrase: which tall statues,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [have, been],
			acomp: None,
			main_vb: deposited,
			modal_vb: None
		}
	},
	conjunction: and,
	related_phrases: in Bacau
"""
    },
    {
        "query": "Where are the coins and swords located?",
        "result": """
statement: {
	target_phrase: where,
	action: {
		dep: acl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: located,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the coins

statement: {
	target_phrase: where,
	action: {
		dep: acl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: located,
			modal_vb: None
		}
	},
	conjunction: and,
	related_phrases: swords
"""
    },
    {
        "query": "What museums and swords are in Bacau?",
        "result": """
statement: {
	target_phrase: what museums,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Bacau

statement: {
	target_phrase: what swords,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: and,
	related_phrases: in Bacau
"""
    },
    {
        "query": "Where was the last place the picture was exposed",
        "result": """
statement: {
	target_phrase: where,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [was],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the last place

statement: {
	target_phrase: the last place,
	action: {
		dep: relcl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [was],
			acomp: None,
			main_vb: exposed,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the picture
"""
    },
    {
        # TODO: the most beautiful
        "query": "Which is the noisiest, the most beautiful and the largest city?",
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
	related_phrases: the noisiest

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
	conjunction: and,
	related_phrases: the largest city
"""
    },
    {
        "query": "Where is the museum?",
        "result": """
statement: {
	target_phrase: where,
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
	related_phrases: the museum
"""
    },
    {
        "query": "What is the most beautiful museum?",
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
	related_phrases: the most beautiful museum
"""
    },
    {
        "query": "What is the name of the most beautiful museum?",
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
	related_phrases: the name of the most beautiful museum
"""
    },
    {
        "query": "What is the name of the largest museum?",
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
	related_phrases: the name of the largest museum
"""
    },
    {
        "query": "What is the most beautiful place and the largest cave?",
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
	related_phrases: the most beautiful place

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
	related_phrases: the largest cave
"""
    },
    {
        # TODO: "Which"
        "query": "Which of the most beautiful paintings has not been moved to Bacau?",
        "result": """
statement: {
	target_phrase: of the most beautiful paintings,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [has, been],
			acomp: None,
			main_vb: moved,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: to Bacau
"""
    },
    {
        # TODO: "Which one"
        "query": "Which one of the most beautiful paintings has not been moved to Bacau?",
        "result": """
statement: {
	target_phrase: of the most beautiful paintings,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [has, been],
			acomp: None,
			main_vb: moved,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: to Bacau
"""
    },
    {
        "query": "Did James work with Andrew?",
        "result": """
statement: {
	target_phrase: James,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [Did],
			acomp: None,
			main_vb: work,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: with Andrew
"""
    },
    {
        "query": "Where does the engineer go?",
        "result": """
statement: {
	target_phrase: where,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [does],
			acomp: None,
			main_vb: go,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the engineer
"""
    },
    {
        "query": "Which is the noisiest, the largest and the most crowded city?",
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
	related_phrases: the noisiest

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
	conjunction: and,
	related_phrases: the most crowded city
"""
    },
    {
        "query": "Which paintings do not have more than three owners?",
        "result": """
statement: {
	target_phrase: which paintings,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [do, have],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: more than three owners
"""
    },
    {
        "query": "Which painting, sharp swords or statues do not have more than three owners?",
        "result": """
statement: {
	target_phrase: which painting,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [do, have],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: more than three owners

statement: {
	target_phrase: which sharp swords,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [do, have],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: or,
	related_phrases: more than three owners

statement: {
	target_phrase: which statues,
	action: {
		dep: ROOT,
		is_available: False,
		neg: not,
		verb: {
			aux_vbs: [do, have],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: or,
	related_phrases: more than three owners
"""
    },
    {
        "query": "Which paintings, swords or statues are in Bacau?",
        "result": """
statement: {
	target_phrase: which paintings,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in Bacau

statement: {
	target_phrase: which swords,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: or,
	related_phrases: in Bacau

statement: {
	target_phrase: which statues,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: or,
	related_phrases: in Bacau
"""
    },
    {
        "query": "Who is the director who own 2 cars and sold a house or a panel?",
        "result": """
statement: {
	target_phrase: who,
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
	related_phrases: the director

statement: {
	target_phrase: the director,
	action: {
		dep: relcl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: own,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: 2 cars

statement: {
	target_phrase: the director,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: sold,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: a house

statement: {
	target_phrase: the director,
	action: {
		dep: conj,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: sold,
			modal_vb: None
		}
	},
	conjunction: or,
	related_phrases: a panel
"""
    },
    {
        "query": "Where is the museum located?",
        "result": """
statement: {
	target_phrase: where,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: None,
			main_vb: located,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the museum
"""
    },
    {
        "query": "Where does the holder of the position of Lech Kaczynski live?",
        "result": """
statement: {
	target_phrase: where,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [does],
			acomp: None,
			main_vb: live,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the holder of the position of Lech Kaczynski
"""
    },
    {
        "query": "Who is very beautiful?",
        "result": """
statement: {
	target_phrase: who,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: beautiful,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: very beautiful
"""
    },
    {
        "query": "Who is the most beautiful?",
        "result": """
statement: {
	target_phrase: who,
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
	related_phrases: the most beautiful
"""
    },
    {
        "query": "Who is the most beautiful woman and the most generous person?",
        "result": """
statement: {
	target_phrase: who,
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
	related_phrases: the most beautiful woman

statement: {
	target_phrase: who,
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
	related_phrases: the most generous person
"""
    },
    {
        "query": "Which smart kid is famous?",
        "result": """
statement: {
	target_phrase: smart kid,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: famous,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: famous
"""
    },
    {
        "query": "Which of the smart kids are famous?",
        "result": """
statement: {
	target_phrase: of the smart kids,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [are],
			acomp: famous,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: famous
"""
    }
]
