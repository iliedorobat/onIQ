WHAT_PAIRS = [
    {
        "query": "What museums and libraries are there in Bacau?",
        "result": """
statement: {
	target: {
		phrase: what museums
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## what libraries
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "What museums and libraries are in Bacau or Bucharest?",
        "result": """
statement: {
	target: {
		phrase: what museums
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: what museums
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: ##or## in Bucharest
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## what libraries
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## what libraries
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: ##or## in Bucharest
		question type: None
	}
}
"""
    },
    {
        "query": "What museums are in Bacau or Bucharest?",
        "result": """
statement: {
	target: {
		phrase: what museums
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: what museums
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: ##or## in Bucharest
		question type: None
	}
}
"""
    },
    {
        "query": "What museums are in Bacau, Iasi or Bucharest?",
        "result": """
statement: {
	target: {
		phrase: what museums
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: what museums
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: ##or## in Iasi
		question type: None
	}
}
statement: {
	target: {
		phrase: what museums
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: ##or## in Bucharest
		question type: None
	}
}
"""
    }
]

WHAT_IS_PAIRS = [
    {
        "query": "What is the most beautiful museum?",
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
		phrase: the most beautiful museum
		question type: None
	}
}
"""
    },
    {
        "query": "What is the name of the largest museum?",
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
		phrase: the name of the largest museum
		question type: None
	}
}
"""
    },
    {
        "query": "What is the name of the most beautiful museum?",
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
		phrase: the name of the most beautiful museum
		question type: None
	}
}
"""
    },
    {
        "query": "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?",
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
		phrase: the name of the largest museum
		question type: None
	}
}
statement: {
	target: {
		phrase: the name of the largest museum
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: more than 10 pictures
		question type: None
	}
}
statement: {
	target: {
		phrase: the name of the largest museum
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: one sword
		question type: None
	}
}
"""
    },
    {
        "query": "What is the most beautiful place and the largest cave?",
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
		phrase: the most beautiful place
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
		phrase: ##and## the largest cave
		question type: None
	}
}
"""
    }
]

WHICH_PAIRS = [

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
		},
		acomp_list: [famous]
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
		},
		acomp_list: [famous]
	},
	related: {
		phrase: famous
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "What sharp swords, very beautiful paintings, or tall statues are in Bacau?",
        "result": """
statement: {
	target: {
		phrase: what sharp swords
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## what very beautiful paintings
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## what tall statues
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
	},
	related: {
		phrase: in Bacau
		question type: None
	}
}
"""
    },
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
		},
		acomp_list: []
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
		},
		acomp_list: []
	},
	related: {
		phrase: to Bacau
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
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
		},
		acomp_list: []
	},
	related: {
		phrase: more than three owners
		question type: None
	}
}
"""
    }
]

WHICH_IS_PAIRS = [
    {
        "query": "Which is the most visited museum?",
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
		acomp_list: []
	},
	related: {
		phrase: the most visited museum
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest and the largest city?",
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
		acomp_list: []
	},
	related: {
		phrase: the noisiest
		question type: None
	}
}
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
		acomp_list: []
	},
	related: {
		phrase: ##and## the largest city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest town and the largest city?",
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
		acomp_list: []
	},
	related: {
		phrase: the noisiest town
		question type: None
	}
}
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
		acomp_list: []
	},
	related: {
		phrase: ##and## the largest city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest and the most beautiful city?",
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
		acomp_list: []
	},
	related: {
		phrase: the noisiest
		question type: None
	}
}
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
		acomp_list: []
	},
	related: {
		phrase: ##and## the most beautiful city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest, the most beautiful and the largest city?",
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
		acomp_list: [beautiful, noisiest]
	},
	related: {
		phrase: the noisiest
		question type: None
	}
}
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
		acomp_list: [beautiful, noisiest]
	},
	related: {
		phrase: ##and## the most beautiful
		question type: None
	}
}
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
		acomp_list: [beautiful, noisiest]
	},
	related: {
		phrase: ##and## the largest city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest, the largest and the most crowded city?",
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
		acomp_list: [largest, noisiest]
	},
	related: {
		phrase: the noisiest
		question type: None
	}
}
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
		acomp_list: [largest, noisiest]
	},
	related: {
		phrase: ##and## the largest
		question type: None
	}
}
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
		acomp_list: [largest, noisiest]
	},
	related: {
		phrase: ##and## the most crowded city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest, the newest, the largest and the most crowded city?",
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
		acomp_list: [largest, newest]
	},
	related: {
		phrase: the noisiest
		question type: None
	}
}
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
		acomp_list: [largest, newest]
	},
	related: {
		phrase: ##and## the newest
		question type: None
	}
}
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
		acomp_list: [largest, newest]
	},
	related: {
		phrase: ##and## the largest
		question type: None
	}
}
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
		acomp_list: [largest, newest]
	},
	related: {
		phrase: ##and## the most crowded city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the museum which hosts more than 10 pictures and exposed one sword?",
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
		acomp_list: []
	},
	related: {
		phrase: the museum
		question type: None
	}
}
statement: {
	target: {
		phrase: the museum
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: more than 10 pictures
		question type: None
	}
}
statement: {
	target: {
		phrase: the museum
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: one sword
		question type: None
	}
}
"""
    }
]

WHO_PAIRS = [
    {
        "query": "Who is married with Jane?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: married,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: with Jane
		question type: None
	}
}
"""
    },
    {
        "query": "Who is very beautiful?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [beautiful]
	},
	related: {
		phrase: beautiful
		question type: None
	}
}
"""
    },
    {
        "query": "Who is very beautiful and very smart?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [beautiful, smart]
	},
	related: {
		phrase: beautiful
		question type: None
	}
}
statement: {
	target: {
		phrase: who
		question type: who
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: [beautiful, smart]
	},
	related: {
		phrase: ##and## smart
		question type: None
	}
}
"""
    },
    {
        "query": "Who is the most beautiful woman and the most generous person?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: the most beautiful woman
		question type: None
	}
}
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: ##and## the most generous person
		question type: None
	}
}
"""
    },
    {
        "query": "Who is the director who own 2 cars and sold a house or a panel?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: the director
		question type: None
	}
}
statement: {
	target: {
		phrase: the director
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: own,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: 2 cars
		question type: None
	}
}
statement: {
	target: {
		phrase: the director
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: sold,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: a house
		question type: None
	}
}
statement: {
	target: {
		phrase: the director
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: sold,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: ##or## a panel
		question type: None
	}
}
"""
    }
]

WHOSE_PAIRS = [
    {
        "query": "Whose picture is it?",
        "result": """
statement: {
	target: {
		phrase: whose picture
		question type: whose
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
		phrase: it
		question type: None
	}
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
	target: {
		phrase: where
		question type: where
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
		phrase: the museum
		question type: None
	}
}
"""
    },
    {
        "query": "Where is the museum located?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: the museum
		question type: None
	}
}
"""
    },
    {
        "query": "Where is the black picture?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the black picture
		question type: None
	}
}
"""
    },
    {
        "query": "Where does the engineer go?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: go,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: the engineer
		question type: None
	}
}
"""
    },
    {
        "query": "Where are the coins and swords located?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: the coins
		question type: None
	}
}
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: ##and## swords
		question type: None
	}
}
"""
    },
    {
        "query": "Where was the last place the picture was exposed?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [was],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: the last place
		question type: None
	}
}
statement: {
	target: {
		phrase: the last place
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [was],
			main_vb: exposed,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: the picture
		question type: None
	}
}
"""
    },
    {
        "query": "Where does the holder of the position of Lech Kaczynski live?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: live,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: the holder of the position of Lech Kaczynski
		question type: None
	}
}
"""
    },
    {
        # [5]
        # NOTICE: "adam mickiewicz" is the named_entity and not "adam mickiewicz monument"
        "query": "Where is adam mickiewicz monument?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: adam mickiewicz monument
		question type: None
	}
}
"""
    },
    {
        # [5]
        "query": "Where can one find farhad and shirin monument?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: find,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: farhad and shirin monument
		question type: None
	}
}
"""
    },
    {
        "query": "Where is the Museum of Amsterdam?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the Museum of Amsterdam
		question type: None
	}
}
"""
    },
    {
        "query": "Where are the swords and axes made?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: made,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: the swords
		question type: None
	}
}
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: made,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: ##and## axes
		question type: None
	}
}
"""
    }
]

QUANTITY_QUESTIONS_PAIRS = [
    {
        "query": "How long does the museum remain closed?",
        "result": """
statement: {
	target: {
		phrase: how long does the museum
		question type: how
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: remain,
			modal_vb: None
		},
		acomp_list: [closed]
	},
	related: {
		phrase: closed
		question type: None
	}
}
"""
    },
    {
        "query": "How long does the largest museum remain closed?",
        "result": """
statement: {
	target: {
		phrase: how long does the largest museum
		question type: how
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: remain,
			modal_vb: None
		},
		acomp_list: [closed]
	},
	related: {
		phrase: closed
		question type: None
	}
}
"""
    },
    {
        "query": "How many people visit the Amsterdam Museum?",
        "result": """
statement: {
	target: {
		phrase: how many people
		question type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: visit,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: the Amsterdam Museum
		question type: None
	}
}
"""
    },
    {
        "query": "How many days do I have to wait for him?",
        "result": """
statement: {
	target: {
		phrase: how many days do I
		question type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: wait,
			modal_vb: None
		},
		acomp_list: []
	},
	related: {
		phrase: for him
		question type: None
	}
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
