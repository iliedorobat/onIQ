WHY_PAIRS = [
    {
        "query": "Why aren't the artifacts in the museum?",
        "result": """
statement: {
	target: {
		phrase: why
		question type: why
	},
	action: {
		neg: n't,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: the artifacts in the museum
		question type: None
	}
}
"""
    }
]
