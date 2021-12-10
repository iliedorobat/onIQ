WHEN_PAIRS_01 = [
    #     {
    #         # FIXME:
    #         "query": "When does the museum open?",
    #         "result": """
    #
    # """
    #     }
]

WHEN_PAIRS_02 = [
    {
        # [6]
        "query": "When did he leave?",
        "result": """
statement: {
	target: {
		phrase: when
		question type: when
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [did],
			main_vb: leave,
			modal_vb: None
		}
	},
	related: {
		phrase: he
		question type: None
	}
}
"""
    }
]

WHEN_PAIRS = WHEN_PAIRS_01 + WHEN_PAIRS_02
