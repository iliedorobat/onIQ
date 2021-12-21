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
		operator: None
		phrase: when
		prep_phrase: None
		type: when
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
		operator: None
		phrase: he
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHEN_PAIRS = WHEN_PAIRS_01 + \
             WHEN_PAIRS_02
