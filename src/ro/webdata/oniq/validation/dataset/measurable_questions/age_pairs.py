AGE_PAIRS = [
    {
        # [6]
        "query": "How old are you?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how old
		prep_phrase: None
		type: count
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
		operator: None
		phrase: you
		prep_phrase: None
		type: None
	}
}
"""
    }
]
