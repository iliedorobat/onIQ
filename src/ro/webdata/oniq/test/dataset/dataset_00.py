WHAT_PAIRS = [
    {
        "query": "What museums and swords are in Bacau?",
        "result": """
statement: {
	target phrase: what museums,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
statement: {
	target phrase: ##and## what swords,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
"""
    },
    {
        "query": "What museums are in Bacau or Bucharest?",
        "result": """
statement: {
	target phrase: what museums,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
statement: {
	target phrase: what museums,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##or## in Bucharest
}
"""
    },
    {
        "query": "What museums are in Bacau, Iasi or Bucharest?",
        "result": """
statement: {
	target phrase: what museums,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
statement: {
	target phrase: what museums,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##or## in Iasi
}
statement: {
	target phrase: what museums,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##or## in Bucharest
}
"""
    }
]

WHAT_IS_PAIRS = [
    {
        "query": "What is the most beautiful museum?",
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
	related phrase: the most beautiful museum
}
"""
    },
    {
        "query": "What is the name of the largest museum?",
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
	related phrase: the name
}
statement: {
	target phrase: the name,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: of the largest museum
}
"""
    },
    {
        "query": "What is the name of the most beautiful museum?",
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
	related phrase: the name
}
statement: {
	target phrase: the name,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: of the most beautiful museum
}
"""
    },
    {
        "query": "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?",
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
	related phrase: the name
}
statement: {
	target phrase: the name,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: of the largest museum
}
statement: {
	target phrase: of the largest museum,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: more than 10 pictures
}
statement: {
	target phrase: of the largest museum,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: one sword
}
"""
    },
    {
        "query": "What is the most beautiful place and the largest cave?",
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
	related phrase: the most beautiful place
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
	related phrase: ##and## the largest cave
}
"""
    }
]

WHICH_PAIRS = [

    {
        "query": "Which smart kid is famous?",
        "result": """
statement: {
	target phrase: which smart kid,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [famous]
	},
	related phrase: famous
}
"""
    },
    {
        "query": "Which of the smart kids are famous?",
        "result": """
statement: {
	target phrase: which of the smart kids,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [famous]
	},
	related phrase: famous
}
"""
    },
    {
        "query": "Which paintings located in Bacau are in good shape?",
        "result": """
statement: {
	target phrase: which paintings,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
statement: {
	target phrase: which paintings,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in good shape
}
"""
    },
    {
        "query": "Which paintings, swords or statues are in Bacau?",
        "result": """
statement: {
	target phrase: which paintings,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
statement: {
	target phrase: ##or## which swords,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
statement: {
	target phrase: ##or## which statues,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
"""
    },
    {
        "query": "Which museum hosts more than 10 pictures and exposed one sword?",
        "result": """
statement: {
	target phrase: which museum,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: more than 10 pictures
}
statement: {
	target phrase: which museum,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: one sword
}
"""
    },
    {
        "query": "Which painting has not been deposited in Bacau?",
        "result": """
statement: {
	target phrase: which painting,
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: deposited,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
"""
    },
    {
        "query": "Which paintings and statues have not been deposited in Bacau?",
        "result": """
statement: {
	target phrase: which paintings,
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
statement: {
	target phrase: ##and## which statues,
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
"""
    },
    {
        "query": "Which paintings, sharp swords and tall statues have not been deposited in Bacau?",
        "result": """
statement: {
	target phrase: which paintings,
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
statement: {
	target phrase: ##and## which sharp swords,
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
statement: {
	target phrase: ##and## which tall statues,
	action: {
		neg: not,
		verb: {
			aux_vbs: [have, been],
			main_vb: deposited,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in Bacau
}
"""
    },
    {
        "query": "Which of the most beautiful paintings has not been moved to Bacau?",
        "result": """
statement: {
	target phrase: which of the most beautiful paintings,
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: to Bacau
}
"""
    },
    {
        "query": "Which one of the most beautiful paintings has not been moved to Bacau?",
        "result": """
statement: {
	target phrase: which one of the most beautiful paintings,
	action: {
		neg: not,
		verb: {
			aux_vbs: [has, been],
			main_vb: moved,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: to Bacau
}
"""
    },
    {
        "query": "Which paintings do not have more than three owners?",
        "result": """
statement: {
	target phrase: which paintings,
	action: {
		neg: not,
		verb: {
			aux_vbs: [do, have],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: more than three owners
}
"""
    },
    {
        "query": "Which painting, sharp swords or statues do not have more than three owners?",
        "result": """
statement: {
	target phrase: which painting,
	action: {
		neg: not,
		verb: {
			aux_vbs: [do, have],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: more than three owners
}
statement: {
	target phrase: ##or## which sharp swords,
	action: {
		neg: not,
		verb: {
			aux_vbs: [do, have],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: more than three owners
}
statement: {
	target phrase: ##or## which statues,
	action: {
		neg: not,
		verb: {
			aux_vbs: [do, have],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: more than three owners
}
"""
    }
]

WHICH_IS_PAIRS = [
    {
        "query": "Which is the noisiest and the largest city?",
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
		acomp_list: []
	},
	related phrase: the noisiest
}
statement: {
	target phrase: which,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##and## the largest city
}
"""
    },
    {
        "query": "Which is the noisiest and the most beautiful city?",
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
		acomp_list: []
	},
	related phrase: the noisiest
}
statement: {
	target phrase: which,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##and## the most beautiful city
}
"""
    },
    {
        # TODO: the most beautiful
        "query": "Which is the noisiest, the most beautiful and the largest city?",
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
		acomp_list: [beautiful, noisiest]
	},
	related phrase: the noisiest
}
statement: {
	target phrase: which,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [beautiful, noisiest]
	},
	related phrase: ##and## the largest city
}
"""
    },
    {
        # FIXME: "the largest", "the most crowded city"
        "query": "Which is the noisiest, the largest and the most crowded city?",
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
		acomp_list: []
	},
	related phrase: the noisiest
}
"""
    },
    {
        "query": "Which is the museum which hosts more than 10 pictures and exposed one sword?",
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
		acomp_list: []
	},
	related phrase: the museum
}
statement: {
	target phrase: the museum,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: more than 10 pictures
}
statement: {
	target phrase: the museum,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: one sword
}
"""
    }
]

WHO_PAIRS = [
    {
        "query": "Who is very beautiful?",
        "result": """
statement: {
	target phrase: who,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [beautiful]
	},
	related phrase: beautiful
}
"""
    },
    {
        "query": "Who is very beautiful and very smart?",
        "result": """
statement: {
	target phrase: who,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [beautiful, smart]
	},
	related phrase: beautiful
}
statement: {
	target phrase: who,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [beautiful, smart]
	},
	related phrase: ##and## smart
}
"""
    },
    {
        "query": "Who is the most beautiful woman and the most generous person?",
        "result": """
statement: {
	target phrase: who,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the most beautiful woman
}
statement: {
	target phrase: who,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##and## the most generous person
}
"""
    },
    {
        "query": "Who is the director who own 2 cars and sold a house or a panel?",
        "result": """
statement: {
	target phrase: who,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the director
}
statement: {
	target phrase: the director,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: own,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: 2 cars
}
statement: {
	target phrase: the director,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: sold,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: a house
}
statement: {
	target phrase: the director,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: sold,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##or## a panel
}
"""
    }
]

WHOSE_PAIRS = [
    {
        "query": "Whose picture is it?",
        "result": """
statement: {
	target phrase: whose picture,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: it
}
"""
    }
]

WHEN_PAIRS = [
#     {
#         # FIXME:
#         "query": "When does the museum open?",
#         "result": """
#
# """
#     }
]

WHERE_PAIRS = [
    {
        "query": "Where is the museum?",
        "result": """
statement: {
	target phrase: where,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the museum
}
"""
    },
    {
        "query": "Where is the museum located?",
        "result": """
statement: {
	target phrase: where,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the museum
}
"""
    },
    {
        "query": "Where does the engineer go?",
        "result": """
statement: {
	target phrase: where,
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: go,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the engineer
}
"""
    },
    {
        "query": "Where are the coins and swords located?",
        "result": """
statement: {
	target phrase: where,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the coins
}
statement: {
	target phrase: where,
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##and## swords
}
"""
    },
    {
        "query": "Where was the last place the picture was exposed?",
        "result": """
statement: {
	target phrase: where,
	action: {
		neg: None,
		verb: {
			aux_vbs: [was],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the last place
}
statement: {
	target phrase: the last place,
	action: {
		neg: None,
		verb: {
			aux_vbs: [was],
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the picture
}
"""
    },
    {
        # TODO: improve the statement structure
        "query": "Where does the holder of the position of Lech Kaczynski live?",
        "result": """
statement: {
	target phrase: where,
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: live,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the holder
}
statement: {
	target phrase: the holder,
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: live,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: of the position
}
statement: {
	target phrase: of the position,
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: live,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: of Lech Kaczynski
}
"""
    }
]

QUANTITY_QUESTIONS_PAIRS = [
    {
        "query": "How long does the museum remain closed?",
        "result": """
statement: {
	target phrase: how long does the museum,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: remain,
			modal_vb: None
		},
		acomp_list: [closed]
	},
	related phrase: closed
}
"""
    },
    {
        "query": "How many days do I have to wait for him?",
        "result": """
statement: {
	target phrase: how many days do I,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: wait,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: for him
}
"""
    }
]

DIRECT_QUESTIONS_PAIRS = [
    # {
    #     # FIXME:
    #     "query": "Did James work with Andrew?",
    #     "result": ""
    # }
]

PAIRS_00 = WHAT_PAIRS + \
           WHAT_IS_PAIRS + \
           WHICH_PAIRS + \
           WHICH_IS_PAIRS + \
           WHO_PAIRS + \
           WHOSE_PAIRS + \
           WHEN_PAIRS + \
           WHERE_PAIRS + \
           QUANTITY_QUESTIONS_PAIRS + \
           DIRECT_QUESTIONS_PAIRS
