from typing import Union
from spacy.tokens import Doc, Span
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.constants import PRINT_MODE
from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.model.sentence.LogicalOperation import LogicalOperation
from ro.webdata.oniq.nlp.actions import get_action_list
from ro.webdata.oniq.nlp.nlp_utils import get_cardinals, retokenize
from ro.webdata.oniq.nlp.phrase import get_conj_phrases, get_main_noun_chunks, get_related_phrase, \
    get_related_wh_phrase, is_nsubj_wh_word


def consolidate_statement_list(document):
    """
    Consolidate the list of statements by grouping the statements which
    have the same action and target_phrase into a new statement

    :param document: The parsed document
    :return: The consolidated list of statements
    """

    statements = _get_statement_list(document)
    aux_stmt = statements[0] if len(statements) > 0 else None
    prepared_list = []

    if len(statements) == 1:
        prepared_list.append(aux_stmt)

    for i in range(1, len(statements)):
        crr_stmt = statements[i]
        prev_stmt = statements[i - 1]
        is_similar_stmt = Statement.is_similar_statement(crr_stmt, prev_stmt)

        if is_similar_stmt is True:
            related_phrases = aux_stmt.related_phrases + crr_stmt.related_phrases
            aux_stmt.related_phrases = list(unique_everseen(related_phrases))

            if i == len(statements) - 1:
                prepared_list.append(aux_stmt)
        elif is_similar_stmt is False:
            prepared_list.append(aux_stmt)
            aux_stmt = crr_stmt

    echo.statement_list(prepared_list, PRINT_MODE.PRINT_CONSOLIDATED_STATEMENT)

    return prepared_list


def _get_statement_list(document):
    """
    Get the list of statements generated around the target phrases

    :param document: The parsed document
    :return: A list of statements
    """
    statements = []

    for sentence in document.sents:
        retokenize(document, sentence)
        action_list = get_action_list(sentence)
        chunk_list = get_main_noun_chunks(sentence)

        for index, chunk in enumerate(chunk_list):
            target_phrase = Phrase(sentence, chunk, True)
            target_actions = _get_target_actions(sentence, target_phrase, action_list, statements)
            target_statements = _get_target_statements(sentence, target_phrase, target_actions, chunk_list, index)
            statements = statements + target_statements

        echo.token_list(sentence)
        echo.action_list(action_list)
        echo.statement_list(statements)

    return statements


def _get_target_actions(sentence: Span, phrase: Phrase, action_list: [Action], statements: [Statement]):
    """
    Get the list of events (actions) in which the target phrase is involved

    :param sentence: The target sentence
    :param phrase: The target phrase
    :param action_list: The list of events (actions)
    :param statements: The list of generated statements
    :return: The list of target events (actions)
    """

    target_actions = []
    first_word = phrase.content[0]

    for index, action in enumerate(action_list):
        if action.is_available is True:
            is_first_action = index == 0
            is_prev_action_available = action_list[index - 1].is_available

            # Add the first action to the action list
            if is_first_action is True:
                action.is_available = False
                target_actions.append(action)
            # Add the rest of actions to the action list
            else:
                # 1. Check if the next action is in the relation of 'conj'
                # 2. Check if the previous action has already been assigned to a phrase
                if action.dep == 'conj' and is_prev_action_available is False:
                    action.is_available = False
                    target_actions.append(action)

                # TODO: documentation: 'what is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
                # 1. Check if at least one statement has already been added
                # 2. TODO: documentation
                # 3. Check if the previous action has already been assigned to a phrase
                # E.g.: "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
                elif len(statements) > 0 and action.dep == "relcl" and is_prev_action_available is False:
                    action.is_available = False
                    target_actions.append(action)

                # 1. Check if at least one statement has already been added
                # 2. Check if the current phrase != the phrase of the last statement
                # 3. Check if the current phrase is not preceded by a verb
                # acl => "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?"
                # acomp => "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?"
                elif len(statements) > 0 \
                        and statements[len(statements) - 1].phrase.content != phrase.content \
                        and sentence[first_word.i - 1].dep_ in ["acl", "acomp"]:
                    action.is_available = False
                    target_actions.append(action)

                # 1. Check if at least one statement has already been added
                # 2. Check if the current phrase != the phrase of the last statement
                # 3. Check if the current phrase is followed by a verb
                # E.g.: "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?"
                elif len(statements) > 0 \
                        and statements[len(statements) - 1].phrase.content != phrase.content \
                        and sentence[phrase.content[len(phrase.content) - 1].i + 1].dep_ in ["acl", "acomp"]:
                    action.is_available = False
                    target_actions.append(action)

    return target_actions


def _get_target_statements(sentence: Span, phrase: Phrase, target_actions: [Action], chunk_list: [Span], chunk_index: int):
    """
    Get the list of statements generated around the target phrase

    :param sentence: The target sentence
    :param phrase: The target phrase
    :param target_actions: The list of events in which the target phrase is involved
    :param chunk_list: The list of chunks
    :param chunk_index: The index of the current iterated chunk
    :return: The list of target statements
    """

    statements = []
    first_word = phrase.content[0]

    # Create a statement for each action
    for index, action in enumerate(target_actions):
        # TODO: cardinals = get_cardinals(chunk)
        # TODO: logical_operation = LogicalOperation(sentence, chunk)

        next_phrase = _get_next_phrase(sentence, chunk_list, chunk_index, index)
        conj_phrases = get_conj_phrases(sentence, chunk_index)
        # E.g.: "Which is the museum which hosts more than 10 pictures and exposed one sword?"
        statements.append(Statement(phrase, action, [next_phrase]))

        for conj_phrase in conj_phrases:
            if first_word.pos_ == "DET" and first_word.tag_ == "WDT":
                if first_word.dep_ == "det":
                    # E.g.: "Which paintings, swords or statues do not have more than three owners?"
                    conj_phrase.is_target = True
                    statements.append(Statement(conj_phrase, action, [next_phrase]))
                if first_word.dep_ == "nsubj":
                    if sentence[first_word.i + 1].pos_ in ["AUX", "VERB"]:
                        # E.g.: "Which is the noisiest and the most beautiful city?"
                        conj_phrase.meta_prep = statements[len(statements) - 1].related_phrases[0].prep
                        statements.append(Statement(phrase, action, [conj_phrase]))
                    else:
                        # E.g.: "Which paintings, white swords or statues do not have more than three owners?"
                        conj_phrase.is_target = True
                        statements.append(Statement(conj_phrase, action, [next_phrase]))
            else:
                # E.g.: "Who is the most beautiful woman and the most generous person?"
                conj_phrase.meta_prep = statements[len(statements) - 1].related_phrases[0].prep
                statements.append(Statement(phrase, action, [conj_phrase]))

    return statements


def _get_next_phrase(sentence: Span, chunk_list: [Span], chunk_index: int, action_index: int):
    chunk = chunk_list[chunk_index]

    if is_nsubj_wh_word(sentence, chunk):
        return get_related_wh_phrase(sentence, chunk_index, action_index)
    return get_related_phrase(sentence, chunk_index, action_index)
