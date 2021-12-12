WHAT_DO_PAIRS_01 = [
    {
        # [1]
        "query": "What did James Cagney win in the 15th Academy Awards?",
        "result": """
statement: {
	target: {
		phrase: what did James Cagney
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [did],
			main_vb: win,
			modal_vb: None
		}
	},
	related: {
		phrase: in the 15th Academy Awards
		question type: None
	}
}
"""
    }
]

WHAT_DO_PAIRS_02 = [
    {
        # [6]
        "query": "What did you do that for?",
        "result": """
statement: {
	target: {
		phrase: what did you
		question type: what
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [did],
			main_vb: do,
			modal_vb: None
		}
	},
	related: {
		phrase: that
		question type: None
	}
}
"""
    }
]

WHAT_DO_PAIRS = WHAT_DO_PAIRS_01 + WHAT_DO_PAIRS_02
