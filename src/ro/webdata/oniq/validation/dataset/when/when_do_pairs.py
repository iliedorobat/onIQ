WHEN_DO_PAIRS_01 = [
    {
        # [1]
        "query": "When did Lena Horne receive the Grammy Award for Best Jazz Vocal Album?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: when did Lena Horne
		prep_phrase: None
		type: when
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
		operator: None
		phrase: the Grammy Award for Best Jazz Vocal Album
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHEN_DO_PAIRS = WHEN_DO_PAIRS_01
