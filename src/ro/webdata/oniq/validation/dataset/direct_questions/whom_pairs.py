WHOM_PAIRS_01 = [
    {
        # [6]
        "query": "Whom did you see?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: whom
		prep_phrase: None
		type: whom
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [did],
			main_vb: see,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: you
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHOM_PAIRS = WHOM_PAIRS_01
