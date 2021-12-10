WHAT_IS_PAIRS_01 = [
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
    },
    {
        "query": "What is the most beautiful museum?",
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
		phrase: the most beautiful museum
		question type: None
	}
}
"""
    },
    {
        "query": "What is the name of the largest museum?",
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
		phrase: the name of the largest museum
		question type: None
	}
}
"""
    },
    {
        "query": "What is the name of the most beautiful museum?",
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
		phrase: the name of the most beautiful museum
		question type: None
	}
}
"""
    },
    {
        "query": "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?",
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
		phrase: the name of the largest museum
		question type: None
	}
}
statement: {
	target: {
		phrase: the name of the largest museum
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: hosts,
			modal_vb: None
		}
	},
	related: {
		phrase: more than 10 pictures
		question type: None
	}
}
statement: {
	target: {
		phrase: the name of the largest museum
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: exposed,
			modal_vb: None
		}
	},
	related: {
		phrase: one sword
		question type: None
	}
}
"""
    },
    {
        "query": "What is the most beautiful place and the largest cave?",
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
		phrase: the most beautiful place
		question type: None
	}
}
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
		phrase: ##and## the largest cave
		question type: None
	}
}
"""
    }
]

WHAT_IS_PAIRS_02 = [
    {
        # [1]
        "query": "What is the federated state located in the Weimar Republic?",
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
		phrase: the federated state
		question type: None
	}
}
statement: {
	target: {
		phrase: the federated state
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: located,
			modal_vb: None
		}
	},
	related: {
		phrase: in the Weimar Republic
		question type: None
	}
}
"""
    }
]

WHAT_IS_PAIRS_03 = [
    {
        # [2]
        # TODO: the population => the population of the most populated state
        "query": "What is the population and area of the most populated state?",
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
		phrase: the population
		question type: None
	}
}
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
		phrase: ##and## area of the most populated state
		question type: None
	}
}
"""
    }
]

WHAT_IS_PAIRS_04 = [
    {
        # [6]
        "query": "What is your name?",
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
		phrase: your name
		question type: None
	}
}
"""
    }
]

WHAT_IS_PAIRS = WHAT_IS_PAIRS_01 + \
                WHAT_IS_PAIRS_02 + \
                WHAT_IS_PAIRS_03
