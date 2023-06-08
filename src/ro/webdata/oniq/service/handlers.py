from urllib.parse import unquote, ParseResult

import pydash

from ro.webdata.oniq.endpoint.common.translator.CSVTranslator import CSVTranslator
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.models.RDFElement import URI, URI_TYPE
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.service.MatcherHandler import SpanMatcherHandler, StringMatcherHandler
from ro.webdata.oniq.service.query_const import ACCESSORS, JOIN_OPERATOR, PAIR_SEPARATOR, DATA_TYPE, NODE_TYPE
from ro.webdata.oniq.spacy_model import nlp_model

print("Loading DBpedia classes...")
all_classes = CSVTranslator.to_classes()

print("Loading DBpedia properties...")
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
    matcher = _get_matcher(parsed_url)
    props = all_props

    if matcher is not None:
        node_type = _get_param_value(parsed_url, ACCESSORS.NODE_TYPE)
        node_text_value = _get_param_value(parsed_url, ACCESSORS.NODE_VALUE, True)

        named_entity = matcher.node_value
        lookup_result = LookupService.entities_lookup(named_entity, all_classes)
        resource_name = pydash.get(lookup_result, [0, "resource", 0], node_text_value)
        res_name = resource_name.replace(NAMESPACE.DBP_RESOURCE, "")

        if node_type == NODE_TYPE.SUBJECT:
            props = DBpediaQueryService.run_subject_properties_query(res_name)

        if node_type == NODE_TYPE.OBJECT:
            props = DBpediaQueryService.run_object_properties_query(res_name)

        return matcher.matcher_finder(props)


def resource_type_handler(parsed_url: ParseResult):
    # E.g.: resource_name == "dbo:Mountain"
    resource_name = _get_param_value(parsed_url, ACCESSORS.RESOURCE_NAME)

    rdf_classes = [rdf_class for rdf_class in all_classes if str(rdf_class) == resource_name]
    obj_parent_uris: str = pydash.get(rdf_classes, ["0", "parent_uris"])

    if obj_parent_uris is None:
        return None

    if URI.PLACE_CLASS in obj_parent_uris:
        if URI.NATURAL_PLACE_CLASS in obj_parent_uris:
            return URI_TYPE.NATURAL_PLACE

        return URI_TYPE.PLACE

    return None


def _get_matcher(parsed_url):
    target_data_type = _get_param_value(parsed_url, ACCESSORS.TARGET_DATA_TYPE)

    if target_data_type == DATA_TYPE.SPAN:
        return SpanMatcherHandler(parsed_url)
    elif target_data_type == DATA_TYPE.STRING:
        return StringMatcherHandler(parsed_url)

    return None


def _get_param_value(parsed_url: ParseResult, accessor: str, is_dbr: bool = False):
    for query in parsed_url.query.split(JOIN_OPERATOR):
        [key, value] = query.split(PAIR_SEPARATOR)

        if key == accessor:
            output = value

            if is_dbr:
                output = value.replace("dbr:", "")

            return unquote(output)

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
