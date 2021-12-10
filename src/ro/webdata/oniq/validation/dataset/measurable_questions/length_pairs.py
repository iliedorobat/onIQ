HOW_LONG_PAIRS_01 = [
    {
        "query": "How long is the journey?",
        "result": """
statement: {
	target: {
		phrase: how long
		question type: how
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		phrase: the journey
		question type: None
	}
}
"""
    },
    {
        "query": "How long does the museum remain closed?",
        "result": """
statement: {
	target: {
		phrase: how long does the museum
		question type: how
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: remain,
			modal_vb: None
		}
	},
	related: {
		phrase: closed
		question type: None
	}
}
"""
    },
    {
        "query": "How long does the largest museum remain closed?",
        "result": """
statement: {
	target: {
		phrase: how long does the largest museum
		question type: how
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: remain,
			modal_vb: None
		}
	},
	related: {
		phrase: closed
		question type: None
	}
}
"""
    }
]

TIME_SPACE_PAIRS = HOW_LONG_PAIRS_01
