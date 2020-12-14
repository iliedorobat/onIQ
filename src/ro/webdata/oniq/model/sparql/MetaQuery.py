from typing import Union

import spacy
from spacy.tokens import Doc, Span
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.constants import APP_MODE
from ro.webdata.oniq.common.print_utils import console, echo
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sparql.Query import Query
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.model.sentence.LogicalOperation import LogicalOperation
from ro.webdata.oniq.nlp.actions import get_action_list
from ro.webdata.oniq.nlp.nlp_utils import get_cardinals, get_preposition, is_wh_noun_phrase, retokenize
from ro.webdata.oniq.nlp.phrase import get_conj_phrases, get_main_noun_chunks, get_phrase, get_related_phrase, \
    get_related_wh_phrase, is_nsubj_wh_word


nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5')
# nlp = spacy.load('../../../../lib/en_core_web_md/en_core_web_md-2.2.5')


_QUERY_SKELETON = "{prefixes}" \
                  "SELECT {targets}" \
                  "WHERE {{" \
                  "{where_block}" \
                  "{filter_statement}" \
                  "}}"


class MetaQuery:
    # nl_query: The query provided by the user in natural language
    def __init__(self, endpoint, nl_query):
        # TODO: nlp("document", disable=["parser"])
        document = nlp(nl_query)
        statements = _prepare_statement_list(document)
        # query = Query(endpoint, statements)
        #
        # self.query = _QUERY_SKELETON.format(
        #     prefixes=Query.get_prefixes(endpoint),
        #     targets=query.get_targets_str(),
        #     where_block=query.get_where_block(),
        #     filter_statement=query.get_filter_block()
        # )
        #
        # if APP_MODE.IS_DEBUG:
        #     print(query)
        #     echo.statements(statements)
        #     print(self.query)
        #
        # # nlp_query = nlp(nl_query)
        # # displacy.serve(nlp_query, style="dep")


class Stmt:
    # TODO: merge it with the Statement class
    #    phrase                      related phrase
    # ---------------                 --------
    # Which paintings are not located in Bacau?
    def __init__(self, action, phrase, related_phrase):
        self.actions = action
        self.phrase = phrase
        self.related_phrase = related_phrase


def _prepare_statement_list(document):
    """
    TODO: update the documentation
    Build the list of statements\n
    Example of statement:\n
    ...

    :param document: The parsed document
    :return: A list of statements
    """
    statements = []

    for sentence in document.sents:
        retokenize(document, sentence)
        action_list = get_action_list(sentence)
        chunk_list = get_main_noun_chunks(sentence)

        echo.token_list(sentence)
        echo.action_list(action_list)
        console.debug(f'len(action_list) = {len(action_list)}')

        for i in range(len(chunk_list)):
            chunk = chunk_list[i]
            phrase = get_phrase(sentence, chunk)
            first_word = phrase[0]
            phrase_actions = []

            for j in range(len(action_list)):
                action = action_list[j]

                if action.is_available is True:
                    is_first_action = j == 0
                    is_prev_action_available = action_list[j - 1].is_available

                    # Add the first action to the action list
                    if is_first_action is True:
                        action.is_available = False
                        phrase_actions.append(action)
                    # Add the rest of actions to the action list
                    else:
                        # 1. Check if the next action is in the relation of 'conj'
                        # 2. Check if the previous action has already been assigned to a phrase
                        if action.dep == 'conj' and is_prev_action_available is False:
                            action.is_available = False
                            phrase_actions.append(action)

                        # TODO: documentation: 'what is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
                        # 1. Check if at least one statement has already been added
                        # 2. TODO: documentation
                        # 3. Check if the previous action has already been assigned to a phrase
                        # E.g.: "What is the name of the largest museum which hosts more than 10 pictures and exposed one sword?"
                        elif len(statements) > 0 and action.dep == "relcl" and is_prev_action_available is False:
                            action.is_available = False
                            phrase_actions.append(action)

                        # 1. Check if at least one statement has already been added
                        # 2. Check if the current phrase != the phrase of the last statement
                        # 3. Check if the current phrase is not preceded by a verb
                        # acl => "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?"
                        # acomp => "Which female actor played in Casablanca and is married to a writer born in Rome and has three children?"
                        elif len(statements) > 0 \
                                and statements[len(statements) - 1].phrase != phrase \
                                and sentence[first_word.i - 1].dep_ in ["acl", "acomp"]:
                            action.is_available = False
                            phrase_actions.append(action)

                        # 1. Check if at least one statement has already been added
                        # 2. Check if the current phrase != the phrase of the last statement
                        # 3. Check if the current phrase is followed by a verb
                        # E.g.: "Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?"
                        elif len(statements) > 0 \
                                and statements[len(statements) - 1].phrase != phrase \
                                and sentence[phrase[len(phrase) - 1].i + 1].dep_ in ["acl", "acomp"]:
                            action.is_available = False
                            phrase_actions.append(action)

            # Create a statement for each action
            for j in range(len(phrase_actions)):
                # cardinals = get_cardinals(chunk)
                # logical_operation = LogicalOperation(sentence, chunk)

                next_phrase = get_related_wh_phrase(sentence, i, j) \
                    if is_nsubj_wh_word(sentence, chunk_list, i) \
                    else get_related_phrase(sentence, i, j)
                conj_phrases = get_conj_phrases(sentence, j)

                # E.g.: "Which is the museum which hosts more than 10 pictures and exposed one sword?"
                statements.append(Stmt(phrase_actions[j], phrase, next_phrase))

                for conj_phrase in conj_phrases:
                    if first_word.pos_ == "DET" and first_word.tag_ == "WDT":
                        if first_word.dep_ == "det":
                            # E.g.: "Which paintings, swords or statues do not have more than three owners?"
                            statements.append(Stmt(phrase_actions[j], conj_phrase, next_phrase))
                        if first_word.dep_ == "nsubj":
                            if sentence[first_word.i + 1].pos_ in ["AUX", "VERB"]:
                                # E.g.: "Which is the noisiest and the most beautiful city?"
                                statements.append(Stmt(phrase_actions[j], phrase, conj_phrase))
                            else:
                                # E.g.: "Which paintings, white swords or statues do not have more than three owners?"
                                statements.append(Stmt(phrase_actions[j], conj_phrase, next_phrase))
                    else:
                        # E.g.: "Who is the most beautiful woman and the most generous person?"
                        statements.append(Stmt(phrase_actions[j], phrase, conj_phrase))

        # TODO: Stmt print method
        for stmt in statements:
            console.warning(stmt.actions)
            print(f'{stmt.phrase}      {stmt.related_phrase}')
            print('-----')
        return statements
