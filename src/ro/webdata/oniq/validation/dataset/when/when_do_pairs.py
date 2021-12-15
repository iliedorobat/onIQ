WHEN_DO_PAIRS_01 = [
    {
        # [1]
        "query": "When did Lena Horne receive the Grammy Award for Best Jazz Vocal Album?",
        "result": """
statement: {
	target: {
		phrase: when did Lena Horne
		question type: when
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

WHEN_DO_PAIRS = WHEN_DO_PAIRS_01
