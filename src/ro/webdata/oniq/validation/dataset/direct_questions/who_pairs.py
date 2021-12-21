WHO_PAIRS_01 = [
    {
        # [1]
        "query": "Who is starring in the film series of Souls of the Departed?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: starring,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: in the film series of Souls of the Departed
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHO_PAIRS_02 = [
    {
        "query": "Who is married with Jane?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [is],
			main_vb: married,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: with Jane
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Who is very beautiful?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
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
		phrase: beautiful
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Who is very beautiful and very smart?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
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
		phrase: beautiful
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
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
		operator: and
		phrase: smart
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Who is the most beautiful woman and the most generous person?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
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
		phrase: the most beautiful woman
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
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
		operator: and
		phrase: the most generous person
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Who is the director of Amsterdam museum?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
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
		phrase: the director of Amsterdam museum
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: ##and## sold
        "query": "Who is the director who own 2 cars and sold a house or a panel?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
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
		phrase: the director
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: the director
		prep_phrase: None
		type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: own,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: 2 cars
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: the director
		prep_phrase: None
		type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: sold,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: a house
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: the director
		prep_phrase: None
		type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: sold,
			modal_vb: None
		}
	},
	related: {
		operator: or
		phrase: a panel
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHO_PAIRS_03 = [
    {
        # [6]
        "query": "Who opened the door?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: who
		prep_phrase: None
		type: who
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: opened,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the door
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHO_PAIRS = WHO_PAIRS_01 + \
            WHO_PAIRS_02 + \
            WHO_PAIRS_03
