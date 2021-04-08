WHAT_IS_PAIRS = [
    {
        # [3]
        "query": "What is villa la reine jeanne all about?",
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
	related phrase: villa la reine jeanne
}
"""
    }
]

WHEN_PAIRS = [
    {
        # [3]
        "query": "When was anıtkabir built?",
        "result": """
statement: {
	target phrase: when,
	action: {
		neg: None,
		verb: {
			aux_vbs: [was],
			main_vb: built,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: anıtkabir
}
"""
    }
]

PAIRS_03 = WHAT_IS_PAIRS + \
           WHEN_PAIRS
