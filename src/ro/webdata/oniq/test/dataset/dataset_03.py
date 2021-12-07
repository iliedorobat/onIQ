WHAT_IS_PAIRS = [
    {
        # [3]
        "query": "What is villa la reine jeanne all about?",
        "result": """
statement: {
	target: {
		phrase: what
		question type: what
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
		phrase: villa la reine jeanne
		question type: None
	}
}
"""
    }
]

WHEN_PAIRS = [
    {
        # [3]
        "query": "When was anıtkabir built?",
        "result": """
statement: {
	target: {
		phrase: when
		question type: when
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [was],
			main_vb: built,
			modal_vb: None
		}
	},
	related: {
		phrase: anıtkabir
		question type: None
	}
}
"""
    },
    {
        "query": "When were swords and shields made?",
        "result": """
statement: {
	target: {
		phrase: when
		question type: when
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [were],
			main_vb: made,
			modal_vb: None
		}
	},
	related: {
		phrase: swords
		question type: None
	}
}
statement: {
	target: {
		phrase: when
		question type: when
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [were],
			main_vb: made,
			modal_vb: None
		}
	},
	related: {
		phrase: ##and## shields
		question type: None
	}
}
"""
    }
]

PAIRS_03 = WHAT_IS_PAIRS + \
           WHEN_PAIRS
