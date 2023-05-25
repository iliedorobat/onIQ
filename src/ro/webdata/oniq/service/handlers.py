from urllib.parse import unquote

from ro.webdata.oniq.endpoint.common.match.PropertiesMatcher import PropertiesMatcher
from ro.webdata.oniq.endpoint.common.translator.CSVTranslator import CSVTranslator
from ro.webdata.oniq.service.query_const import ACCESSORS, JOIN_OPERATOR, PAIR_SEPARATOR
from ro.webdata.oniq.spacy_model import nlp_model

props = CSVTranslator.to_props()


def entities_handler(parsed):
    output = {}

    for query in parsed.query.split(JOIN_OPERATOR):
        [key, value] = query.split(PAIR_SEPARATOR)
        question = unquote(value)

        if key == ACCESSORS.QUESTION:
            output[ACCESSORS.QUESTION] = question
            output[ACCESSORS.ENTITIES] = _get_json_entities(question)


def matcher_handler(parsed):
    start_i = -1
    end_i = -1
    target_expression = None
    result_type = None
    document = None
    question = None

    for query in parsed.query.split(JOIN_OPERATOR):
        [key, value] = query.split(PAIR_SEPARATOR)

        if key == ACCESSORS.QUESTION:
            question = unquote(value)
            document = nlp_model(question)
        elif key == ACCESSORS.START_I:
            start_i = int(value)
        elif key == ACCESSORS.END_I:
            end_i = int(value)
        elif key == ACCESSORS.RESULT_TYPE:
            result_type = value

    if start_i == -1 or end_i == -1:
        return {
            ACCESSORS.QUESTION: question,
            ACCESSORS.START_I: start_i,
            ACCESSORS.END_I: end_i,
            ACCESSORS.PROPERTY: None,
            ACCESSORS.SCORE: -1
        }

    target_expression = document[start_i, end_i]
    best_matched = PropertiesMatcher.get_best_matched(props, target_expression, result_type)

    return {
        ACCESSORS.QUESTION: question,
        ACCESSORS.START_I: start_i,
        ACCESSORS.END_I: end_i,
        ACCESSORS.PROPERTY: best_matched.property.serialize(),
        ACCESSORS.SCORE: best_matched.score
    }


# TODO: remove
def _get_json_entities(question: str):
    entities = []
    doc = nlp_model(question)

    for entity in doc.ents:
        root = entity.root
        json_entity = {
            "end": entity.end,
            "end_char": entity.end_char,
            "label": entity.label,
            "label_": entity.label_,
            "lemma_": entity.lemma_,
            "root": {
                "dep": root.dep,
                "dep_": root.dep_,
                "ent_type": root.ent_type,
                "idx": root.idx,
                "lemma": root.lemma,
                "lemma_": root.lemma_,
                "pos:": root.pos,
                "pos_": root.pos_,
                "tag": root.tag,
                "tag_": root.tag_,
                "text": root.text
            },
            "start": entity.start,
            "start_char": entity.start_char,
            "text": entity.text
        }
        entities.append(json_entity)

    return entities
