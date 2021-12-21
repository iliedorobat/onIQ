WHAT_PAIRS_01 = [
    {
        "query": "What museums and libraries are there in Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what museums
		prep_phrase: None
		type: what
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
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: what libraries
		prep_phrase: None
		type: what
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
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "What museums and libraries are in Bacau or Bucharest?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what museums
		prep_phrase: None
		type: what
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
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: what museums
		prep_phrase: None
		type: what
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
		operator: or
		phrase: in Bucharest
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: what libraries
		prep_phrase: None
		type: what
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
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: and
		phrase: what libraries
		prep_phrase: None
		type: what
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
		operator: or
		phrase: in Bucharest
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "What museums are in Bacau or Bucharest?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what museums
		prep_phrase: None
		type: what
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
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: what museums
		prep_phrase: None
		type: what
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
		operator: or
		phrase: in Bucharest
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "What museums are in Bacau, Iasi or Bucharest?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what museums
		prep_phrase: None
		type: what
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
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: what museums
		prep_phrase: None
		type: what
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
		operator: or
		phrase: in Iasi
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: None
		phrase: what museums
		prep_phrase: None
		type: what
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
		operator: or
		phrase: in Bucharest
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "What sharp swords, very beautiful paintings, or tall statues are in Bacau?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: what sharp swords
		prep_phrase: None
		type: what
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
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: what very beautiful paintings
		prep_phrase: None
		type: what
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
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
statement: {
	target: {
		operator: or
		phrase: what tall statues
		prep_phrase: None
		type: what
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
		phrase: in Bacau
		prep_phrase: None
		type: None
	}
}
"""
    }
]

WHAT_PAIRS = WHAT_PAIRS_01
