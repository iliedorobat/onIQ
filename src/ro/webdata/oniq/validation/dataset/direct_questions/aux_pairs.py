DID_PAIRS = [
    {
        "query": "Did James work with Andrew?",
        "result": """
statement: {
	target: {
		phrase: James
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [Did],
			main_vb: work,
			modal_vb: None
		}
	},
	related: {
		phrase: with Andrew
		question type: None
	}
}
"""
    },
    {
        "query": "Did Steve Sampson manage a club of Santa Clara university?",
        "result": """
statement: {
	target: {
		phrase: Steve Sampson
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [Did],
			main_vb: manage,
			modal_vb: None
		}
	},
	related: {
		phrase: a club of Santa Clara university
		question type: None
	}
}
"""
    },
    {
        "query": "Did it rain most often at the beginning of the year?",
        "result": """
statement: {
	target: {
		phrase: it
		question type: None
	},
	action: {
		neg: None,
		verb: {
			aux_vbs: [Did],
			main_vb: rain,
			modal_vb: None
		}
	},
	related: {
		phrase: at the beginning of the year
		question type: None
	}
}
"""
    }
]

DO_PAIRS = [
#     {
#         # TODO: phrase: Prince William => phrase: ##and## Prince William
#         # [1]
#         "query": "Do Prince Harry and Prince William have the same parents?",
#         "result": """
# statement: {
# 	target: {
# 		phrase: Prince Harry
# 		question type: None
# 	},
# 	action: {
# 		neg: None,
# 		verb: {
# 			aux_vbs: [Do],
# 			main_vb: have,
# 			modal_vb: None
# 		}
# 	},
# 	related: {
# 		phrase: the same parents
# 		question type: None
# 	}
# }
# statement: {
# 	target: {
# 		phrase: Prince William
# 		question type: None
# 	},
# 	action: {
# 		neg: None,
# 		verb: {
# 			aux_vbs: [Do],
# 			main_vb: have,
# 			modal_vb: None
# 		}
# 	},
# 	related: {
# 		phrase: the same parents
# 		question type: None
# 	}
# }
# """
#     }
]
