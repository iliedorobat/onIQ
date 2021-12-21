WHERE_DO_PAIRS_01 = [
    {
        # derived from [1]
        "query": "Where did Lena Horne receive the Grammy Award for Best Jazz Vocal Album?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: where did Lena Horne
		prep_phrase: None
		type: where
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

WHERE_DO_PAIRS_02 = [
    {
        # [6]
        "query": "Where do they live?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: where
		prep_phrase: None
		type: where
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
		operator: None
		phrase: they
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHERE_DO_PAIRS_03 = [

    {
        # [1]
        "query": "Where does the holder of the position of Lech Kaczynski live?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: where
		prep_phrase: None
		type: where
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
		operator: None
		phrase: the holder of the position of Lech Kaczynski
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Where does the engineer go?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: where
		prep_phrase: None
		type: where
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
		operator: None
		phrase: the engineer
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Where does the best architect live?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: where
		prep_phrase: None
		type: where
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
		operator: None
		phrase: the best architect
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHERE_DO_PAIRS = WHERE_DO_PAIRS_01 + \
                 WHERE_DO_PAIRS_02 + \
                 WHERE_DO_PAIRS_03
