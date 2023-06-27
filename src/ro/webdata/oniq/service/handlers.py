from urllib.parse import unquote, ParseResult

import pydash

from ro.webdata.oniq.common.nlp.utils import get_resource_name
from ro.webdata.oniq.endpoint.common.translator.CSVTranslator import CSVTranslator
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.endpoint.dbpedia.query import DBpediaQueryService
from ro.webdata.oniq.endpoint.models.RDFElement import URI, URI_TYPE
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.service.EntityHandler import SpanEntityHandler
from ro.webdata.oniq.service.MatcherHandler import SpanMatcherHandler, StringMatcherHandler
from ro.webdata.oniq.service.query_const import ACCESSORS, JOIN_OPERATOR, PAIR_SEPARATOR, DATA_TYPE, NODE_TYPE

print("Loading DBpedia classes...")
all_classes = CSVTranslator.to_classes()

print("Loading DBpedia properties...")
all_props = CSVTranslator.to_props()


def entities_handler(parsed):
    handler = _get_entity_handler(parsed, all_classes)

    if handler is not None:
        return handler.entity_finder()

    return None


def matcher_handler(parsed_url: ParseResult):
    handler = get_matcher_handler(parsed_url)
    props = all_props

    if handler is not None:
        node_type = _get_param_value(parsed_url, ACCESSORS.NODE_TYPE)
        node_text_value = _get_param_value(parsed_url, ACCESSORS.NODE_VALUE, True)

        named_entity = handler.node_value
        if named_entity.label_ == "DBPEDIA_ENT" and named_entity.kb_id_ != "":
            # E.g.: "What is the net income of Apple?"
            # E.g.: "When did the Ming dynasty dissolve?" => named_entity.kb_id_ == ""
            res_name = get_resource_name(named_entity)
        else:
            lookup_result = LookupService.entities_lookup(named_entity, all_classes)
            resource_name = pydash.get(lookup_result, [0, "resource", 0], node_text_value)
            res_name = resource_name.replace(NAMESPACE.DBP_RESOURCE, "")

        if node_type == NODE_TYPE.SUBJECT:
            props = DBpediaQueryService.run_subject_properties_query(res_name)

        if node_type == NODE_TYPE.OBJECT:
            props = DBpediaQueryService.run_object_properties_query(res_name)

        return handler.matcher_finder(props)

    return None


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


def _get_entity_handler(parsed_url, classes: RDFElements):
    target_data_type = _get_param_value(parsed_url, ACCESSORS.TARGET_DATA_TYPE)

    if target_data_type == DATA_TYPE.SPAN:
        return SpanEntityHandler(parsed_url, classes)

    return None


def get_matcher_handler(parsed_url):
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
