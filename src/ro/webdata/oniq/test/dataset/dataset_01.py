pairs_01 = [
    {
        # [1]
        "query": "Which is the state and country of the Watergate scandal?",
        "result": """
statement: {
	target_chunks: [Which],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the state
}
statement: {
	target_chunks: [Which],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: country of the Watergate scandal
}
"""
    },
    {
        # [1]
        "query": "What is the federated state located in the Weimar Republic?",
        "result": """
statement: {
	target_chunks: [What],
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the federated state
}
statement: {
	target_chunks: [the federated state],
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: located,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: the Weimar Republic
}
"""
    }
]
