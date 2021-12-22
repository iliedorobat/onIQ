WHAT_IS_PAIRS_01 = [
    {
        # [3]
        "query": "What is villa la reine jeanne all about?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: villa la reine jeanne
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "What is the most beautiful museum?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: the most beautiful museum
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "What is the name of the largest museum?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: the name
		prep_phrase: the largest museum
		type: None
	}
}
"""
    },
    {
        "query": "What is the name of the most beautiful museum?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: the name
		prep_phrase: the most beautiful museum
		type: None
	}
}
"""
    },
    {
        # TODO: ilie.dorobat: ##and## exposed
        "query": "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: the name
		prep_phrase: the largest museum
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: the name
		prep_phrase: the largest museum
		type: None
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
		operator: None
		phrase: more than 10 pictures
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: the name
		prep_phrase: the largest museum
		type: None
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
		operator: None
		phrase: one sword
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "What is the most beautiful place and the largest cave?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: the most beautiful place
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: the largest cave
		prep_phrase: None
		type: None
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
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: the federated state
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: the federated state
		prep_phrase: None
		type: None
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
		operator: None
		phrase: in the Weimar Republic
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHAT_IS_PAIRS_03 = [
    {
        # [2]
        "query": "What is the population and area of the most populated state?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: the population
		prep_phrase: the most populated state
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: area
		prep_phrase: the most populated state
		type: None
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
		operator: None
		phrase: what
		prep_phrase: None
		type: what
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
		phrase: your name
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHAT_IS_PAIRS = WHAT_IS_PAIRS_01 + \
                WHAT_IS_PAIRS_02 + \
                WHAT_IS_PAIRS_03 + \
                WHAT_IS_PAIRS_04
