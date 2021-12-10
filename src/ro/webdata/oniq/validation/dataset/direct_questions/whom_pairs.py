WHOM_PAIRS_01 = [
    {
        # [6]
        "query": "Whom did you see?",
        "result": """
statement: {
	target: {
		phrase: whom
		question type: whom
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
		phrase: you
		question type: None
	}
}
"""
    }
]

WHOM_PAIRS = WHOM_PAIRS_01
