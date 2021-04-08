WHICH_IS_PAIRS = [
    {
        # [1]
        # TODO: improve the statement structure
        "query": "Which is the state and country of the Watergate scandal?",
        "result": """
statement: {
	target phrase: which,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the state
}
statement: {
	target phrase: which,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: ##and## country
}
statement: {
	target phrase: the state,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: of the Watergate scandal
}
statement: {
	target phrase: ##and## country,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: of the Watergate scandal
}
"""
    },
    {
        # [1]
        "query": "What is the federated state located in the Weimar Republic?",
        "result": """
statement: {
	target phrase: what,
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: the federated state
}
statement: {
	target phrase: the federated state,
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related phrase: in the Weimar Republic
}
"""
    }
]

PAIRS_01 = WHICH_IS_PAIRS
