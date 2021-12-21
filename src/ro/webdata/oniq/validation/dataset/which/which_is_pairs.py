WHICH_IS_PAIRS_01 = [
    {
        "query": "Which is the most visited museum?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the most visited museum
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: ilie.dorobat the noisiest => the noisiest city
        "query": "Which is the noisiest and the largest city?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the noisiest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the largest city
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Which is the noisiest town and the largest city?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the noisiest town
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the largest city
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: the noisiest => the noisiest city
        "query": "Which is the noisiest and the most beautiful city?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the noisiest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the most beautiful city
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: the noisiest; the most beautiful => the noisiest city; the most beautiful city
        "query": "Which is the noisiest, the most beautiful and the largest city?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the noisiest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the most beautiful
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the largest city
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: the noisiest; the largest => the noisiest city; the largest city
        "query": "Which is the noisiest, the largest and the most crowded city?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the noisiest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the largest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the most crowded city
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: the noisiest; the largest => the noisiest city; the largest city
        "query": "Which is the noisiest and the largest and the most crowded city?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the noisiest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the largest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the most crowded city
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: the noisiest; the newest; the largest => the noisiest city; the newest city; the largest city
        "query": "Which is the noisiest, the newest, the largest and the most crowded city?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the noisiest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the newest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the largest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the most crowded city
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: ilie.dorobat: expposed one sword => and exposed one sword
        "query": "Which is the museum which hosts more than 10 pictures and exposed one sword?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the museum
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: the museum
		prep_phrase: None
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
		phrase: the museum
		prep_phrase: None
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
    }
]

WHICH_IS_PAIRS_02 = [
    {
        # [1]
        # TODO: ilie.dorobat: the state => the state of the Watergate scandal
        "query": "Which is the state and country of the Watergate scandal?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the state
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: country of the Watergate scandal
		prep_phrase: None
		type: None
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
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the longest and shortest river
		prep_phrase: None
		type: None
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
		operator: None
		phrase: which
		prep_phrase: None
		type: which
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
		phrase: the longest and shortest river
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: the longest and shortest river
		prep_phrase: None
		type: None
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
		operator: None
		phrase: Mississippi
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHICH_IS_PAIRS = WHICH_IS_PAIRS_01 + \
                 WHICH_IS_PAIRS_02 + \
                 WHICH_IS_PAIRS_03
