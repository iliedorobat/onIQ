QUANTITY_PAIS_01 = [
    {
        "query": "How many paintings are on display at the Amsterdam Museum?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how many paintings
		prep_phrase: None
		type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: on display at the Amsterdam Museum
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "How many people visit the Amsterdam Museum?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how many people
		prep_phrase: None
		type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: visit,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the Amsterdam Museum
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: have to wait
        "query": "How many days do I have to wait until the opening?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how many days do I
		prep_phrase: None
		type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [do],
			main_vb: wait,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: until the opening
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "How many days do I have to wait for him?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how many days do I
		prep_phrase: None
		type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [do],
			main_vb: wait,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: for him
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # [??] TODO: get the reference
        "query": "How many monuments are there in vallon-pont-d'arc",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how many monuments
		prep_phrase: None
		type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: in vallon-pont
		prep_phrase: None
		type: None
	}
}
"""
    }
]

QUANTITY_PAIS_02 = [
    {
        # [6]
        "query": "How much money do you have?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how much money
		prep_phrase: None
		type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [do],
			main_vb: have,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: you
		prep_phrase: None
		type: None
	}
}
"""
    }
]

QUANTITY_PAIS_03 = [
    {
        # [6]
        "query": "How many cars are there?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how many cars
		prep_phrase: None
		type: count
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [are],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: there
		prep_phrase: None
		type: None
	}
}
"""
    }
]

QUANTITY_PAIS = QUANTITY_PAIS_01 + \
                QUANTITY_PAIS_02 + \
                QUANTITY_PAIS_03
