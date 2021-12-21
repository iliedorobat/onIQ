HOW_FAR_PAIRS_01 = [
    {
        # [6]
        "query": "How far is Pattaya from Bangkok?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how far
		prep_phrase: None
		type: how
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
		operator: None
		phrase: Pattaya from Bangkok
		prep_phrase: None
		type: None
	}
}
"""
    }
]

DISTANCE_PAIRS = HOW_FAR_PAIRS_01
