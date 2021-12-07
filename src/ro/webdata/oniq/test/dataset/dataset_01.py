WHICH_IS_PAIRS = [
    {
        # [1]
        # TODO: the state => the state of the Watergate scandal
        "query": "Which is the state and country of the Watergate scandal?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the state
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## country of the Watergate scandal
		question type: None
	}
}
"""
    },
    {
        # [1]
        "query": "What is the federated state located in the Weimar Republic?",
        "result": """
statement: {
	target: {
		phrase: what
		question type: what
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
		phrase: the federated state
		question type: None
	}
}
statement: {
	target: {
		phrase: the federated state
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: located,
			modal_vb: None
		}
	},
	related: {
		phrase: in the Weimar Republic
		question type: None
	}
}
"""
    }
]

PAIRS_01 = WHICH_IS_PAIRS
