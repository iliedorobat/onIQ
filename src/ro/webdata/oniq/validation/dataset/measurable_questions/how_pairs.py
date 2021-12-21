from ro.webdata.oniq.validation.dataset.measurable_questions.age_pairs import AGE_PAIRS
from ro.webdata.oniq.validation.dataset.measurable_questions.distance_pairs import DISTANCE_PAIRS
from ro.webdata.oniq.validation.dataset.measurable_questions.quantity_pairs import QUANTITY_PAIS
from ro.webdata.oniq.validation.dataset.measurable_questions.length_pairs import TIME_SPACE_PAIRS

HOW_IS_PAIRS = [
    {
        # [6]
        "query": "How was your exam?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how
		prep_phrase: None
		type: how
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
		phrase: your exam
		prep_phrase: None
		type: None
	}
}
"""
    }
]

INFORMAL_PAIRS = [
    {
        # [6]
        "query": "How come I can't see her?",
        "result": """
statement: {
	target: {
		operator: None
		phrase: how come I
		prep_phrase: None
		type: how
	},
	action: {
		neg: n't,
		verb: {
			aux_vbs: [ca],
			main_vb: see,
			modal_vb: None
		}
	},
	related: {
		operator: None
		phrase: her
		prep_phrase: None
		type: None
	}
}
"""
    }
]

HOW_PAIRS = AGE_PAIRS + \
            DISTANCE_PAIRS + \
            HOW_IS_PAIRS + \
            INFORMAL_PAIRS + \
            QUANTITY_PAIS + \
            TIME_SPACE_PAIRS
