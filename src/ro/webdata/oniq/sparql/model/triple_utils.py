from spacy.tokens import Span, Token

from ro.webdata.oniq.common.nlp.sentence_utils import ends_with_verb, contains_multiple_wh_words
from ro.webdata.oniq.common.nlp.word_utils import is_noun, is_aux, is_verb, is_followed_by_prep
from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.sparql.model.NLQuestion import QUESTION_TARGET
from ro.webdata.oniq.sparql.model.NounEntity import NounEntity
from ro.webdata.oniq.sparql.model.Triples import Triples


class TripleUtils:
    @staticmethod
    def append_rdf_type_triple(triples: Triples, subject, entity: NounEntity):
        for triple in triples.elements:
            if triple.s == subject and str(triple.p) == "rdf:type":
                # E.g.: "Who is the tallest basketball player?"
                return None

        if not entity.is_named_entity:
            resource = LookupService.local_resource_lookup(entity.text)
            return triples.append_triple(subject, "rdf:type", NounEntity(resource, entity.token))

        return None

    @staticmethod
    def append_root_aux_ask_triple(triples: Triples, sentence: Span, root: Token):
        subject = get_child_noun(root, sentence)
        obj = get_child_noun(subject, sentence[subject.i + 1:])

        if obj is None:
            # E.g.: "Did Arnold Schwarzenegger attend a university?"
            noun_list = [token for token in list(root.rights) if token.pos_ == "NOUN"]
            obj = noun_list[0] if len(noun_list) > 0 else None

        if obj is None:
            return None

        return triples.append_triple(subject, root, obj)

    @staticmethod
    def append_root_aux_triple(triples: Triples, sentence: Span, root: Token, target: str):
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
                predicate = child_noun
                obj = grandchild_noun
                if obj.noun.ent_type_ == "GPE":
                    predicate = QUESTION_TARGET.LOCATION
            else:
                # E.g.: "Who is the manager of Real Madrid?"
                # E.g.: "Who is the leader of the town where the Myntdu river originates?"
                subject = grandchild_noun  # town
                predicate = child_noun
                obj = child_noun  # leader

        return triples.append_triple(subject, predicate, obj)

    @staticmethod
    def append_root_target_triple(triples: Triples, root: Token, question_target: str):
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

        return triples.append_triple(subject, root, obj)

    @staticmethod
    def append_root_target_prep_triple(triples: Triples, root: Token):
        # E.g.: [1] "In which country is Mecca located?"
        # E.g.: [2] "At what distance does the earth curve?"

        subject = get_child_noun(root, root.sent)
        obj = get_child_noun(root.sent[0], root.sent)

        return triples.append_triple(subject, obj, obj)

    @staticmethod
    def append_passive_triple(triples: Triples, sentence: Span, subject: NounEntity, predicate: Token):
        triple = None

        if ends_with_verb(sentence):
            # E.g.: "Where was the person who won the oscar born?"

            predicate = get_related_verb(subject.noun, sentence)
            obj = get_child_noun(predicate, sentence[predicate.i + 1:])
            triple = triples.append_triple(subject, predicate, obj)
        else:
            # E.g.: "Where was the person born whose successor was Le Hong Phong?"

            next_verb = get_related_verb(predicate, sentence[predicate.i + 1:])
            predicate = get_child_noun(next_verb, sentence)
            obj = get_child_noun(next_verb, sentence[next_verb.i + 1:])
            triple = triples.append_triple(subject, predicate, obj)

        return triple


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
