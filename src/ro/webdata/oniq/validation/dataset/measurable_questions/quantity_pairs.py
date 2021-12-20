QUANTITY_PAIS_01 = [
    {
        "query": "How many paintings are on display at the Amsterdam Museum?",
        "result": """
statement: {
	target: {
		phrase: how many paintings
		question type: count
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
		phrase: on display at the Amsterdam Museum
		question type: None
	}
}
"""
    },
    {
        "query": "How many people visit the Amsterdam Museum?",
        "result": """
statement: {
	target: {
		phrase: how many people
		question type: count
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
		phrase: the Amsterdam Museum
		question type: None
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
		phrase: how many days do I
		question type: count
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
		phrase: until the opening
		question type: None
	}
}
"""
    },
    {
        "query": "How many days do I have to wait for him?",
        "result": """
statement: {
	target: {
		phrase: how many days do I
		question type: count
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
		phrase: for him
		question type: None
	}
}
"""
    },
    {
        # [??]
        "query": "How many monuments are there in vallon-pont-d'arc",
        "result": """
statement: {
	target: {
		phrase: how many monuments
		question type: count
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
		phrase: in vallon-pont
		question type: None
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
		phrase: how much money
		question type: count
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
		phrase: you
		question type: None
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
		phrase: how many cars
		question type: count
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
		phrase: there
		question type: None
	}
}
"""
    }
]

QUANTITY_PAIS = QUANTITY_PAIS_01 + \
                QUANTITY_PAIS_02 + \
                QUANTITY_PAIS_03
