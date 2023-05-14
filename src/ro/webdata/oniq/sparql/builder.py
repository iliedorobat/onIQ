import json
from typing import List

import requests

from ro.webdata.oniq.common.nlp.sentence_utils import get_root
from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, ROOT_TYPES
from ro.webdata.oniq.sparql.model.final_triples.Triples import Triples
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple
from ro.webdata.oniq.sparql.model.raw_triples.raw_triple_utils import RawTripleUtils
from ro.webdata.oniq.sparql.model.raw_triples.raw_target_utils import RawTargetUtils


class SPARQLBuilder:
    def __init__(self, endpoint, input_question, print_deps=True, print_result=False):
        # self.triples = Triples(self.raw_query.raw_triples)

        nl_question = NLQuestion(input_question)
        self.raw_triples = _prepare_raw_triples(nl_question)
        self.target_nouns = _prepare_target_nouns(nl_question, self.raw_triples)

        if print_deps:
            echo.deps_list(nl_question.question)

        if print_result:
            # print(self.to_raw_query_str())
            print(self.to_sparql_query())

    def to_sparql_query(self):
        output = "SELECT"

        for target in self.target_nouns:
            output += f" {target.to_var()}"

        output += "\nWHERE {"
        # TODO: replace raw_triples with self.triples
        for triple in self.raw_triples:
            output += f"\n\t{str(triple)} ."
        output += "\n}"

        return output

    def to_raw_query_str(self):
        output = "target_nouns = [\n"
        for target in self.target_nouns:
            output += f"\t{target.to_var()}\n"
        output += "]\n"

        output += "raw_triples = [\n"
        for raw_triple in self.raw_triples:
            output += f"\t<{str(raw_triple)}>\n"
        output += "]"

        return output


def _get_entities(question: str):
    entities_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{ACCESSORS.QUESTION}={question}'
    entities_response = requests.get(entities_uri)
    return json.loads(entities_response.content)


def _prepare_raw_triples(nl_question: NLQuestion):
    root = get_root(nl_question.question)
    root_type = nl_question.root_type
    raw_triples = []

    if root_type == ROOT_TYPES.AUX_ASK:
        RawTripleUtils.aux_ask_processing(nl_question, raw_triples, root)
    if root_type == ROOT_TYPES.VERB_ASK:
        RawTripleUtils.verb_ask(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.PREP_ASK:
        RawTripleUtils.prep_ask_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.PASSIVE:
        RawTripleUtils.passive_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.POSSESSIVE:
        RawTripleUtils.possessive_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.POSSESSIVE_COMPLEX:
        RawTripleUtils.possessive_complex_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.AUX:
        RawTripleUtils.aux_processing(nl_question, raw_triples, root)
    elif root_type == ROOT_TYPES.MAIN:
        RawTripleUtils.main_processing(nl_question, raw_triples, root)
    else:
        # subject = root
        # predicate = get_related_verb(subject, sentence[subject.i + 1:])
        # obj = get_child_noun(predicate, sentence[predicate.i:])
        # triple = self.triples.append_triple(subject, predicate, obj)
        pass

    return raw_triples


def _prepare_target_nouns(nl_question: NLQuestion, raw_triples: List[RawTriple]):
    target_nouns = []

    for raw_triple in raw_triples:
        RawTargetUtils.update_target_nouns(nl_question, target_nouns, raw_triple)

    return target_nouns
