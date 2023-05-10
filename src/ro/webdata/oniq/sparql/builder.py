import json

import requests
from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.sentence_utils import get_root, contains_multiple_wh_words, ends_with_verb
from ro.webdata.oniq.common.nlp.word_utils import is_followed_by_prep, is_preceded_by_adj_modifier, get_prev_word, \
    is_noun
from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.service.query_const import ACCESSORS, PATHS
from ro.webdata.oniq.spacy_model import nlp_model
from ro.webdata.oniq.sparql.model.NLQuestion import NLQuestion, ROOT_TYPES
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.triple_utils import get_related_verb, TripleUtils, get_child_noun
from ro.webdata.oniq.sparql.model.Triples import Triples


class SPARQLBuilder:
    def __init__(self, endpoint, input_question, print_deps=True, print_result=False):
        self.triples = Triples([])

        document = nlp_model(input_question)

        if print_deps:
            echo.deps_list(document)

        for sentence in document.sents:
            nl_question = NLQuestion(sentence)
            root = get_root(nl_question.value)
            root_type = nl_question.root_type

            if root_type == ROOT_TYPES.AUX_ASK:
                _aux_ask_processing(self.triples, root)
            if root_type == ROOT_TYPES.VERB_ASK:
                _verb_ask(self.triples, root)
            elif root_type == ROOT_TYPES.PREP_ASK:
                _prep_ask_processing(self.triples, root)
            elif root_type == ROOT_TYPES.PASSIVE:
                _passive_processing(self.triples, root, nl_question)
            elif root_type == ROOT_TYPES.POSSESSIVE:
                _possessive_processing(self.triples, root, nl_question)
            elif root_type == ROOT_TYPES.POSSESSIVE_COMPLEX:
                _possessive_complex_processing(self.triples, root, nl_question)
            elif root_type == ROOT_TYPES.AUX:
                _aux_processing(self.triples, root, nl_question)
            elif root_type == ROOT_TYPES.MAIN:
                _main_processing(self.triples, root, nl_question)
            else:
                pass

        if print_result is True:
            print(self.triples)


def _get_entities(question: str):
    entities_uri = f'http://localhost:8200/{PATHS.ENTITIES}?{ACCESSORS.QUESTION}={question}'
    entities_response = requests.get(entities_uri)
    return json.loads(entities_response.content)


def _aux_processing(triples: Triples, root: Token, nl_question: NLQuestion):
    # E.g.: "Who is the leader of the town where the Myntdu river originates?"

    sentence = root.sent  # TODO: remove
    triple = TripleUtils.append_root_aux_triple(triples, sentence, root, nl_question.target)
    # <(town)   (leader)   (leader)>

    if triple is None:
        # E.g.: "Who is the tallest basketball player?"
        subject = nl_question.target
        obj = NounEntity(
            get_child_noun(root, sentence)
        )
        triple = TripleUtils.append_rdf_type_triple(triples, subject, obj)

    if triple is None:
        # E.g.: "Who is the youngest Pulitzer Prize winner?"
        subject = nl_question.target
        predicate = subject
        obj = NounEntity(
            get_child_noun(root, sentence)
        )
        if obj.noun.dep_ == "attr":
            predicate = obj.noun
        triple = triples.append_triple(subject, predicate, obj)

    if triple is not None:
        TripleUtils.append_rdf_type_triple(triples, triple.s, triple.s)

        related_verb = get_related_verb(triple.s.noun, sentence)
        if related_verb is not None:
            subject = get_child_noun(related_verb, sentence)
            triple = triples.append_triple(subject, related_verb, triple.s)
            # <("Myntdu river")   (originates)   (town)>
        else:
            # E.g.: "What is the population and area of the most populated state?"
            # Do nothing
            pass

        # add the right side
        # E.g.: Which museum in New York has the most visitors?
        def exists(word):
            for _triple in triples:
                if _triple.o.token == word:
                    # E.g.: "Who is the tallest basketball player?"
                    return True
            return False

        rights = [noun for noun in list(root.rights) if is_noun(noun) and not exists(noun)]

        if len(rights) > 0:
            for noun in rights:
                if triple.s.token != noun:
                    # triple.s.token == noun => E.g.: "What is the tallest building in Romania?"
                    triple = triples.append_triple(triple.s, noun, noun)

    pass


def _aux_ask_processing(triples: Triples, root: Token):
    # E.g.: "Did Arnold Schwarzenegger attend a university?"

    sentence = root.sent  # TODO: remove
    triple = TripleUtils.append_root_aux_ask_triple(triples, sentence, root)
    # <subject of the root (Schwarzenegger)   predicate (attend)   object (university)>

    TripleUtils.append_rdf_type_triple(triples, triple.o, triple.o)
    # <(university)   (rdf:type)   (dbo:University)>

    pass


def _main_processing(triples: Triples, root: Token, nl_question: NLQuestion):
    # FIXME: "Who won the Pulitzer Prize?"

    # ends with a verb
    # E.g.: [1] "Where is the New York Times published?"
    # E.g.: [2] "Where did Mashhur bin Abdulaziz Al Saud's father die?"

    triple = TripleUtils.append_root_target_triple(triples, root, nl_question.target)
    # [1] <subject of the predicate ("New York Times")   predicate (published)>   target (location)> (NER)
    # [2] <subject of the predicate (father)             predicate (die)          target (location)>

    if not triple.o.is_text:
        # E.g.: "Which musician wrote the most books?"
        TripleUtils.append_rdf_type_triple(triples, triple.o, triple.o)

    subject = get_child_noun(triple.s.compound_noun[0], root.sent)
    if subject is not None:
        # possessive ending (E.g.: [2] => 's)
        pos = [token for token in list(subject.rights) if token.tag_ == "POS"]
        if len(pos) > 0:
            triple = triples.append_triple(subject, triple.s.noun, triple.s)
            # [2] <subject ("Mashhur bin Abdulaziz Al Saud")   subject.head (father)   subject.head (father)> (NER)

    pass


def _passive_processing(triples: Triples, root: Token, nl_question: NLQuestion):
    # ends with a verb which has a passive verb attached
    # E.g.: [1] "Where is Fort Knox located?"
    # E.g.: [2] "Where was the person who won the oscar born?" [passive attachment]
    # E.g.: [3] "Where was the person born whose successor was Le Hong Phong?" [passive attachment]
    # E.g.: [4] "Where was the designer of REP Parasol born?"

    sentence = root.sent  # TODO: remove
    triple = TripleUtils.append_root_target_triple(triples, root, nl_question.target)
    # [1] <subject of root ("Fort Knox")   predicate (located)   target (location)> (NER)
    # [2] <subject of root (person)        predicate (born)      target (location)>
    # [3] <subject of root (person)        predicate (born)      target (location)>
    # [4] <subject of root (designer)      predicate (born)      target (location)>
    TripleUtils.append_rdf_type_triple(triples, triple.s, triple.s)

    if contains_multiple_wh_words(sentence):
        triple = TripleUtils.append_passive_triple(triples, sentence, triple.s, triple.p)
        # [2] <subject of root (person)    predicate (won)        object (oscar)>
        # [3] <subject of root (person)    predicate (successor)  object ("Le Hong Phong")>

    # TODO: make a generic method for adding the pobjs preceded by a preposition
    prep = [token for token in list(triple.s.noun.rights) if token.dep_ == "prep"]
    if len(prep) > 0:
        subject = get_child_noun(triple.p, sentence)
        obj = get_child_noun(subject, sentence)
        triple = triples.append_triple(subject, subject, obj)
        # [4] <subject of root (designer)   subject of root (designer)  pobj ("REP Parasol")

    pass


def _possessive_processing(triples: Triples, root: Token, nl_question: NLQuestion):
    # E.g.: "Whose successor is Le Hong Phong?"  ## made by me

    sentence = root.sent  # TODO: remove
    predicate = get_child_noun(root, sentence)
    obj = get_child_noun(root, sentence[root.i + 1:])
    triple = triples.append_triple(nl_question.target, predicate, obj)
    TripleUtils.append_rdf_type_triple(triples, triple.s, triple.s)

    pass


def _possessive_complex_processing(triples: Triples, root: Token, nl_question: NLQuestion):
    sentence = root.sent  # TODO: remove

    if ends_with_verb(sentence):
        # E.g.: "Where was the person whose successor studied law born?"

        subject = get_child_noun(root, root.sent)
        # triple = append_root_target_triple(self.triples, root, nl_question.target)
        triple = triples.append_triple(subject, nl_question.target, nl_question.target)

        predicate = get_related_verb(triple.s.noun, sentence[subject.i + 1:])
        subject = get_child_noun(predicate, sentence)
        obj = get_child_noun(predicate, sentence[predicate.i + 1:])

        triple = triples.append_triple(triple.s, subject, subject)
        triple = triples.append_triple(subject, predicate, obj)

        pass
    else:
        # E.g.: "Who is the woman whose successor was Le Hong Phong?"

        subject = get_child_noun(root, sentence)
        predicate = get_child_noun(subject, sentence)
        obj = get_child_noun(predicate.head, sentence[predicate.i + 1:])
        triple = triples.append_triple(subject, predicate, obj)

    pass


def _verb_ask(triples: Triples, root: Token):
    sentence = root.sent  # TODO: remove
    child_noun = get_child_noun(root, sentence)

    if is_followed_by_prep(child_noun):
        # E.g.: "Give me the currency of China."
        subject = NounEntity(
            get_child_noun(child_noun, sentence)
        )
        predicate = child_noun
        obj = NounEntity(predicate.lemma_)

        triples.append_triple(subject, predicate, obj)

    elif is_preceded_by_adj_modifier(child_noun):
        # E.g.: "Give me all Swedish holidays."

        adj_modifier = get_prev_word(child_noun)
        rdf_type = NounEntity(child_noun.lemma_)
        triple = TripleUtils.append_rdf_type_triple(triples, rdf_type, rdf_type)

        obj = NounEntity(adj_modifier)
        triple = triples.append_triple(triple.s, "country", obj)

    else:
        # E.g.: "Give me all ESA astronauts."

        prev_word = get_prev_word(child_noun)

        if prev_word.dep_ == "compound":
            rdf_type = NounEntity(child_noun.lemma_)
            triple = TripleUtils.append_rdf_type_triple(triples, rdf_type, rdf_type)

            obj = NounEntity(prev_word)
            triple = triples.append_triple(triple.s, "prop", obj)

    pass


def _prep_ask_processing(triples: Triples, root: Token):
    # E.g.: [1] "In which country is Mecca located?"
    # E.g.: [2] "At what distance does the earth curve?"  # TODO:

    triple = TripleUtils.append_root_target_prep_triple(triples, root)
    # <subject of the root (Mecca)   object (country)   object (country)>

    pass
