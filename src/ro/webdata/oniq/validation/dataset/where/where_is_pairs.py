WHERE_IS_PAIRS_01 = [
    {
        "query": "Where is the museum?",
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
"""
    },
    {
        "query": "Where is the museum located?",
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
			aux_vbs: [is],
			main_vb: located,
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
"""
    },
    {
        "query": "Where is the black picture?",
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
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the black picture
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Where is the picture with the black frame?",
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
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the picture with the black frame
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: ilie.dorobat: swords => the swords
        "query": "Where are the coins and swords located?",
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
			aux_vbs: [are],
			main_vb: located,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the coins
		prep_phrase: None
		type: None
	}
}
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
			aux_vbs: [are],
			main_vb: located,
			modal_vb: None
		}
	},
	related: {
		operator: and
		phrase: swords
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Where was the picture with the black frame stolen?",
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
			aux_vbs: [was],
			main_vb: stolen,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the picture with the black frame
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Where was the last place the picture was exposed?",
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
			aux_vbs: [was],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the last place
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: the last place
		prep_phrase: None
		type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [was],
			main_vb: exposed,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the picture
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # [5]
        # NOTICE: "adam mickiewicz" is the named_entity but not "adam mickiewicz monument"
        "query": "Where is adam mickiewicz monument?",
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
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: adam mickiewicz monument
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Where is the Museum of Amsterdam?",
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
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the Museum of Amsterdam
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        # TODO: ilie.dorobat: axes => the axes
        "query": "Where are the swords and axes made?",
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
			aux_vbs: [are],
			main_vb: made,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the swords
		prep_phrase: None
		type: None
	}
}
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
			aux_vbs: [are],
			main_vb: made,
			modal_vb: None
		}
	},
	related: {
		operator: and
		phrase: axes
		prep_phrase: None
		type: None
	}
}
"""
    },

    {
        "query": "Where is the woman in black?",
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
			aux_vbs: [is],
			main_vb: None,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: the woman in black
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHERE_IS_PAIRS = WHERE_IS_PAIRS_01
