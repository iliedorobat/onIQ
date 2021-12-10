WHAT_PAIRS = [
    {
        "query": "What museums and libraries are there in Bacau?",
        "result": """
statement: {
	target: {
		phrase: what museums
		question type: what
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
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## what libraries
		question type: what
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
		phrase: in Bacau
		question type: None
	}
}
"""
    },
    {
        "query": "What museums and libraries are in Bacau or Bucharest?",
        "result": """
statement: {
	target: {
		phrase: what museums
		question type: what
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
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: what museums
		question type: what
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
		phrase: ##or## in Bucharest
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## what libraries
		question type: what
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
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##and## what libraries
		question type: what
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
		phrase: ##or## in Bucharest
		question type: None
	}
}
"""
    },
    {
        "query": "What museums are in Bacau or Bucharest?",
        "result": """
statement: {
	target: {
		phrase: what museums
		question type: what
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
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: what museums
		question type: what
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
		phrase: ##or## in Bucharest
		question type: None
	}
}
"""
    },
    {
        "query": "What museums are in Bacau, Iasi or Bucharest?",
        "result": """
statement: {
	target: {
		phrase: what museums
		question type: what
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
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: what museums
		question type: what
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
		phrase: ##or## in Iasi
		question type: None
	}
}
statement: {
	target: {
		phrase: what museums
		question type: what
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
		phrase: ##or## in Bucharest
		question type: None
	}
}
"""
    },
    {
        "query": "What sharp swords, very beautiful paintings, or tall statues are in Bacau?",
        "result": """
statement: {
	target: {
		phrase: what sharp swords
		question type: what
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
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## what very beautiful paintings
		question type: what
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
		phrase: in Bacau
		question type: None
	}
}
statement: {
	target: {
		phrase: ##or## what tall statues
		question type: what
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
		phrase: in Bacau
		question type: None
	}
}
"""
    }
]
