pairs_03 = [
    {
        # [3]
        "query": "When was anıtkabir built?",
        "result": """
statement: {
	target_phrase: when,
	action: {
		dep: ROOT,
		is_available: False,
		neg: None,
		verb: {
			aux_vbs: [was],
			acomp: None,
			main_vb: built,
			modal_vb: None
		}
	},
	conjunction: None,
	related_phrases: anıtkabir
"""
    },
    {
        # [3]
        "query": "What is villa la reine jeanne all about?",
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
	related_phrases: villa la reine jeanne
"""
    }
]
