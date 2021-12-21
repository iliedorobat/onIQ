WHEN_IS_PAIRS_01 = [
    {
        # [3]
        "query": "When was anıtkabir built?",
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
			aux_vbs: [was],
			main_vb: built,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: anıtkabir
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "When were swords and shields made?",
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
			aux_vbs: [were],
			main_vb: made,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: swords
		prep_phrase: None
		type: None
	}
}
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
			aux_vbs: [were],
			main_vb: made,
			modal_vb: None
		}
	},
	related: {
		operator: and
		phrase: shields
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHEN_IS_PAIRS_02 = [
    {
        # [1]
        "query": "When was Carl Sagan married Ann Druyan?",
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
			aux_vbs: [was],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: Carl Sagan
		prep_phrase: None
		type: None
	}
}
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
			aux_vbs: [was],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: Ann Druyan
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: Per Ahlmark => to Per Ahlmark
        # [1]
        "query": "When was Bibi Andersson married to Per Ahlmark?",
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
			aux_vbs: [was],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: Bibi Andersson
		prep_phrase: None
		type: None
	}
}
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
			aux_vbs: [was],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: Per Ahlmark
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHEN_IS_PAIRS = WHEN_IS_PAIRS_01 + \
                WHEN_IS_PAIRS_02
