WHERE_PAIRS_01 = [
    {
        # [1]
        "query": "Where does the holder of the position of Lech Kaczynski live?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: live,
			modal_vb: None
		}
	},
	related: {
		phrase: the holder of the position of Lech Kaczynski
		question type: None
	}
}
"""
    },
    {
        "query": "Where does the engineer go?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: go,
			modal_vb: None
		}
	},
	related: {
		phrase: the engineer
		question type: None
	}
}
"""
    },
    {
        # [5]
        "query": "Where can one find farhad and shirin monument?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [can],
			main_vb: find,
			modal_vb: None
		}
	},
	related: {
		phrase: farhad and shirin monument
		question type: None
	}
}
"""
    }
]

WHERE_PAIRS_02 = [
    {
        # [6]
        "query": "Where do they live?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [do],
			main_vb: live,
			modal_vb: None
		}
	},
	related: {
		phrase: they
		question type: None
	}
}
"""
    }
]

WHERE_PAIRS_03 = [
    {
        "query": "Where does the best architect live?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [does],
			main_vb: live,
			modal_vb: None
		}
	},
	related: {
		phrase: the best architect
		question type: None
	}
}
"""
    }
]

WHERE_PAIRS = WHERE_PAIRS_01 + WHERE_PAIRS_02
