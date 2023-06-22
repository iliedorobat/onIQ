from typing import List, Union

from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span
from ro.webdata.oniq.common.nlp.sentence_utils import ends_with_verb, contains_multiple_wh_words
from ro.webdata.oniq.common.nlp.word_utils import is_noun, is_followed_by_prep, is_preceded_by_adj_modifier, \
    get_prev_word, is_verb, is_aux, is_adj, is_adv
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.sparql.model.NLQuestion import QUESTION_TARGET, NLQuestion, ROOT_TYPES, QUESTION_TYPES
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class HRawTripleUtils:
    @staticmethod
    def aux_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        subject = NounEntity(
            get_child_noun(root, nl_question.question)
        )
        prev_word = get_prev_word(root)

        if is_adj(prev_word) or is_adv(prev_word):
            # E.g.: is_adj(prev_word) => "How high is the Yokohama Marine Tower?"
            # E.g.: is_adv(prev_word) => "How long is the ...?"

            raw_triple = RawTriple(
                s=subject,
                p=token_to_span(prev_word),
                o=prev_word.text,
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)

            return raw_triple

        return None


class WRawTripleUtils:
    @staticmethod
    def aux_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        # E.g.: "Who is the leader of the town where the Myntdu river originates?"
        triple = _append_root_aux_triple(nl_question, raw_triples, root)
        # <(town)   (leader)   (leader)>

        if triple is None:
            # E.g.: "Who is the youngest Pulitzer Prize winner?"
            subject = nl_question.target
            predicate = nl_question.target
            obj = NounEntity(
                get_child_noun(root, nl_question.question)
            )
            if obj.noun.dep_ == "attr":
                predicate = obj.to_span()

            raw_triple = RawTriple(
                s=subject,
                p=predicate,
                o=obj,
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)

        if triple is not None:
            if not triple.is_rdf_type():
                # E.g.: triple.is_rdf_type => "Who is the tallest basketball player?"
                _append_rdf_type_triple(nl_question, raw_triples, triple.s, triple.s)

            related_verb = get_related_verb(triple.s.noun, nl_question.question)

            if related_verb is not None:
                raw_triple = RawTriple(
                    s=get_child_noun(related_verb, nl_question.question),
                    p=token_to_span(related_verb),
                    o=triple.s,
                    question=nl_question.question
                )
                _append_raw_triple(raw_triples, raw_triple)
                # <("Myntdu river")   (originates)   (town)>
            else:
                # E.g.: "What is the population and area of the most populated state?"
                # Do nothing
                pass

            # add the right side
            # E.g.: Which museum in New York has the most visitors?
            def exists(word):
                for _triple in raw_triples:
                    if _triple.o.token == word:
                        # E.g.: "Who is the tallest basketball player?"
                        return True
                return False

            rights = [noun for noun in list(root.rights) if is_noun(noun) and not exists(noun)]

            if len(rights) > 0:
                for noun in rights:
                    if triple.s.token != noun:
                        # triple.s.token == noun => E.g.: "What is the tallest building in Romania?"
                        raw_triple = RawTriple(
                            s=triple.s,
                            p=token_to_span(noun),
                            o=noun,
                            question=nl_question.question
                        )
                        _append_raw_triple(raw_triples, raw_triple)

        pass

    @staticmethod
    def aux_ask_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        # E.g.: "Did Arnold Schwarzenegger attend a university?"
        triple = _append_root_aux_ask_triple(nl_question, raw_triples, root)
        # <subject of the root (Schwarzenegger)   predicate (attend)   object (university)>

        _append_rdf_type_triple(nl_question, raw_triples, triple.o, triple.o)
        # <(university)   (rdf:type)   (dbo:University)>

        pass

    @staticmethod
    def main_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        # FIXME: "Who won the Pulitzer Prize?"

        # ends with a verb
        # E.g.: [1] "Where is the New York Times published?"
        # E.g.: [2] "Where did Mashhur bin Abdulaziz Al Saud's father die?"

        triple = _append_root_target_triple(nl_question, raw_triples, root)
        # [1] <subject of the predicate ("New York Times")   predicate (published)>   target (location)> (NER)
        # [2] <subject of the predicate (father)             predicate (die)          target (location)>

        _append_rdf_type_triple(nl_question, raw_triples, triple.o, triple.o)

        subject = get_child_noun(triple.s.compound_noun[0], root.sent)

        if subject is not None:
            # possessive ending (E.g.: [2] => 's)
            pos = [token for token in list(subject.rights) if token.tag_ == "POS"]

            if len(pos) > 0:
                raw_triple = RawTriple(
                    s=subject,
                    p=triple.s.to_span(),
                    o=triple.s,
                    question=nl_question.question
                )
                _append_raw_triple(raw_triples, raw_triple)
                # [2] <subject ("Mashhur bin Abdulaziz Al Saud")   subject.head (father)   subject.head (father)> (NER)

        pass

    @staticmethod
    def passive_near_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        # E.g.: [1] "Which soccer players were born on Malta?"
        # E.g.: [2] "Who was married to an actor that played in Philadelphia?"

        if nl_question.main_type == QUESTION_TYPES.WHO:
            # E.g.: [1]
            obj = NounEntity(
                get_child_noun(root, nl_question.question)
            )

            raw_triple = RawTriple(
                s=QUESTION_TARGET.PERSON,
                p=token_to_span(root),
                o=obj,
                question=nl_question.question
            )
            triple = _append_raw_triple(raw_triples, raw_triple)

            if not triple.o.is_res():
                _append_rdf_type_triple(nl_question, raw_triples, triple.o, triple.o)

            subject = triple.o
            predicate = get_related_verb(subject.token, nl_question.question[subject.token.i + 1:])
            obj = NounEntity(
                get_child_noun(subject.token, nl_question.question)
            )

            raw_triple = RawTriple(
                s=subject,
                p=token_to_span(predicate),
                o=obj,
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)
        else:
            # E.g.: [2]
            triple = _append_root_target_triple(nl_question, raw_triples, root)
            _append_rdf_type_triple(nl_question, raw_triples, triple.s, triple.s)

        pass

    @staticmethod
    def passive_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        # ends with a verb which has a passive verb attached
        # E.g.: [1] "Where is Fort Knox located?"
        # E.g.: [2] "Where was the person who won the oscar born?" [passive attachment]
        # E.g.: [3] "Where was the person born whose successor was Le Hong Phong?" [passive attachment]
        # E.g.: [4] "Where was the designer of REP Parasol born?"

        triple = _append_root_target_triple(nl_question, raw_triples, root)
        # [1] <subject of root ("Fort Knox")   predicate (located)   target (location)> (NER)
        # [2] <subject of root (person)        predicate (born)      target (location)>
        # [3] <subject of root (person)        predicate (born)      target (location)>
        # [4] <subject of root (designer)      predicate (born)      target (location)>
        _append_rdf_type_triple(nl_question, raw_triples, triple.s, triple.s)

        if contains_multiple_wh_words(nl_question.question):
            triple = _append_passive_triple(nl_question, raw_triples, triple.s, triple.p.root)
            # [2] <subject of root (person)    predicate (won)        object (oscar)>
            # [3] <subject of root (person)    predicate (successor)  object ("Le Hong Phong")>

        # TODO: make a generic method for adding the pobjs preceded by a preposition
        prep = [token for token in list(triple.s.noun.rights) if token.dep_ == "prep"]
        if len(prep) > 0:
            subject = get_child_noun(triple.p.root, nl_question.question)
            raw_triple = RawTriple(
                s=subject,
                p=token_to_span(subject),
                o=get_child_noun(subject, nl_question.question),
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)
            # [4] <subject of root (designer)   subject of root (designer)  pobj ("REP Parasol")

        pass

    @staticmethod
    def possessive_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        # E.g.: ### "Whose successor is Le Hong Phong?"

        predicate = get_child_noun(root, nl_question.question)
        raw_triple = RawTriple(
            s=nl_question.target,
            p=token_to_span(predicate),
            o=get_child_noun(root, nl_question.question[root.i + 1:]),
            question=nl_question.question
        )
        _append_raw_triple(raw_triples, raw_triple)

        _append_rdf_type_triple(nl_question, raw_triples, raw_triple.s, raw_triple.s)

        pass

    @staticmethod
    def possessive_complex_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        if ends_with_verb(nl_question.question):
            # E.g.: "Where was the person whose successor studied law born?"
            subject = get_child_noun(root, root.sent)
            # triple = append_root_target_triple(self.triples, root, nl_question.target)
            raw_triple = RawTriple(
                s=subject,
                p=nl_question.target,
                o=nl_question.target,
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)

            related_verb = get_related_verb(raw_triple.s.noun, nl_question.question[subject.i + 1:])
            child_noun = get_child_noun(related_verb, nl_question.question)

            raw_triple = RawTriple(
                s=raw_triple.s,
                p=token_to_span(child_noun),
                o=child_noun,
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)

            raw_triple = RawTriple(
                s=child_noun,
                p=token_to_span(related_verb),
                o=get_child_noun(related_verb, nl_question.question[related_verb.i + 1:]),
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)

            pass
        else:
            # E.g.: "Who is the woman whose successor was Le Hong Phong?"
            subject = get_child_noun(root, nl_question.question)
            predicate = get_child_noun(subject, nl_question.question)
            raw_triple = RawTriple(
                s=subject,
                p=token_to_span(predicate),
                o=get_child_noun(predicate.head, nl_question.question[predicate.i + 1:]),
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)

        pass

    @staticmethod
    def noun_ask(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        subject = NounEntity(root)
        predicate = get_related_verb(subject.token, nl_question.question[subject.token.i + 1:])
        obj = NounEntity(
            get_child_noun(predicate, nl_question.question[predicate.i:])
        )

        raw_triple = RawTriple(
            s=subject,
            p=token_to_span(predicate),
            o=obj,
            question=nl_question.question
        )

        _append_raw_triple(raw_triples, raw_triple)
        _append_rdf_type_triple(nl_question, raw_triples, raw_triple.s, raw_triple.s)

        if is_followed_by_prep(root):
            # E.g.: "Desserts from which country contain fish?"

            obj = NounEntity(
                get_child_noun(root, nl_question.question, nl_question.root_type)
            )

            raw_triple = RawTriple(
                s=subject,
                p=obj.to_span(),
                o=obj,
                question=nl_question.question
            )

            _append_raw_triple(raw_triples, raw_triple)

    @staticmethod
    def verb_ask(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        child_noun = get_child_noun(root, nl_question.question)

        if is_followed_by_prep(child_noun):
            # E.g.: "Give me the currency of China."
            subject = NounEntity(
                get_child_noun(child_noun, nl_question.question)
            )

            # TODO: pass s=get_child_noun(child_noun, sentence) ???
            raw_triple = RawTriple(
                s=subject,
                p=token_to_span(child_noun),
                o=NounEntity(child_noun.lemma_, child_noun),
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)

        elif is_preceded_by_adj_modifier(child_noun):
            # E.g.: "Give me all Swedish holidays."
            adj_modifier = get_prev_word(child_noun)
            rdf_type = NounEntity(child_noun.lemma_, child_noun)
            triple = _append_rdf_type_triple(nl_question, raw_triples, rdf_type, rdf_type)

            # TODO: pass o=adj_modifier ???
            raw_triple = RawTriple(
                s=triple.s,
                p="country",
                o=NounEntity(adj_modifier),
                question=nl_question.question
            )
            _append_raw_triple(raw_triples, raw_triple)

        else:
            # E.g.: "Give me all ESA astronauts."
            prev_word = get_prev_word(child_noun)

            if prev_word.dep_ == "compound":
                rdf_type = NounEntity(child_noun.lemma_, child_noun)

                # TODO: workaround to handle targets
                # E.g.: "Give me all ESA astronauts."
                triple_subject = NounEntity(rdf_type.token.text)
                triple_subject.token = rdf_type.token

                triple = _append_rdf_type_triple(nl_question, raw_triples, triple_subject, rdf_type)

                # TODO: pass o=prev_word ???
                raw_triple = RawTriple(
                    s=triple.s,
                    p="?prop",
                    o=NounEntity(prev_word),
                    question=nl_question.question
                )
                _append_raw_triple(raw_triples, raw_triple)

        pass

    @staticmethod
    def prep_ask_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        # E.g.: [1] "In which country is Mecca located?"
        # E.g.: [2] "At what distance does the earth curve?"  # TODO:

        triple = _append_root_target_prep_triple(nl_question, raw_triples, root)
        # <subject of the root (Mecca)   object (country)   object (country)>

        pass


def get_related_verb(word: Token, sentence: Span):
    """
    Get the word whose head is the input word.

    :param word: The target head.
    :param sentence: The target sentence.
    :return: Token.
    """

    for token in sentence:
        if is_verb(token) and token.head == word:
            return token

    return None


# TODO: make root_type mandatory
def get_child_noun(word: Token, span: Span, root_type: str = None):
    for token in span:
        if token.i > word.i and token.pos_ == "ADP":
            # E.g.: "Who is the leader of the town where the Myntdu river originates?"
            return get_child_noun(token, token.sent[token.i + 1:], root_type)

        if token != word:
            token_equality = token.head == word
            if root_type == ROOT_TYPES.NOUN_ASK and is_verb(token.head):
                # E.g.: "Desserts from which country contain fish?"
                token_equality = token.head == word.head

            # E.g.: "Where was the designer of REP Parasol born?"
            is_auxpass = token.head.dep_ == "auxpass"

            # "Who is the person whose successor was Le Hong Phong?"
            prev_word = get_prev_word(token)
            is_poss = prev_word.dep_ == "poss" if isinstance(prev_word, Token) else False

            if token_equality or is_auxpass or is_poss:
                if token.dep_ == "auxpass":
                    if contains_multiple_wh_words(word.sent):
                        if ends_with_verb(span):
                            # E.g.: ### "Where was the person who won the oscar born?"
                            return get_child_noun(token, token.sent[token.i + 1:], root_type)
                        else:
                            # E.g.: "Where was the person born whose successor was Le Hong Phong?"
                            pass
                    else:
                        # E.g.: "Where is Fort Knox located?"
                        pass  # nothing to do

                if is_noun(token) and token.dep_ != "conj":
                    # E.g.: token.dep_ != "conj" => "What is the population and area of the most populated state?"
                    return token

                if token.pos_ == "NUM":
                    # E.g.: "who is the one who baptized Ion's father?"
                    return token

    return None


def _append_raw_triple(raw_triples: List[RawTriple], raw_triple: RawTriple):
    if not raw_triple.is_valid():
        # E.g.: "Where is Fort Knox located?"
        return None

    raw_triples.append(raw_triple)

    return raw_triple


def _append_rdf_type_triple(nl_question: NLQuestion, raw_triples: List[RawTriple], subject: Union[str, NounEntity], entity: NounEntity):
    if isinstance(subject, str) or subject.is_var():
        # E.g.: isinstance(subject, str) => "Who is the tallest basketball player?"
        # E.g.: not subject.is_var() => "Who is the manager of Real Madrid?"
        # E.g.: not subject.is_var() => "Who is the youngest Pulitzer Prize winner?"

        resource = LookupService.local_resource_lookup(entity.text)
        if resource is None:
            # E.g.: "What is the net income of Apple?"
            return None

        raw_triple = RawTriple(
            s=subject,
            p="rdf:type",
            o=NounEntity(resource, entity.token),
            question=nl_question.question
        )
        _append_raw_triple(raw_triples, raw_triple)

        return raw_triple

    return None


def _append_root_aux_ask_triple(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
    subject = get_child_noun(root, nl_question.question)
    obj = get_child_noun(subject, nl_question.question[subject.i + 1:])
    prop = token_to_span(root)

    if obj is None:
        # E.g.: "Did Arnold Schwarzenegger attend a university?"
        noun_list = [token for token in list(root.rights) if token.pos_ == "NOUN"]
        obj = noun_list[0] if len(noun_list) > 0 else None

    if is_aux(root):
        # E.g.: "Is Barack Obama a democrat?"
        prop = "?prop"

    # TODO: remove ???
    if obj is None:
        return None

    raw_triple = RawTriple(
        s=subject,
        p=prop,
        o=obj,
        question=nl_question.question
    )
    _append_raw_triple(raw_triples, raw_triple)

    return raw_triple


def _append_root_aux_triple(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
    child_noun = NounEntity(
        get_child_noun(root, nl_question.question)
    )
    grandchild_noun = NounEntity(
        get_child_noun(child_noun.compound_noun[0], nl_question.question)
    )

    if grandchild_noun.is_null():
        # E.g.: "Who is the tallest basketball player?"
        # E.g.: "Who is the youngest Pulitzer Prize winner?"

        # E.g.: "Which is the country where New York is located?"
        obj = NounEntity(
            get_child_noun(root, nl_question.question)
        )

        return _append_rdf_type_triple(nl_question, raw_triples, child_noun, obj)

    if grandchild_noun.noun.head.dep_ == "prep":
        if grandchild_noun.noun.head.text.lower() == "in":
            # E.g.: "What is the highest mountain in Italy?"
            # E.g.: "What is the tallest building in Romania?"
            # E.g.: "What is the highest mountain in the Bavarian Alps?"
            subject = child_noun
            predicate = child_noun.to_span()
            obj = grandchild_noun
            if obj.noun.ent_type_ in ["GPE", "LOC"]:
                # GPE Countries, cities, states
                # LOC Non-GPE locations, mountain ranges, bodies of water
                predicate = QUESTION_TARGET.LOCATION
        else:
            # E.g.: "Who is the manager of Real Madrid?"
            # E.g.: "Who is the leader of the town where the Myntdu river originates?"
            subject = grandchild_noun  # town
            predicate = child_noun.to_span()
            obj = child_noun  # leader

    raw_triple = RawTriple(
        s=subject,
        p=predicate,
        o=obj,
        question=nl_question.question
    )
    _append_raw_triple(raw_triples, raw_triple)

    return raw_triple


def _append_root_target_triple(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
    # E.g.: [1] "Where is Fort Knox located?"
    # E.g.: [2] "Where is the New York Times published?"
    # E.g.: [3] "Where did Mashhur bin Abdulaziz Al Saud's father die?"
    # E.g.: [4] "Where was the designer of REP Parasol born?"

    subject = NounEntity(
        get_child_noun(root, root.sent)
    )
    index = subject.compound_noun[0].i
    obj = NounEntity(
        get_child_noun(subject.compound_noun[0], root.sent[index:])
    )

    if obj.is_null() or not is_followed_by_prep(root):
        # E.g.: obj.is_null() => [1]
        # E.g.: not is_followed_by_prep(root) => [3][4]
        obj = nl_question.target

    if isinstance(obj, str):
        # E.g.: "Which musician wrote the most books?"
        if subject.token not in list(root.rights):
            rights = [noun for noun in list(root.rights) if is_noun(noun)]
            if len(rights) > 0:
                obj = NounEntity(rights[0])

    raw_triple = RawTriple(
        s=subject,
        p=token_to_span(root),
        o=obj,
        question=nl_question.question
    )
    _append_raw_triple(raw_triples, raw_triple)

    return raw_triple


def _append_root_target_prep_triple(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
    # E.g.: [1] "In which country is Mecca located?"
    # E.g.: [2] "At what distance does the earth curve?"

    subject = get_child_noun(root, root.sent)
    obj = get_child_noun(root.sent[0], root.sent)
    predicate = obj

    raw_triple = RawTriple(
        s=subject,
        p=token_to_span(predicate),
        o=obj,
        question=nl_question.question
    )
    _append_raw_triple(raw_triples, raw_triple)

    return raw_triple


def _append_passive_triple(nl_question: NLQuestion, raw_triples: List[RawTriple], subject: NounEntity, predicate: Token):
    raw_triple = None

    sentence = nl_question.question
    if ends_with_verb(sentence):
        # E.g.: "Where was the person who won the oscar born?"
        predicate = get_related_verb(subject.noun, sentence)
        raw_triple = RawTriple(
            s=subject,
            p=token_to_span(predicate),
            o=get_child_noun(predicate, sentence[predicate.i + 1:]),
            question=nl_question.question
        )
        _append_raw_triple(raw_triples, raw_triple)
    else:
        # E.g.: "Where was the person born whose successor was Le Hong Phong?"
        next_verb = get_related_verb(predicate, sentence[predicate.i + 1:])
        predicate = get_child_noun(next_verb, sentence)
        raw_triple = RawTriple(
            s=subject,
            p=token_to_span(predicate),
            o=get_child_noun(next_verb, sentence[next_verb.i + 1:]),
            question=nl_question.question
        )
        _append_raw_triple(raw_triples, raw_triple)

    return raw_triple
