WHICH_IS_PAIRS_01 = [
    {
        "query": "Which is the most visited museum?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the most visited museum
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest and the largest city?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the noisiest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the largest city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest town and the largest city?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the noisiest town
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the largest city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest and the most beautiful city?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the noisiest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the most beautiful city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest, the most beautiful and the largest city?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the noisiest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the most beautiful
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the largest city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest, the largest and the most crowded city?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the noisiest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the largest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the most crowded city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest and the largest and the most crowded city?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the noisiest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the largest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the most crowded city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest, the newest, the largest and the most crowded city?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the noisiest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the newest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the largest
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## the most crowded city
		question type: None
	}
}
"""
    },
    {
        "query": "Which is the museum which hosts more than 10 pictures and exposed one sword?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the museum
		question type: None
	}
}
statement: {
	target: {
		phrase: the museum
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
		phrase: the museum
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
    }
]

WHICH_IS_PAIRS_02 = [
    {
        # [1]
        # TODO: the state => the state of the Watergate scandal
        "query": "Which is the state and country of the Watergate scandal?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the state
		question type: None
	}
}
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: ##and## country of the Watergate scandal
		question type: None
	}
}
"""
    }
]

WHICH_IS_PAIRS_03 = [
    {
        # derived from [2]
        "query": "Which is the longest and shortest river?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the longest and shortest river
		question type: None
	}
}
"""
    },
    {
        # [2]
        "query": "Which is the longest and shortest river that traverses Mississippi?",
        "result": """
statement: {
	target: {
		phrase: which
		question type: which
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
		phrase: the longest and shortest river
		question type: None
	}
}
statement: {
	target: {
		phrase: the longest and shortest river
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: None,
			main_vb: traverses,
			modal_vb: None
		}
	},
	related: {
		phrase: Mississippi
		question type: None
	}
}
"""
    }
]

WHICH_IS_PAIRS = WHICH_IS_PAIRS_01 + \
                 WHICH_IS_PAIRS_02 + \
                 WHICH_IS_PAIRS_03
