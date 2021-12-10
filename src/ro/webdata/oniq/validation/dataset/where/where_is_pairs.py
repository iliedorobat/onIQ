WHERE_IS_PAIRS = [
    {
        "query": "Where is the museum?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
"""
    },
    {
        "query": "Where is the museum located?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the museum
		question type: None
	}
}
"""
    },
    {
        "query": "Where is the black picture?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the black picture
		question type: None
	}
}
"""
    },
    {
        "query": "Where is the picture with the black frame?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the picture with the black frame
		question type: None
	}
}
"""
    },
    {
        "query": "Where are the coins and swords located?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the coins
		question type: None
	}
}
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: ##and## swords
		question type: None
	}
}
"""
    },
    {
        "query": "Where was the picture with the black frame stolen?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the picture with the black frame
		question type: None
	}
}
"""
    },
    {
        "query": "Where was the last place the picture was exposed?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the last place
		question type: None
	}
}
statement: {
	target: {
		phrase: the last place
		question type: None
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
		phrase: the picture
		question type: None
	}
}
"""
    },
    {
        # [5]
        # NOTICE: "adam mickiewicz" is the named_entity and not "adam mickiewicz monument"
        "query": "Where is adam mickiewicz monument?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: adam mickiewicz monument
		question type: None
	}
}
"""
    },
    {
        "query": "Where is the Museum of Amsterdam?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the Museum of Amsterdam
		question type: None
	}
}
"""
    },
    {
        "query": "Where are the swords and axes made?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the swords
		question type: None
	}
}
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: ##and## axes
		question type: None
	}
}
"""
    },

    {
        "query": "Where is the woman in black?",
        "result": """
statement: {
	target: {
		phrase: where
		question type: where
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
		phrase: the woman in black
		question type: None
	}
}
"""
    }
]
