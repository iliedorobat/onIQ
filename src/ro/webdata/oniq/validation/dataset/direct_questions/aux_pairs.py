DID_PAIRS = [
    {
        "query": "Did James work with Andrew?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: James
		prep_phrase: None
		type: None
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
		operator: None
		phrase: with Andrew
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Did Steve Sampson manage a club of Santa Clara university?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: Steve Sampson
		prep_phrase: None
		type: None
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
		operator: None
		phrase: a club of Santa Clara university
		prep_phrase: None
		type: None
	}
}
"""
    },
    {
        "query": "Did it rain most often at the beginning of the year?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: it
		prep_phrase: None
		type: None
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
		operator: None
		phrase: at the beginning of the year
		prep_phrase: None
		type: None
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
