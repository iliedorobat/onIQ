from spacy.tokens import Doc, Span, Token
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.nlp.actions import get_action_list
from ro.webdata.oniq.nlp.nlp_utils import get_cardinals, get_chunk, retokenize
from ro.webdata.oniq.nlp.phrase import prepare_phrase_list, get_related_phrase, is_nsubj_wh_word, get_noun_chunks
from ro.webdata.oniq.nlp.word_utils import is_verb, is_part_of_action, is_wh_adverb, is_wh_word


def get_statement_list(document: Doc):
    """
    Get the list of statements generated around the target phrases

    :param document: The parsed document
    :return: A list of statements
    """
    statements = []

    for sentence in document.sents:
        retokenize(document, sentence)
        action_list = get_action_list(sentence)
        statements = _generate_statement_list(sentence, action_list)

        echo.token_list(sentence)
        echo.action_list(action_list)
        echo.statement_list(statements)

    return statements


class ss:
    def __init__(self, text=None):
        self.text = text


def _generate_statement_list(sentence, action_list):
    statements = []

    # TODO: phrase_list = prepare_phrase_list(sentence) => instead of get_noun_chunks???
    noun_chunks = get_noun_chunks(sentence)

    for i, chunk in enumerate(noun_chunks):
        action_head = _get_action_head(chunk.root)
        action = _get_action(action_head, action_list)
        target_chunks = _generate_target_chunks(action_head, noun_chunks)

        if not _is_chunk_in_list(target_chunks, chunk):
            statement = Statement(target_chunks, action, chunk)
            statements.append(statement)

        # E.g.: "Who is very beautiful and very smart?"
        # E.g.: "When does the museum open?"
        # E.g.: "Which of the smart kids are famous?"
        elif len(noun_chunks) == 1:
            first_word = noun_chunks[0][0]
            if not is_nsubj_wh_word(sentence, first_word) and action.acomp_list is not None:
                for acomp in action.acomp_list:
                    new_action = Action(sentence, action.verb, [acomp])
                    statement = Statement(target_chunks, new_action, acomp.token)
                    statements.append(statement)

    return statements


def _get_action(action_head: Token, action_list: [Span]):
    """
    Retrieve the event (Action) to which the action_head belongs

    :param action_head: The prepared head of the chunk (see "_get_action_head")
    :param action_list: The list of events (Actions)
    :return: The event (Action)
    """

    for action in action_list:
        words = action.verb.to_list()
        if action.acomp_list is not None:
            for acomp in action.acomp_list:
                words.append(acomp.token)

        for word in words:
            if action_head == word:
                return action

    return None


def _is_chunk_in_list(chunk_list, input_chunk):
    """
    Determine if the input chunk exists in the provided list of chunks

    :param chunk_list: The list of chunks (use case: "target_chunks")
    :param input_chunk: The chunk to be searched for
    :return: True/False
    """

    for chunk in chunk_list:
        if chunk == input_chunk:
            return True
    return False


def _get_left_edge(action_head):
    left_edge = action_head.left_edge

    # 1. "How many days do I have to wait until the opening?"
    #   => action_head = "wait"
    #   => action_head.left_edge = "to"
    #   => action_head.left_edge.head.head = "have"
    # 2. "How many days do I have to wait until the opening?"
    if (left_edge.pos_ == "PART" and left_edge.tag_ == "TO" and left_edge.dep_ == "aux") or \
            (left_edge.pos_ == "ADP" and left_edge.tag_ == "IN" and left_edge.dep_ == "mark"):
        left_edge = left_edge.head.head

    if not is_verb(left_edge):
        return left_edge
    else:
        return _get_left_edge(action_head.head)


def _generate_target_chunks(action_head: Token, chunk_list: [Span]):
    """
    Generate the list of target chunks

    :param action_head: The prepared head of the chunk (see "_get_action_head")
    :param chunk_list: The list of chunks (use case: "noun_chunks")
    :return: The list of target chunks
    """

    target_chunks = []
    left_edge = _get_left_edge(action_head)

    # "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
    # => "[...] which hosts [...]"
    # => left_edge = "which"
    # => new left_edge = "museum"
    if is_wh_word(left_edge) and left_edge.i > 0:
        left_edge = action_head.sent[left_edge.i - 1]
    left_edge_chunk = get_chunk(chunk_list, left_edge)

    if left_edge_chunk is not None:
        target_chunks.append(left_edge_chunk)

        for conj in left_edge_chunk.conjuncts:
            conj_chunk = get_chunk(chunk_list, conj)
            target_chunks.append(conj_chunk)

    return target_chunks


def _get_action_head(root: Token):
    """
    Retrieve the head of the root

    :param root: The chunk.root
    :return: The head of the root
    """

    head = root.head

    # 2. "When does the museum open?" => "open"
    if is_verb(head) or (head.pos_ == "ADJ" and head.dep_ == "ROOT"):
        return head
    else:
        return _get_action_head(head)
