HOW_FAR_PAIRS_01 = [
    {
        # [6]
        "query": "How far is Pattaya from Bangkok?",
        "result": """
statement: {
	target: {
		phrase: how far
		question type: how
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: Pattaya from Bangkok
		question type: None
	}
}
"""
    }
]

DISTANCE_PAIRS = HOW_FAR_PAIRS_01
