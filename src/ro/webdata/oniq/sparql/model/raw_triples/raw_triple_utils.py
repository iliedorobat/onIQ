from typing import List

from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span
from ro.webdata.oniq.common.nlp.sentence_utils import ends_with_verb, contains_multiple_wh_words
from ro.webdata.oniq.common.nlp.word_utils import is_noun, is_followed_by_prep, is_preceded_by_adj_modifier, \
    get_prev_word, is_verb, is_aux
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.sparql.model.NLQuestion import QUESTION_TARGET, NLQuestion
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawTriple import RawTriple


class RawTripleUtils:
    @staticmethod
    def aux_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        # E.g.: "Who is the leader of the town where the Myntdu river originates?"
        triple = _append_root_aux_triple(nl_question, raw_triples, root)
        # <(town)   (leader)   (leader)>

        if triple is None:
            # E.g.: "Who is the tallest basketball player?"
            subject = nl_question.target
            obj = NounEntity(
                get_child_noun(root, nl_question.question)
            )
            triple = _append_rdf_type_triple(nl_question, raw_triples, subject, obj)

        if triple is None:
            # E.g.: "Who is the youngest Pulitzer Prize winner?"
            subject = nl_question.target
            predicate = nl_question.target
            obj = NounEntity(
                get_child_noun(root, nl_question.question)
            )
            if obj.noun.dep_ == "attr":
                predicate = obj.to_span()

            raw_triple = RawTriple(subject, predicate, obj)
            _append_raw_triple(raw_triples, raw_triple)

        if triple is not None:
            _append_rdf_type_triple(nl_question, raw_triples, triple.s, triple.s)
            related_verb = get_related_verb(triple.s.noun, nl_question.question)

            if related_verb is not None:
                raw_triple = RawTriple(
                    s=get_child_noun(related_verb, nl_question.question),
                    p=token_to_span(related_verb),
                    o=triple.s
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
                            o=noun
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

        if not triple.o.is_text:
            # E.g.: "Which musician wrote the most books?"
            _append_rdf_type_triple(nl_question, raw_triples, triple.o, triple.o)

        subject = get_child_noun(triple.s.compound_noun[0], root.sent)

        if subject is not None:
            # possessive ending (E.g.: [2] => 's)
            pos = [token for token in list(subject.rights) if token.tag_ == "POS"]

            if len(pos) > 0:
                raw_triple = RawTriple(
                    s=subject,
                    p=triple.s.to_span(),
                    o=triple.s
                )
                _append_raw_triple(raw_triples, raw_triple)
                # [2] <subject ("Mashhur bin Abdulaziz Al Saud")   subject.head (father)   subject.head (father)> (NER)

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
                o=get_child_noun(subject, nl_question.question)
            )
            _append_raw_triple(raw_triples, raw_triple)
            # [4] <subject of root (designer)   subject of root (designer)  pobj ("REP Parasol")

        pass

    @staticmethod
    def possessive_processing(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
        # E.g.: "Whose successor is Le Hong Phong?"  ## made by me

        predicate = get_child_noun(root, nl_question.question)
        raw_triple = RawTriple(
            s=nl_question.target,
            p=token_to_span(predicate),
            o=get_child_noun(root, nl_question.question[root.i + 1:])
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
                o=nl_question.target
            )
            _append_raw_triple(raw_triples, raw_triple)

            related_verb = get_related_verb(raw_triple.s.noun, nl_question.question[subject.i + 1:])
            child_noun = get_child_noun(related_verb, nl_question.question)

            raw_triple = RawTriple(
                s=raw_triple.s,
                p=token_to_span(child_noun),
                o=child_noun
            )
            _append_raw_triple(raw_triples, raw_triple)

            raw_triple = RawTriple(
                s=child_noun,
                p=token_to_span(related_verb),
                o=get_child_noun(related_verb, nl_question.question[related_verb.i + 1:])
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
                o=get_child_noun(predicate.head, nl_question.question[predicate.i + 1:])
            )
            _append_raw_triple(raw_triples, raw_triple)

        pass

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
                o=NounEntity(child_noun.lemma_, child_noun)
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
                o=NounEntity(adj_modifier)
            )
            _append_raw_triple(raw_triples, raw_triple)

        else:
            # E.g.: "Give me all ESA astronauts."
            prev_word = get_prev_word(child_noun)

            if prev_word.dep_ == "compound":
                rdf_type = NounEntity(child_noun.lemma_, child_noun)
                triple = _append_rdf_type_triple(nl_question, raw_triples, rdf_type, rdf_type)

                # TODO: pass o=prev_word ???
                raw_triple = RawTriple(
                    s=triple.s,
                    p="prop",
                    o=NounEntity(prev_word)
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


def get_child_noun(word: Token, span: Span):
    for token in span:
        if token.i > word.i and token.pos_ == "ADP":
            # E.g.: "Who is the leader of the town where the Myntdu river originates?"
            return get_child_noun(token, token.sent[token.i + 1:])

        # "Where was the designer of REP Parasol born?"
        is_auxpass = is_aux(token.head) and token.head.head == word

        if token.head == word or is_auxpass:
            if token.dep_ == "auxpass":
                if contains_multiple_wh_words(word.sent):
                    if ends_with_verb(span):
                        # E.g.: ### "Where was the person who won the oscar born?"
                        return get_child_noun(token, token.sent[token.i + 1:])
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


def _append_rdf_type_triple(nl_question: NLQuestion, raw_triples: List[RawTriple], subject: [str, NounEntity], entity: NounEntity):
    for triple in raw_triples:
        if triple.s == subject and str(triple.p) == "rdf:type":
            # E.g.: "Who is the tallest basketball player?"
            return None

    resource = LookupService.local_resource_lookup(entity.text)
    raw_triple = RawTriple(
        s=subject,
        p="rdf:type",
        o=NounEntity(resource, entity.token)
    )
    _append_raw_triple(raw_triples, raw_triple)

    return raw_triple


def _append_root_aux_ask_triple(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
    subject = get_child_noun(root, nl_question.question)
    obj = get_child_noun(subject, nl_question.question[subject.i + 1:])

    if obj is None:
        # E.g.: "Did Arnold Schwarzenegger attend a university?"
        noun_list = [token for token in list(root.rights) if token.pos_ == "NOUN"]
        obj = noun_list[0] if len(noun_list) > 0 else None

    # TODO: remove ???
    if obj is None:
        return None

    raw_triple = RawTriple(
        s=subject,
        p=token_to_span(root),
        o=obj
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
        return None

    if grandchild_noun.noun.head.dep_ == "prep":
        if grandchild_noun.noun.head.text.lower() == "in":
            # E.g.: "What is the highest mountain in Italy?"
            # E.g.: "What is the tallest building in Romania?"
            subject = child_noun
            predicate = child_noun.to_span()
            obj = grandchild_noun
            if obj.noun.ent_type_ == "GPE":
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
        o=obj
    )
    _append_raw_triple(raw_triples, raw_triple)

    return raw_triple


def _append_root_target_triple(nl_question: NLQuestion, raw_triples: List[RawTriple], root: Token):
    # E.g.: [1] "Where is Fort Knox located?"
    # E.g.: [2] "Where is the New York Times published?"
    # E.g.: [3] "Where did Mashhur bin Abdulaziz Al Saud's father die?"
    # E.g.: [4] "Where was the designer of REP Parasol born?"
    # E.g.: [5] "Which soccer players were born on Malta?"

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
        o=obj
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
        o=obj
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
            o=get_child_noun(predicate, sentence[predicate.i + 1:])
        )
        _append_raw_triple(raw_triples, raw_triple)
    else:
        # E.g.: "Where was the person born whose successor was Le Hong Phong?"
        next_verb = get_related_verb(predicate, sentence[predicate.i + 1:])
        predicate = get_child_noun(next_verb, sentence)
        raw_triple = RawTriple(
            s=subject,
            p=token_to_span(predicate),
            o=get_child_noun(next_verb, sentence[next_verb.i + 1:])
        )
        _append_raw_triple(raw_triples, raw_triple)

    return raw_triple
