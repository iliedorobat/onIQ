pairs_03 = [
    {
        # [3]
        "query": "When was anıtkabir built?",
        "result": """
statement: {
	target_chunks: [When],
	action: {
		neg: None,
		verb: {
			aux_vbs: [was],
			main_vb: built,
			modal_vb: None
		},
		acomp_list: []
	},
	related_chunk: anıtkabir
}
"""
    },
    {
        # [3]
        "query": "What is villa la reine jeanne all about?",
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
	related_chunk: villa la reine jeanne
}
"""
    }
]
