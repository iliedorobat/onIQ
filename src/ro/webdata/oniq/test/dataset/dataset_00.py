pairs_00 = [
    {
        "query": "Which is the noisiest and the largest city?",
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
	related_chunk: the noisiest
}
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
	related_chunk: the largest city
}
"""
    },
    {
        "query": "Which is the noisiest and the most beautiful city?",
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
	related_chunk: the noisiest
}
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
	related_chunk: the most beautiful city
}
"""
    },
    {
        "query": "What museums are in Bacau or Bucharest?",
        "result": """
statement: {
	target_chunks: [What museums],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
statement: {
	target_chunks: [What museums],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bucharest
}
"""
    },
    {
        "query": "What museums are in Bacau, Iasi or Bucharest?",
        "result": """
statement: {
	target_chunks: [What museums],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
statement: {
	target_chunks: [What museums],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Iasi
}
statement: {
	target_chunks: [What museums],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bucharest
}
"""
    },
    {
        "query": "Which museum hosts more than 10 pictures and exposed one sword?",
        "result": """
statement: {
	target_chunks: [Which museum],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: more than 10 pictures
}
statement: {
	target_chunks: [Which museum],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: one sword
}
"""
    },
    {
        "query": "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?",
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
	related_chunk: the name of the largest museum
}
statement: {
	target_chunks: [the name of the largest museum],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: more than 10 pictures
}
statement: {
	target_chunks: [the name of the largest museum],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: one sword
}
"""
    },
    {
        "query": "Which is the museum which hosts more than 10 pictures and exposed one sword?",
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
	related_chunk: the museum
}
statement: {
	target_chunks: [the museum],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: more than 10 pictures
}
statement: {
	target_chunks: [the museum],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: one sword
}
"""
    },
    {
        "query": "When does the museum open?",
        "result": """
statement: {
	target_chunks: [When],
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [open]
	},
	related_chunk: the museum
}
"""
    },
    {
        "query": "Which painting has not been deposited in Bacau?",
        "result": """
statement: {
	target_chunks: [Which painting],
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: deposited,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
"""
    },
    {
        "query": "Which paintings and statues have not been deposited in Bacau?",
        "result": """
statement: {
	target_chunks: [Which paintings, statues],
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
"""
    },
    {
        "query": "Which paintings, sharp swords and tall statues have not been deposited in Bacau?",
        "result": """
statement: {
	target_chunks: [Which paintings, sharp swords, tall statues],
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
"""
    },
    {
        "query": "Where are the coins and swords located?",
        "result": """
statement: {
	target_chunks: [Where],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the coins
}
statement: {
	target_chunks: [Where],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: swords
}
"""
    },
    {
        "query": "What museums and swords are in Bacau?",
        "result": """
statement: {
	target_chunks: [What museums, swords],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
"""
    },
    # {
    #     "query": "Where was the last place the picture was exposed",
    #     "result": ""  # FIXME
    # },
    {
        # TODO: the most beautiful
        "query": "Which is the noisiest, the most beautiful and the largest city?",
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
	related_chunk: the noisiest
}
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
	related_chunk: the largest city
}
"""
    },
    {
        "query": "Where is the museum?",
        "result": """
statement: {
	target_chunks: [Where],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the museum
}
"""
    },
    {
        "query": "What is the most beautiful museum?",
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
	related_chunk: the most beautiful museum
}
"""
    },
    {
        "query": "What is the name of the most beautiful museum?",
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
	related_chunk: the name of the most beautiful museum
}
"""
    },
    {
        "query": "What is the name of the largest museum?",
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
	related_chunk: the name of the largest museum
}
"""
    },
    {
        "query": "What is the most beautiful place and the largest cave?",
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
	related_chunk: the most beautiful place
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
	related_chunk: the largest cave
}
"""
    },
    {
        "query": "Which of the most beautiful paintings has not been moved to Bacau?",
        "result": """
statement: {
	target_chunks: [Which of the most beautiful paintings],
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
"""
    },
    {
        "query": "Which one of the most beautiful paintings has not been moved to Bacau?",
        "result": """
statement: {
	target_chunks: [Which one of the most beautiful paintings],
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
"""
    },
    # {
    #     "query": "Did James work with Andrew?",
    #     "result": ""  # FIXME
    # },
    {
        "query": "Where does the engineer go?",
        "result": """
statement: {
	target_chunks: [Where],
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: go,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the engineer
}
"""
    },
    {
        # TODO: "the largest"
        "query": "Which is the noisiest, the largest and the most crowded city?",
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
	related_chunk: the noisiest
}
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
	related_chunk: the most crowded city
}
"""
    },
    {
        "query": "Which paintings do not have more than three owners?",
        "result": """
statement: {
	target_chunks: [Which paintings],
	action: {
		neg: not,
		verb: {
			aux_vbs: [do, have],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: more than three owners
}
"""
    },
    {
        "query": "Which painting, sharp swords or statues do not have more than three owners?",
        "result": """
statement: {
	target_chunks: [Which painting, sharp swords, statues],
	action: {
		neg: not,
		verb: {
			aux_vbs: [do, have],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: more than three owners
}
"""
    },
    {
        "query": "Which paintings, swords or statues are in Bacau?",
        "result": """
statement: {
	target_chunks: [Which paintings, swords, statues],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
"""
    },
    {
        "query": "Who is the director who own 2 cars and sold a house or a panel?",
        "result": """
statement: {
	target_chunks: [Who],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the director
}
statement: {
	target_chunks: [the director],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: own,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: 2 cars
}
statement: {
	target_chunks: [the director],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: sold,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: a house
}
statement: {
	target_chunks: [the director],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: sold,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: a panel
}
"""
    },
    {
        "query": "Where is the museum located?",
        "result": """
statement: {
	target_chunks: [Where],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the museum
}
"""
    },
    {
        "query": "Where does the holder of the position of Lech Kaczynski live?",
        "result": """
statement: {
	target_chunks: [Where],
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: live,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the holder of the position of Lech Kaczynski
}
"""
    },
    {
        "query": "Who is very beautiful?",
        "result": """
statement: {
	target_chunks: [Who],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [beautiful]
	},
	related_chunk: beautiful
}
"""
    },
    {
        "query": "Who is very beautiful and very smart?",
        "result": """
statement: {
	target_chunks: [Who],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [beautiful]
	},
	related_chunk: beautiful
}
statement: {
	target_chunks: [Who],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [smart]
	},
	related_chunk: smart
}
"""
    },
    {
        "query": "Who is the most beautiful woman and the most generous person?",
        "result": """
statement: {
	target_chunks: [Who],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the most beautiful woman
}
statement: {
	target_chunks: [Who],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the most generous person
}
"""
    },
    {
        "query": "Which smart kid is famous?",
        "result": """
statement: {
	target_chunks: [Which smart kid],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [famous]
	},
	related_chunk: famous
}
"""
    },
    {
        "query": "Which of the smart kids are famous?",
        "result": """
statement: {
	target_chunks: [Which of the smart kids],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [famous]
	},
	related_chunk: famous
}
"""
    },
    {
        "query": "Which paintings located in Bacau are in good shape?",
        "result": """
statement: {
	target_chunks: [Which paintings],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: Bacau
}
statement: {
	target_chunks: [Which paintings],
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: good shape
}
"""
    },
    {
        "query": "Whose picture is it?",
        "result": """
statement: {
	target_chunks: [Whose picture],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: it
}
"""
    },
    {
        "query": "How long does the museum remain closed?",
        "result": """
statement: {
	target_chunks: [How long does the museum],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: remain,
			modal_vb: None
		},
		acomp_list: [closed]
	},
	related_chunk: closed
}
"""
    },
    {
        "query": "How many days do I have to wait for him?",
        "result": """
statement: {
	target_chunks: [How many days do I],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: wait,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: him
}
"""
    }
]
