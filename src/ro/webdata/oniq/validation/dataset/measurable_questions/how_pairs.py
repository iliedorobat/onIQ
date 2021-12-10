from ro.webdata.oniq.validation.dataset.measurable_questions.distance_pairs import DISTANCE_PAIRS
from ro.webdata.oniq.validation.dataset.measurable_questions.age_pairs import AGE_PAIRS
from ro.webdata.oniq.validation.dataset.measurable_questions.quantity_pairs import QUANTITY_PAIS
from ro.webdata.oniq.validation.dataset.measurable_questions.length_pairs import TIME_SPACE_PAIRS

HOW_IS_PAIRS = [
    {
        # [6]
        "query": "How was your exam?",
        "result": """
statement: {
	target: {
		phrase: how
		question type: how
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
		phrase: your exam
		question type: None
	}
}
"""
    }
]

HOW_PAIRS = AGE_PAIRS + \
            DISTANCE_PAIRS + \
            QUANTITY_PAIS + \
            TIME_SPACE_PAIRS
