WHO_PAIRS_01 = [
    {
        # [1]
        "query": "Who is starring in the film series of Souls of the Departed?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: in the film series of Souls of the Departed
		question type: None
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
		phrase: who
		question type: who
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
		phrase: with Jane
		question type: None
	}
}
"""
    },
    {
        "query": "Who is very beautiful?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: beautiful
		question type: None
	}
}
"""
    },
    {
        "query": "Who is very beautiful and very smart?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: beautiful
		question type: None
	}
}
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: ##and## smart
		question type: None
	}
}
"""
    },
    {
        "query": "Who is the most beautiful woman and the most generous person?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: the most beautiful woman
		question type: None
	}
}
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: ##and## the most generous person
		question type: None
	}
}
"""
    },
    {
        "query": "Who is the director of Amsterdam museum?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: the director of Amsterdam museum
		question type: None
	}
}
"""
    },
    {
        "query": "Who is the director who own 2 cars and sold a house or a panel?",
        "result": """
statement: {
	target: {
		phrase: who
		question type: who
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
		phrase: the director
		question type: None
	}
}
statement: {
	target: {
		phrase: the director
		question type: None
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
		phrase: 2 cars
		question type: None
	}
}
statement: {
	target: {
		phrase: the director
		question type: None
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
		phrase: a house
		question type: None
	}
}
statement: {
	target: {
		phrase: the director
		question type: None
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
		phrase: ##or## a panel
		question type: None
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
		phrase: who
		question type: who
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
		phrase: the door
		question type: None
	}
}
"""
    }
]

WHO_PAIRS = WHO_PAIRS_01 + WHO_PAIRS_02 + WHO_PAIRS_03
