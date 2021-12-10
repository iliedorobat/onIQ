AGE_PAIRS = [
    {
        # [6]
        "query": "How old are you?",
        "result": """
statement: {
	target: {
		phrase: how old
		question type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
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
