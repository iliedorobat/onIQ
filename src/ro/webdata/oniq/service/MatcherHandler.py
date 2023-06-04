from urllib.parse import unquote, ParseResult

from spacy.tokens import Doc, Span

from ro.webdata.oniq.endpoint.common.match.PropertiesMatcher import PropertiesMatcher
from ro.webdata.oniq.endpoint.common.match.PropertyMatcher import PropertyMatcher
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements
from ro.webdata.oniq.service.query_const import ACCESSORS, PAIR_SEPARATOR, JOIN_OPERATOR, VALUES
from ro.webdata.oniq.spacy_model import nlp_model


class MatcherHandler:
    @staticmethod
    def prepare_successful_response(question: str, start_i: int, end_i: int, best_matched: PropertyMatcher):
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
    def prepare_failed_response(question: str, start_i: int, end_i: int):
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
    subject_uri: str = None
    object_uri: str = None

    def __init__(self, parsed_url: ParseResult):
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
            elif key == ACCESSORS.RESULT_TYPE:
                self.result_type = value
                continue
            elif key == ACCESSORS.TARGET_SUBJECT:
                self.subject_uri = value
                continue
            elif key == ACCESSORS.TARGET_OBJECT:
                self.object_uri = value
                continue

    def matcher_finder(self, props: RDFElements):
        failed_response = self.document is None or self.start_i == -1 or self.end_i == -1

        if failed_response:
            return MatcherHandler.prepare_failed_response(self.question, self.start_i, self.end_i)

        target_expression = self.document[self.start_i: self.end_i]
        best_matched = PropertiesMatcher.get_best_matched(
            props=props,
            target_expression=target_expression,
            result_type=self.result_type,
            subject_uri=self.subject_uri,
            object_uri=self.object_uri
        )

        return MatcherHandler.prepare_successful_response(self.question, self.start_i, self.end_i, best_matched)


class StringMatcherHandler:
    document: Doc = None
    question: str = None
    result_type: str = None  # one of the attributes of DBPEDIA_CLASS_TYPES
    target_expression: Span = None
    subject_uri: str = None
    object_uri: str = None

    def __init__(self, parsed_url: ParseResult):
        for query in parsed_url.query.split(JOIN_OPERATOR):
            [key, value] = query.split(PAIR_SEPARATOR)

            if key == ACCESSORS.QUESTION:
                self.question = unquote(value)
                self.document = nlp_model(self.question)
                continue
            elif key == ACCESSORS.RESULT_TYPE:
                self.result_type = value
                continue
            elif key == ACCESSORS.TARGET_EXPRESSION:
                nlp_value = nlp_model(value)
                self.target_expression = Span(nlp_value, 0, len(nlp_value))
                continue
            elif key == ACCESSORS.TARGET_SUBJECT:
                self.subject_uri = value
                continue
            elif key == ACCESSORS.TARGET_OBJECT:
                self.object_uri = value
                continue

    def matcher_finder(self, props: RDFElements):
        failed_response = self.document is None or self.target_expression is None

        if failed_response:
            return MatcherHandler.prepare_failed_response(self.question, -1, -1)

        best_matched = PropertiesMatcher.get_best_matched(
            props=props,
            target_expression=self.target_expression,
            result_type=self.result_type,
            subject_uri=self.subject_uri,
            object_uri=self.object_uri
        )

        return MatcherHandler.prepare_successful_response(self.question, -1, -1, best_matched)
