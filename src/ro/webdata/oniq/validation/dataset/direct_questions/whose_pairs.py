WHOSE_PAIRS_01 = [
    {
        "query": "Whose picture is it?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: whose picture
		prep_phrase: None
		type: whose
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
		phrase: it
		prep_phrase: None
		type: None
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
		operator: None
		phrase: whose turn
		prep_phrase: None
		type: whose
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
		phrase: it
		prep_phrase: None
		type: None
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
		operator: None
		phrase: whose
		prep_phrase: None
		type: whose
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
		phrase: these keys
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHOSE_PAIRS = WHOSE_PAIRS_01 + \
              WHOSE_PAIRS_02 + \
              WHOSE_ARE_PAIRS_02
