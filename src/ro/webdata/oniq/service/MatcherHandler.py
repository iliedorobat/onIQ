from urllib.parse import unquote, ParseResult

import spacy
from spacy.tokens import Doc, Span

from ro.webdata.oniq.common.nlp.nlp_utils import text_to_span
from ro.webdata.oniq.common.nlp.utils import WordnetUtils
from ro.webdata.oniq.endpoint.common.match.PropertiesMatcher import PropertiesMatcher
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.service.query_const import ACCESSORS, PAIR_SEPARATOR, JOIN_OPERATOR
from ro.webdata.oniq.spacy_model import nlp_model


nlp_dbpedia = spacy.load('en_core_web_md')
nlp_dbpedia.add_pipe('dbpedia_spotlight', config={'confidence': 0.75})


class _ResponseFormatter:
    @staticmethod
    def successful(question: str, start_i: int, end_i: int, best_matched: PropertyMatcher):
        return {
            ACCESSORS.QUESTION: question,
            ACCESSORS.START_I: start_i,
            ACCESSORS.END_I: end_i,
            ACCESSORS.PROPERTY: best_matched.property.serialize(),
            ACCESSORS.SCORE: best_matched.score,
            ACCESSORS.DETACHMENT_SCORE: best_matched.detachment_score,
            ACCESSORS.RESULT_TYPE: best_matched.result_type
        }

    @staticmethod
    def failed(question: str, start_i: int, end_i: int):
        return {
            ACCESSORS.QUESTION: question,
            ACCESSORS.START_I: start_i,
            ACCESSORS.END_I: end_i,
            ACCESSORS.PROPERTY: None,
            ACCESSORS.SCORE: -1
        }


class SpanMatcherHandler:
    document: Doc = None
    end_i: int = -1
    start_i: int = -1
    question: str = None
    result_type: str = None  # one of the attributes of DBPEDIA_CLASS_TYPES
    target_expression = None

    node_type: str = None
    node_start_i: int = -1
    node_end_i: int = -1
    node_value: Span = None
    str_node_value: str = None

    def __init__(self, parsed_url: ParseResult):
        for query in parsed_url.query.split(JOIN_OPERATOR):
            [key, value] = query.split(PAIR_SEPARATOR)

            if key == ACCESSORS.QUESTION:
                self.question = unquote(value)
                self.document = nlp_dbpedia(self.question)
                continue
            elif key == ACCESSORS.START_I:
                self.start_i = int(value)
                continue
            elif key == ACCESSORS.END_I:
                self.end_i = int(value)
                continue
            elif key == ACCESSORS.RESULT_TYPE:
                self.result_type = value
                continue
            elif key == ACCESSORS.NODE_TYPE:
                self.node_type = unquote(value)
                continue
            elif key == ACCESSORS.NODE_VALUE:
                self.str_node_value = unquote(value)
                continue
            elif key == ACCESSORS.NODE_START_I:
                self.node_start_i = int(value)
                continue
            elif key == ACCESSORS.NODE_END_I:
                self.node_end_i = int(value)
                continue

        if isinstance(self.document, Doc):
            failed_expression_construct = self.start_i == -1 or self.end_i == -1
            if not failed_expression_construct:
                self.target_expression = self.document[self.start_i: self.end_i]

            failed_node_construct = self.node_start_i == -1 or self.node_end_i == -1
            if not failed_node_construct:
                node_value = self.document[self.node_start_i: self.node_end_i]
                ents = self.document.ents

                if len(ents) > 0:
                    for ent in ents:
                        if ent.text == node_value.text:
                            self.node_value = ent
                else:
                    self.node_value = text_to_span(self.str_node_value, node_value.root.ent_type_)

    def matcher_finder(self, props: RDFElements):
        if self.target_expression is None:
            return _ResponseFormatter.failed(self.question, self.start_i, self.end_i)

        best_matched = PropertiesMatcher.get_best_matched(
            props=props,
            target_expression=self.target_expression,
            result_type=self.result_type,
            node_type=self.node_type,
            node_text_value=self.str_node_value
        )

        # if self.target_expression.text.lower() == "dissolve":
        #     # Use a proper synonym for the word "dissolve"
        #     # E.g.: "When did the Ming dynasty dissolve?"
        #
        #     nlp_value = nlp_dbpedia("end")
        #     new_target_expression = Span(nlp_value, 0, len(nlp_value))
        #
        #     new_best_matched = PropertiesMatcher.get_best_matched(
        #         props=props,
        #         target_expression=new_target_expression,
        #         result_type=self.result_type,
        #         node_type=self.node_type,
        #         node_text_value=self.str_node_value
        #     )
        #
        #     if new_best_matched.score > best_matched.score:
        #         return _ResponseFormatter.prepare_successful_response(self.question, self.start_i, self.end_i, new_best_matched)

        return _ResponseFormatter.successful(self.question, self.start_i, self.end_i, best_matched)


class StringMatcherHandler:
    document: Doc = None
    question: str = None
    result_type: str = None  # one of the attributes of DBPEDIA_CLASS_TYPES
    target_expression: Span = None

    node_type: str = None
    node_start_i: int = -1
    node_end_i: int = -1
    node_value: Span = None
    str_node_value: str = None

    def __init__(self, parsed_url: ParseResult):
        for query in parsed_url.query.split(JOIN_OPERATOR):
            [key, value] = query.split(PAIR_SEPARATOR)

            if key == ACCESSORS.QUESTION:
                self.question = unquote(value)
                self.document = nlp_dbpedia(self.question)
                continue
            elif key == ACCESSORS.RESULT_TYPE:
                self.result_type = value
                continue
            elif key == ACCESSORS.TARGET_EXPRESSION:
                nlp_value = nlp_dbpedia(value)
                self.target_expression = Span(nlp_value, 0, len(nlp_value))
                continue
            elif key == ACCESSORS.NODE_TYPE:
                self.node_type = unquote(value)
                continue
            elif key == ACCESSORS.NODE_VALUE:
                self.str_node_value = unquote(value)
                continue
            elif key == ACCESSORS.NODE_START_I:
                self.node_start_i = int(value)
                continue
            elif key == ACCESSORS.NODE_END_I:
                self.node_end_i = int(value)
                continue

        if isinstance(self.document, Doc):
            failed_node_construct = self.node_start_i == -1 or self.node_end_i == -1

            if not failed_node_construct:
                node_value = self.document[self.node_start_i: self.node_end_i]
                ent_type = node_value.root.ent_type_

                if self.target_expression.text.lower() == "country":
                    # E.g.: "Give me all Swedish holidays."
                    self.str_node_value = WordnetUtils.find_country_by_nationality(node_value.text)
                    ent_type = "GPE"

                self.node_value = text_to_span(self.str_node_value, ent_type)

    def matcher_finder(self, props: RDFElements):
        if self.target_expression is None:
            return _ResponseFormatter.failed(self.question, -1, -1)

        best_matched = PropertiesMatcher.get_best_matched(
            props=props,
            target_expression=self.target_expression,
            result_type=self.result_type,
            node_type=self.node_type,
            node_text_value=self.str_node_value
        )

        return _ResponseFormatter.successful(self.question, -1, -1, best_matched)
