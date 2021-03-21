from spacy.tokens import Doc, Span
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.constants import PRINT_MODE
from ro.webdata.oniq.common.print_utils import echo
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Phrase import Phrase
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.nlp.actions import get_action_list
from ro.webdata.oniq.nlp.nlp_utils import get_cardinals, retokenize
from ro.webdata.oniq.nlp.phrase import get_phrase_list, get_related_phrase, get_related_phrases, \
    get_related_wh_phrase, get_target_phrases, is_nsubj_wh_word


def consolidate_statement_list(document: Doc):
    """
    Consolidate the list of statements by grouping the statements which
    have the same action and target_phrase into a new statement

    :param document: The parsed document
    :return: The consolidated list of statements
    """

    statements = _get_statement_list(document)
    prepared_list = [statements[0]] if len(statements) > 0 else []

    if len(statements) > 1:
        aux_stmt = statements[0] if len(statements) > 0 else None

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
                prepared_list.append(crr_stmt)
                aux_stmt = crr_stmt

    echo.statement_list(prepared_list, PRINT_MODE.PRINT_CONSOLIDATED_STATEMENT)

    return prepared_list


def _get_statement_list(document: Doc):
    """
    Get the list of statements generated around the target phrases

    :param document: The parsed document
    :return: A list of statements
    """
    statements = []

    for sentence in document.sents:
        retokenize(document, sentence)
        action_list = get_action_list(sentence)
        phrase_list = get_phrase_list(sentence)

        for index, phrase in enumerate(phrase_list):
            target_actions = _get_target_actions(sentence, phrase_list, index, action_list, statements)
            target_statements = _get_target_statements(sentence, phrase_list, index, target_actions)
            statements = statements + target_statements

        echo.token_list(sentence)
        echo.action_list(action_list)
        echo.statement_list(statements)

    return statements


def _get_target_actions(sentence: Span, phrase_list: [Phrase], phrase_index: int, action_list: [Action], statements: [Statement]):
    """
    Get the list of events (Actions) in which the target phrase is involved

    :param sentence: The target sentence
    :param phrase_list: The list of phrases
    :param phrase_index: The index of the current phrase
    :param action_list: The list of events (actions)
    :param statements: The list of generated statements
    :return: The list of target events (Actions)
    """

    target_actions = []
    phrase = phrase_list[phrase_index]
    first_word = phrase.content[0]
    next_phrase = phrase_list[phrase_index + 1] \
        if len(phrase_list) - 1 > phrase_index \
        else None

    for index, action in enumerate(action_list):
        target_phrases = get_target_phrases(sentence, phrase_list, phrase_index, action)
        last_target_phrase = target_phrases[len(target_phrases) - 1] if len(target_phrases) > 1 else None

        if action.is_available is True and (last_target_phrase is None or action.i == last_target_phrase.end + 1):
            is_first_action = index == 0
            is_prev_action_available = action_list[index - 1].is_available

            # Add the first action to the action list
            if is_first_action is True:
                # 1. check if the phrase is not the last
                # 2. check if the next phrase is not a "target phrase" (the index
                # of the first item is greater than the index of the action)
                # E.g.: "Which is the noisiest and the largest city?"
                if next_phrase is None or next_phrase.content.start > action.i:
                    action.is_available = False
                target_actions.append(action)
            # Add the rest of actions to the action list
            else:
                # 1. Check if the next action is in the relation of 'conj'
                # 2. Check if the previous action has already been assigned to a phrase
                if action.dep == 'conj' and is_prev_action_available is False:
                    action.is_available = False
                    target_actions.append(action)

                # 1. Check if at least one statement has already been added
                # 2. Check if the current phrase != the phrase of the last statement
                elif len(statements) > 0 and statements[len(statements) - 1].phrase.content != phrase.content:
                    # 1. TODO: documentation
                    # 2. Check if the previous action has already been assigned to a phrase
                    # E.g.: "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
                    if action.dep == "relcl" and is_prev_action_available is False:
                        action.is_available = False
                        target_actions.append(action)

                    # Check if the current phrase is not preceded by a verb
                    # acl => "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?"
                    # acomp => "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?"
                    elif sentence[first_word.i - 1].dep_ in ["acl", "acomp"]:
                        action.is_available = False
                        target_actions.append(action)

                    # Check if the current phrase is followed by an adjectival clause/complement
                    # E.g.: "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?"
                    elif sentence[phrase.end + 1].dep_ in ["acl", "acomp"]:
                        action.is_available = False
                        target_actions.append(action)

                    # Check if the word before the first element of the action is a nominal subject or not
                    # E.g.: "When did Lena Horne receive the Grammy Award for Best Jazz Vocal Album?" [1]
                    elif sentence[action.i - 1].dep_ == "nsubj":
                        action.is_available = False
                        target_actions.append(action)

    return target_actions


def _get_target_statements(sentence: Span, phrase_list: [Phrase], phrase_index: int, target_actions: [Action]):
    """
    Get the list of statements generated around the target phrase

    :param sentence: The target sentence
    :param phrase_list: The list of phrases
    :param phrase_index: The index of the current phrase
    :param target_actions: The list of events in which the target phrase is involved
    :return: The list of target statements
    """

    statements = []
    first_word = phrase_list[phrase_index].content[0]

    # Create a statement for each action
    for action_index, action in enumerate(target_actions):
        # TODO: cardinals = get_cardinals(chunk)

        next_phrase = _get_next_phrase(sentence, phrase_list, phrase_index, action_index)
        related_phrases = get_related_phrases(sentence, phrase_index, action)
        # E.g.: "Which is the museum which hosts more than 10 pictures and exposed one sword?"
        statement = Statement(phrase_list, phrase_index, action, [next_phrase])
        statements.append(statement)

        for j, related_phrase in enumerate(related_phrases):
            if first_word.pos_ == "DET" and first_word.tag_ == "WDT":
                if first_word.dep_ == "det":
                    # E.g.: "Which paintings, swords or statues do not have more than three owners?"
                    statement = Statement(related_phrases, j, action, [next_phrase])
                    statements.append(statement)

                elif first_word.dep_ == "nsubj":
                    if sentence[first_word.i + 1].pos_ in ["AUX", "VERB"]:
                        # E.g.: "Which is the noisiest and the most beautiful city?"
                        related_phrase.meta_prep = statements[len(statements) - 1].related_phrases[0].prep
                        statement = Statement(phrase_list, phrase_index, action, [related_phrase])
                        statements.append(statement)
                    else:
                        # E.g.: "Which paintings, white swords or statues do not have more than three owners?"
                        statement = Statement(related_phrases, j, action, [next_phrase])
                        statements.append(statement)
            else:
                # E.g.: "What museums are in Bacau or Bucharest?"
                # E.g.: "Who is the most beautiful woman and the most generous person?"
                related_phrase.meta_prep = statements[len(statements) - 1].related_phrases[0].prep
                statement = Statement(phrase_list, phrase_index, action, [related_phrase])
                statements.append(statement)

    return statements


def _get_next_phrase(sentence: Span, phrase_list: [Phrase], phrase_index: int, action_index: int):
    """
    Get he phrase which is the object of the current iterated action

    :param sentence: The target sentence
    :param phrase_list: The list of phrases
    :param phrase_index: The index of the current iterated phrase
    :param action_index: The index of the current iterated action
    :return: The phrase which is the object of the current iterated action
    """

    phrase = phrase_list[phrase_index]
    if is_nsubj_wh_word(sentence, phrase.content):
        return get_related_wh_phrase(sentence, phrase_index, action_index)
    return get_related_phrase(sentence, phrase_index, action_index)
