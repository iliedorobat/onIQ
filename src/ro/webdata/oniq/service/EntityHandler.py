from urllib.parse import unquote, ParseResult

import pydash
from spacy.tokens import Doc, Span

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.service.query_const import ACCESSORS, PAIR_SEPARATOR, JOIN_OPERATOR
from ro.webdata.oniq.spacy_model import nlp_model


class _ResponseFormatter:
    @staticmethod
    def successful(question: str, start_i: int, end_i: int, named_entity: Span, resource: str):
        res_name = resource.replace(NAMESPACE.DBP_RESOURCE, "")

        return {
            ACCESSORS.QUESTION: question,
            ACCESSORS.START_I: start_i,
            ACCESSORS.END_I: end_i,
            ACCESSORS.NAMED_ENTITY: named_entity.text,
            ACCESSORS.RESOURCE_NAME: res_name,
            ACCESSORS.RESOURCE_NAMESPACE: NAMESPACE.DBP_RESOURCE
        }

    @staticmethod
    def failed(question: str, start_i: int, end_i: int):
        return {
            ACCESSORS.QUESTION: question,
            ACCESSORS.START_I: start_i,
            ACCESSORS.END_I: end_i,
            ACCESSORS.NAMED_ENTITY: None
        }


class SpanEntityHandler:
    all_classes: RDFElements = RDFElements([])
    document: Doc = None
    end_i: int = -1
    start_i: int = -1
    question: str = None
    named_entity = None

    def __init__(self, parsed_url: ParseResult, all_classes: RDFElements):
        self.all_classes = all_classes

        for query in parsed_url.query.split(JOIN_OPERATOR):
            [key, value] = query.split(PAIR_SEPARATOR)

            if key == ACCESSORS.QUESTION:
                self.question = unquote(value)
                self.document = nlp_model(self.question)
                continue
            elif key == ACCESSORS.START_I:
                self.start_i = int(value)
                continue
            elif key == ACCESSORS.END_I:
                self.end_i = int(value)
                continue

        if isinstance(self.document, Doc):
            failed_entity_construct = self.start_i == -1 or self.end_i == -1
            if not failed_entity_construct:
                value = self.document[self.start_i: self.end_i]
                self.named_entity = text_to_span(value.text, value.root.ent_type_)

    def entity_finder(self):
        if self.named_entity is None:
            return _ResponseFormatter.failed(self.question, self.start_i, self.end_i)

        lookup_result = LookupService.entities_lookup(self.named_entity, self.all_classes)
        resource = pydash.get(lookup_result, [0, "resource", 0])

        return _ResponseFormatter.successful(self.question, self.start_i, self.end_i, self.named_entity, resource)
