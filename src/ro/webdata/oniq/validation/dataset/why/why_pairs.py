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
    },
    {
        # [6]
        "query": "Why don't I help you?",
        "result": """
statement: {
	target: {
		phrase: why don't I
		question type: why
	},
	action: {
		neg: n't,
		verb: {
			aux_vbs: [do],
			main_vb: help,
			modal_vb: None
		}
	},
	related: {
		phrase: you
		question type: None
	}
}
"""
    },
    {
        # [6]
        "query": "Why do you say that?",
        "result": """
statement: {
	target: {
		phrase: why do you
		question type: why
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [do],
			main_vb: say,
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
