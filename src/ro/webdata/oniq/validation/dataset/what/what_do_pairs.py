WHAT_DO_PAIRS_01 = [
    {
        # [1]
        "query": "What did James Cagney win in the 15th Academy Awards?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what did James Cagney
		prep_phrase: None
		type: what
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
		operator: None
		phrase: in the 15th Academy Awards
		prep_phrase: None
		type: None
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
		operator: None
		phrase: what did you
		prep_phrase: None
		type: what
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
		operator: None
		phrase: that
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHAT_DO_PAIRS = WHAT_DO_PAIRS_01 + \
                WHAT_DO_PAIRS_02
