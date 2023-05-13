from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.nlp_utils import token_to_span
from ro.webdata.oniq.common.nlp.sentence_utils import ends_with_verb, contains_multiple_wh_words
from ro.webdata.oniq.common.nlp.word_utils import is_noun, is_followed_by_prep, is_preceded_by_adj_modifier, \
    get_prev_word
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.sparql.model.NLQuestion import QUESTION_TARGET, NLQuestion
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.raw_triples.RawQuery import RawQuery
from ro.webdata.oniq.sparql.model.raw_triples.raw_triple_utils import get_related_verb, get_child_noun


class RawQueryUtils:
    @staticmethod
    def aux_processing(raw_query: RawQuery, root: Token, nl_question: NLQuestion):
        # E.g.: "Who is the leader of the town where the Myntdu river originates?"
    
        sentence = root.sent  # TODO: remove
        triple = _append_root_aux_triple(raw_query, sentence, root, nl_question.target)
        # <(town)   (leader)   (leader)>
    
        if triple is None:
            # E.g.: "Who is the tallest basketball player?"
            subject = nl_question.target
            obj = NounEntity(
                get_child_noun(root, sentence)
            )
            triple = _append_rdf_type_triple(raw_query, subject, obj)
    
        if triple is None:
            # E.g.: "Who is the youngest Pulitzer Prize winner?"
            subject = nl_question.target
            predicate = nl_question.target
            obj = NounEntity(
                get_child_noun(root, sentence)
            )
            if obj.noun.dep_ == "attr":
                predicate = obj.to_span()
            triple = raw_query.append_raw_triple(subject, predicate, obj)
    
        if triple is not None:
            _append_rdf_type_triple(raw_query, triple.s, triple.s)
            related_verb = get_related_verb(triple.s.noun, sentence)

            if related_verb is not None:
                subject = get_child_noun(related_verb, sentence)
                predicate = related_verb
                obj = triple.s
                triple = raw_query.append_raw_triple(subject, token_to_span(predicate), obj)
                # <("Myntdu river")   (originates)   (town)>
            else:
                # E.g.: "What is the population and area of the most populated state?"
                # Do nothing
                pass
    
            # add the right side
            # E.g.: Which museum in New York has the most visitors?
            def exists(word):
                for _triple in raw_query:
                    if _triple.o.token == word:
                        # E.g.: "Who is the tallest basketball player?"
                        return True
                return False
    
            rights = [noun for noun in list(root.rights) if is_noun(noun) and not exists(noun)]
    
            if len(rights) > 0:
                for noun in rights:
                    if triple.s.token != noun:
                        # triple.s.token == noun => E.g.: "What is the tallest building in Romania?"
                        triple = raw_query.append_raw_triple(triple.s, token_to_span(noun), noun)
    
        pass

    @staticmethod
    def aux_ask_processing(raw_query: RawQuery, root: Token):
        # E.g.: "Did Arnold Schwarzenegger attend a university?"
    
        sentence = root.sent  # TODO: remove
        triple = _append_root_aux_ask_triple(raw_query, sentence, root)
        # <subject of the root (Schwarzenegger)   predicate (attend)   object (university)>
    
        _append_rdf_type_triple(raw_query, triple.o, triple.o)
        # <(university)   (rdf:type)   (dbo:University)>
    
        pass

    @staticmethod
    def main_processing(raw_query: RawQuery, root: Token, nl_question: NLQuestion):
        # FIXME: "Who won the Pulitzer Prize?"
    
        # ends with a verb
        # E.g.: [1] "Where is the New York Times published?"
        # E.g.: [2] "Where did Mashhur bin Abdulaziz Al Saud's father die?"
    
        triple = _append_root_target_triple(raw_query, root, nl_question.target)
        # [1] <subject of the predicate ("New York Times")   predicate (published)>   target (location)> (NER)
        # [2] <subject of the predicate (father)             predicate (die)          target (location)>
    
        if not triple.o.is_text:
            # E.g.: "Which musician wrote the most books?"
            _append_rdf_type_triple(raw_query, triple.o, triple.o)
    
        subject = get_child_noun(triple.s.compound_noun[0], root.sent)

        if subject is not None:
            # possessive ending (E.g.: [2] => 's)
            pos = [token for token in list(subject.rights) if token.tag_ == "POS"]

            if len(pos) > 0:
                predicate = triple.s.to_span()
                obj = triple.s
                triple = raw_query.append_raw_triple(subject, predicate, obj)
                # [2] <subject ("Mashhur bin Abdulaziz Al Saud")   subject.head (father)   subject.head (father)> (NER)
    
        pass

    @staticmethod
    def passive_processing(raw_query: RawQuery, root: Token, nl_question: NLQuestion):
        # ends with a verb which has a passive verb attached
        # E.g.: [1] "Where is Fort Knox located?"
        # E.g.: [2] "Where was the person who won the oscar born?" [passive attachment]
        # E.g.: [3] "Where was the person born whose successor was Le Hong Phong?" [passive attachment]
        # E.g.: [4] "Where was the designer of REP Parasol born?"
    
        sentence = root.sent  # TODO: remove
        triple = _append_root_target_triple(raw_query, root, nl_question.target)
        # [1] <subject of root ("Fort Knox")   predicate (located)   target (location)> (NER)
        # [2] <subject of root (person)        predicate (born)      target (location)>
        # [3] <subject of root (person)        predicate (born)      target (location)>
        # [4] <subject of root (designer)      predicate (born)      target (location)>
        _append_rdf_type_triple(raw_query, triple.s, triple.s)
    
        if contains_multiple_wh_words(sentence):
            triple = _append_passive_triple(raw_query, sentence, triple.s, triple.p.root)
            # [2] <subject of root (person)    predicate (won)        object (oscar)>
            # [3] <subject of root (person)    predicate (successor)  object ("Le Hong Phong")>
    
        # TODO: make a generic method for adding the pobjs preceded by a preposition
        prep = [token for token in list(triple.s.noun.rights) if token.dep_ == "prep"]
        if len(prep) > 0:
            subject = get_child_noun(triple.p.root, sentence)
            predicate = subject
            obj = get_child_noun(subject, sentence)
            triple = raw_query.append_raw_triple(subject, token_to_span(predicate), obj)
            # [4] <subject of root (designer)   subject of root (designer)  pobj ("REP Parasol")
    
        pass

    @staticmethod
    def possessive_processing(raw_query: RawQuery, root: Token, nl_question: NLQuestion):
        # E.g.: "Whose successor is Le Hong Phong?"  ## made by me

        sentence = root.sent  # TODO: remove
        subject = nl_question.target
        predicate = get_child_noun(root, sentence)
        obj = get_child_noun(root, sentence[root.i + 1:])
        triple = raw_query.append_raw_triple(subject, token_to_span(predicate), obj)

        _append_rdf_type_triple(raw_query, triple.s, triple.s)
    
        pass

    @staticmethod
    def possessive_complex_processing(raw_query: RawQuery, root: Token, nl_question: NLQuestion):
        sentence = root.sent  # TODO: remove
    
        if ends_with_verb(sentence):
            # E.g.: "Where was the person whose successor studied law born?"
    
            subject = get_child_noun(root, root.sent)
            predicate = nl_question.target
            obj = nl_question.target
            # triple = append_root_target_triple(self.triples, root, nl_question.target)
            triple = raw_query.append_raw_triple(subject, predicate, obj)

            related_verb = get_related_verb(triple.s.noun, sentence[subject.i + 1:])
            child_noun = get_child_noun(related_verb, sentence)

            subject = triple.s
            predicate = child_noun
            obj = child_noun
            triple = raw_query.append_raw_triple(subject, token_to_span(predicate), obj)

            subject = child_noun
            predicate = related_verb
            obj = get_child_noun(related_verb, sentence[related_verb.i + 1:])
            triple = raw_query.append_raw_triple(subject, token_to_span(predicate), obj)
    
            pass
        else:
            # E.g.: "Who is the woman whose successor was Le Hong Phong?"
    
            subject = get_child_noun(root, sentence)
            predicate = get_child_noun(subject, sentence)
            obj = get_child_noun(predicate.head, sentence[predicate.i + 1:])
            triple = raw_query.append_raw_triple(subject, token_to_span(predicate), obj)
    
        pass

    @staticmethod
    def verb_ask(raw_query: RawQuery, root: Token):
        sentence = root.sent  # TODO: remove
        child_noun = get_child_noun(root, sentence)
    
        if is_followed_by_prep(child_noun):
            # E.g.: "Give me the currency of China."
            subject = NounEntity(
                get_child_noun(child_noun, sentence)
            )
            predicate = child_noun
            obj = NounEntity(predicate.lemma_)
    
            raw_query.append_raw_triple(subject, token_to_span(predicate), obj)
    
        elif is_preceded_by_adj_modifier(child_noun):
            # E.g.: "Give me all Swedish holidays."
    
            adj_modifier = get_prev_word(child_noun)
            rdf_type = NounEntity(child_noun.lemma_)
            triple = _append_rdf_type_triple(raw_query, rdf_type, rdf_type)
    
            obj = NounEntity(adj_modifier)
            triple = raw_query.append_raw_triple(triple.s, "country", obj)
    
        else:
            # E.g.: "Give me all ESA astronauts."
    
            prev_word = get_prev_word(child_noun)
    
            if prev_word.dep_ == "compound":
                rdf_type = NounEntity(child_noun.lemma_)
                triple = _append_rdf_type_triple(raw_query, rdf_type, rdf_type)
    
                obj = NounEntity(prev_word)
                triple = raw_query.append_raw_triple(triple.s, "prop", obj)
    
        pass

    @staticmethod
    def prep_ask_processing(raw_query: RawQuery, root: Token):
        # E.g.: [1] "In which country is Mecca located?"
        # E.g.: [2] "At what distance does the earth curve?"  # TODO:
    
        triple = _append_root_target_prep_triple(raw_query, root)
        # <subject of the root (Mecca)   object (country)   object (country)>
    
        pass


def _append_rdf_type_triple(raw_query: RawQuery, subject, entity: NounEntity):
    for triple in raw_query.raw_triples:
        if triple.s == subject and str(triple.p) == "rdf:type":
            # E.g.: "Who is the tallest basketball player?"
            return None

    if not entity.is_named_entity:
        resource = LookupService.local_resource_lookup(entity.text)
        return raw_query.append_raw_triple(subject, "rdf:type", NounEntity(resource, entity.token))

    return None


def _append_root_aux_ask_triple(raw_query: RawQuery, sentence: Span, root: Token):
    subject = get_child_noun(root, sentence)
    obj = get_child_noun(subject, sentence[subject.i + 1:])

    if obj is None:
        # E.g.: "Did Arnold Schwarzenegger attend a university?"
        noun_list = [token for token in list(root.rights) if token.pos_ == "NOUN"]
        obj = noun_list[0] if len(noun_list) > 0 else None

    if obj is None:
        return None

    return raw_query.append_raw_triple(subject, token_to_span(root), obj)


def _append_root_aux_triple(raw_query: RawQuery, sentence: Span, root: Token, target: str):
    child_noun = NounEntity(
        get_child_noun(root, sentence)
    )
    grandchild_noun = NounEntity(
        get_child_noun(child_noun.compound_noun[0], sentence)
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

    return raw_query.append_raw_triple(subject, predicate, obj)


def _append_root_target_triple(raw_query: RawQuery, root: Token, question_target: str):
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
        obj = question_target

    if isinstance(obj, str):
        # E.g.: "Which musician wrote the most books?"
        if subject.token not in list(root.rights):
            rights = [noun for noun in list(root.rights) if is_noun(noun)]
            if len(rights) > 0:
                obj = NounEntity(rights[0])

    return raw_query.append_raw_triple(subject, token_to_span(root), obj)


def _append_root_target_prep_triple(raw_query: RawQuery, root: Token):
    # E.g.: [1] "In which country is Mecca located?"
    # E.g.: [2] "At what distance does the earth curve?"

    subject = get_child_noun(root, root.sent)
    obj = get_child_noun(root.sent[0], root.sent)
    predicate = obj

    return raw_query.append_raw_triple(subject, token_to_span(predicate), obj)


def _append_passive_triple(raw_query: RawQuery, sentence: Span, subject: NounEntity, predicate: Token):
    triple = None

    if ends_with_verb(sentence):
        # E.g.: "Where was the person who won the oscar born?"

        predicate = get_related_verb(subject.noun, sentence)
        obj = get_child_noun(predicate, sentence[predicate.i + 1:])
        triple = raw_query.append_raw_triple(subject, token_to_span(predicate), obj)
    else:
        # E.g.: "Where was the person born whose successor was Le Hong Phong?"

        next_verb = get_related_verb(predicate, sentence[predicate.i + 1:])
        predicate = get_child_noun(next_verb, sentence)
        obj = get_child_noun(next_verb, sentence[next_verb.i + 1:])
        triple = raw_query.append_raw_triple(subject, token_to_span(predicate), obj)

    return triple
