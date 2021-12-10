WHEN_IS_PAIRS_01 = [
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

WHEN_IS_PAIRS_02 = [
    {
        # [1]
        "query": "When was Carl Sagan married Ann Druyan?",
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
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		phrase: Carl Sagan
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
			aux_vbs: [was],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		phrase: Ann Druyan
		question type: None
	}
}
"""
    },
    {
        # [1]
        "query": "When was Bibi Andersson married to Per Ahlmark?",
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
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		phrase: Bibi Andersson
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
			aux_vbs: [was],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		phrase: Per Ahlmark
		question type: None
	}
}
"""
    }
]

WHEN_IS_PAIRS = WHEN_IS_PAIRS_01 + WHEN_IS_PAIRS_02
