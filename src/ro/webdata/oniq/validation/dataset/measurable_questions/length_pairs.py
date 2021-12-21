# Length of time or space

HOW_LONG_PAIRS_01 = [
    {
        "query": "How long is the journey?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how long
		prep_phrase: None
		type: how
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
		operator: None
		phrase: the journey
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "How long does the museum remain closed?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how long does the museum
		prep_phrase: None
		type: how
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
		operator: None
		phrase: closed
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "How long does the largest museum remain closed?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how long does the largest museum
		prep_phrase: None
		type: how
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
		operator: None
		phrase: closed
		prep_phrase: None
		type: None
	}
}
"""
    }
]

HOW_LONG_PAIRS_02 = [
    {
        # [6]
        "query": "How long will it take?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how long
		prep_phrase: None
		type: how
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [will],
			main_vb: take,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: it
		prep_phrase: None
		type: None
	}
}
"""
    }
]

TIME_SPACE_PAIRS = HOW_LONG_PAIRS_01 + \
                   HOW_LONG_PAIRS_02
