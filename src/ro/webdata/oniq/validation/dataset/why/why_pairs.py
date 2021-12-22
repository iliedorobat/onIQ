WHY_PAIRS_01 = [
    {
        "query": "Why aren't the artifacts in the museum?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: why
		prep_phrase: None
		type: why
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
		operator: None
		phrase: the artifacts
		prep_phrase: the museum
		type: None
	}
}
"""
    }
]

WHY_PAIRS_02 = [
    {
        # [6]
        "query": "Why don't I help you?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: why don't I
		prep_phrase: None
		type: why
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
		operator: None
		phrase: you
		prep_phrase: None
		type: None
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
		operator: None
		phrase: why do you
		prep_phrase: None
		type: why
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
		operator: None
		phrase: that
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHY_PAIRS = WHY_PAIRS_01 + \
            WHY_PAIRS_02
