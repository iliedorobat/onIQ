WHOSE_PAIRS_01 = [
    {
        "query": "Whose picture is it?",
        "result": """
statement: {
	target: {
		phrase: whose picture
		question type: whose
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
		phrase: it
		question type: None
	}
}
"""
    }
]

WHOSE_PAIRS_02 = [
    {
        # [6]
        "query": "Whose turn is it?",
        "result": """
statement: {
	target: {
		phrase: whose turn
		question type: whose
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
		phrase: it
		question type: None
	}
}
"""
    }
]

WHOSE_ARE_PAIRS_02 = [
    {
        # [6]
        "query": "Whose are these keys?",
        "result": """
statement: {
	target: {
		phrase: whose
		question type: whose
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
		phrase: these keys
		question type: None
	}
}
"""
    }
]

WHOSE_PAIRS = WHOSE_PAIRS_01 + WHOSE_PAIRS_02
