import json

import requests

from ro.webdata.oniq.common.nlp.sentence_utils import get_root
from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.spacy_model import nlp_model
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, ROOT_TYPES
from ro.webdata.oniq.sparql.model.final_triples.Triples import Triples
from ro.webdata.oniq.sparql.model.raw_triples.RawQuery import RawQuery
from ro.webdata.oniq.sparql.model.raw_triples.raw_query_utils import RawQueryUtils


class SPARQLBuilder:
    def __init__(self, endpoint, input_question, print_deps=True, print_result=False, include_targets=False):
        self.raw_query = _prepare_raw_query(input_question, print_deps)
        # self.triples = Triples(self.raw_query.raw_triples)

        if print_result is True:
            print(self.raw_query)


def _get_entities(question: str):
    entities_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{ACCESSORS.QUESTION}={question}'
    entities_response = requests.get(entities_uri)
    return json.loads(entities_response.content)


def _prepare_raw_query(input_question: str, print_deps: bool):
    document = nlp_model(input_question)
    raw_query = None

    # document = nlp_model("Who is the woman whose successor was Le Hong Phong?")  # FIXME
    # document = nlp_model("who is the one who baptized Ion's father?")  # FIXME
    # document = nlp_model("who is the son of Ion who died last year?")
    # document = nlp_model("Where did Ion's father reborn?")

    # document = nlp_model("What devices are used to treat heart failure?.")
    # document = nlp_model("Heart failure can be treated by what devices?")
    # document = nlp_model("Find me the devices to treat heart failure.")
    #
    # document = nlp_model("Which programming languages were influenced by Perl?")
    # document = nlp_model("When was Alberta admitted as province?")

    if print_deps:
        echo.deps_list(document)

    for sentence in document.sents:
        nl_question = NLQuestion(sentence)
        root = get_root(nl_question.value)
        root_type = nl_question.root_type
        raw_query = RawQuery(sentence)

        if root_type == ROOT_TYPES.AUX_ASK:
            RawQueryUtils.aux_ask_processing(nl_question, raw_query, root)
        if root_type == ROOT_TYPES.VERB_ASK:
            RawQueryUtils.verb_ask(nl_question, raw_query, root)
        elif root_type == ROOT_TYPES.PREP_ASK:
            RawQueryUtils.prep_ask_processing(nl_question, raw_query, root)
        elif root_type == ROOT_TYPES.PASSIVE:
            RawQueryUtils.passive_processing(nl_question, raw_query, root)
        elif root_type == ROOT_TYPES.POSSESSIVE:
            RawQueryUtils.possessive_processing(nl_question, raw_query, root)
        elif root_type == ROOT_TYPES.POSSESSIVE_COMPLEX:
            RawQueryUtils.possessive_complex_processing(nl_question, raw_query, root)
        elif root_type == ROOT_TYPES.AUX:
            RawQueryUtils.aux_processing(nl_question, raw_query, root)
        elif root_type == ROOT_TYPES.MAIN:
            RawQueryUtils.main_processing(nl_question, raw_query, root)
        else:
            # subject = root
            # predicate = get_related_verb(subject, sentence[subject.i + 1:])
            # obj = get_child_noun(predicate, sentence[predicate.i:])
            # triple = self.triples.append_triple(subject, predicate, obj)
            print()
            pass

    return raw_query
