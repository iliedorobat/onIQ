pairs_01 = [
    {
        # [1]
        "query": "Which is the state and country of the Watergate scandal?",
        "result": """
statement: {
	target_phrase: which,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the state

statement: {
	target_phrase: which,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: and,
	related_phrases: country of the Watergate scandal
"""
    },
    {
        # [1]
        "query": "What is the federated state located in the Weimar Republic?",
        "result": """
statement: {
	target_phrase: what,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [is],
			acomp: None,
			main_vb: None,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: the federated state

statement: {
	target_phrase: the federated state,
	action: {
		dep: acl,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: None,
			acomp: None,
			main_vb: located,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: in the Weimar Republic
"""
    }
]
