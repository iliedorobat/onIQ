from urllib.parse import unquote, ParseResult

from spacy.tokens import Doc

from ro.webdata.oniq.endpoint.common.match.PropertiesMatcher import PropertiesMatcher
from ro.webdata.oniq.endpoint.common.translator.CSVTranslator import CSVTranslator
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.service.MatcherHandler import SpanMatcherHandler, StringMatcherHandler
from ro.webdata.oniq.service.query_const import ACCESSORS, JOIN_OPERATOR, PAIR_SEPARATOR, VALUES
from ro.webdata.oniq.spacy_model import nlp_model

all_props = CSVTranslator.to_props()


def entities_handler(parsed):
    output = {}

    for query in parsed.query.split(JOIN_OPERATOR):
        [key, value] = query.split(PAIR_SEPARATOR)
        question = unquote(value)

        if key == ACCESSORS.QUESTION:
            output[ACCESSORS.QUESTION] = question
            output[ACCESSORS.ENTITIES] = _get_json_entities(question)


def matcher_handler(parsed_url: ParseResult):
    target_subject = _get_target_resource(parsed_url, ACCESSORS.TARGET_SUBJECT)
    target_object = _get_target_resource(parsed_url, ACCESSORS.TARGET_OBJECT)
    target_type = _get_target_type(parsed_url)
    props = all_props

    if target_subject is not None:
        props = DBpediaQueryService.run_subject_properties_query(target_subject)
    if target_object is not None:
        props = DBpediaQueryService.run_object_properties_query(target_object)

    if target_type == VALUES.SPAN:
        matcher = SpanMatcherHandler(parsed_url)
        return matcher.matcher_finder(props)
    elif target_type == VALUES.STRING:
        matcher = StringMatcherHandler(parsed_url)
        return matcher.matcher_finder(props)


def _get_target_resource(parsed_url: ParseResult, accessor: str):
    for query in parsed_url.query.split(JOIN_OPERATOR):
        [key, value] = query.split(PAIR_SEPARATOR)

        if key == accessor:
            return value.replace("dbr:", "")

    return None


def _get_target_type(parsed_url: ParseResult):
    for query in parsed_url.query.split(JOIN_OPERATOR):
        [key, value] = query.split(PAIR_SEPARATOR)

        if key == ACCESSORS.TARGET_TYPE:
            return value

    return None


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
