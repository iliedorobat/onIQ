WHERE_DO_PAIRS_01 = [
    {
        # derived from [1]
        "query": "Where did Lena Horne receive the Grammy Award for Best Jazz Vocal Album?",
        "result": """
statement: {
	target: {
		phrase: where did Lena Horne
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [did],
			main_vb: receive,
			modal_vb: None
		}
	},
	related: {
		phrase: the Grammy Award for Best Jazz Vocal Album
		question type: None
	}
}
"""
    }
]

WHERE_DO_PAIRS = WHERE_DO_PAIRS_01
