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
from ro.webdata.oniq.nlp.verbs import prepare_verb_list
from ro.webdata.oniq.nlp.nlp_utils import get_cardinals, get_preposition, get_prev_chunk, get_wh_words, retokenize
from ro.webdata.oniq.nlp.phrase import get_conj_phrases, get_main_noun_chunks, get_noun_chunks, get_phrase, \
    get_phrase_list, get_related_phrase, get_related_wh_phrase, is_nsubj_wh_word


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
        action_list = _get_action_list(sentence)
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
                    # adauga in lista prima actiune
                    if j == 0:
                        action.is_available = False
                        phrase_actions.append(action)
                    else:
                        # adauga in lista urmatoarea actiune care se afla in relatie de conjuctie/disjunctie cu actiunea anterioara:
                        # 1. daca urmatoarea actiune se afla in relatie de conjuctie/disjunctie cu actiunea anterioara
                        # 2. daca anterioara actiune a fost deja atribuita
                        if action.dep == 'conj' \
                                and action_list[j - 1].is_available is False:
                            action.is_available = False
                            phrase_actions.append(action)
                        # 1. daca exista cel putin un statement inregistrat
                        # 2. daca fraza curenta != fraza ultimului statement inregistrat
                        # 3. daca fraza curenta nu este precedata de un verb
                        # acl => 'Which female actor played in Casablanca and has been married to a writer born in Rome and has three children?'
                        # acomp => 'Which female actor played in Casablanca and is married to a writer born in Rome and has three children?'
                        elif len(statements) > 0 \
                                and statements[len(statements) - 1].phrase != phrase \
                                and sentence[first_word.i - 1].dep_ in ["acl", "acomp"]:
                            action.is_available = False
                            phrase_actions.append(action)
                        # 1. daca primul element din fraza este wh-determiner
                        # 2. daca primul element din fraza are dependinta de nsubj
                        # 3. daca dupa primul element se afla un verb
                        # E.g.: "Which is the noisiest and the largest city?"
                        elif first_word.tag_ == "WDT" and first_word.dep_ == "nsubj" and phrase[1].pos_ in ["AUX", "VERB"]:
                            action.is_available = False
                            phrase_actions.append(action)

            # creaza cate un statement pentru fiecare actiune a unei fraze
            for j in range(len(phrase_actions)):
                #         cardinals = get_cardinals(chunk)
                #         logical_operation = LogicalOperation(sentence, chunk)

                next_phrase = get_related_wh_phrase(sentence, i, j) \
                    if is_nsubj_wh_word(sentence, chunk_list, i) \
                    else get_related_phrase(sentence, i, j)
                conj_phrases = [] \
                    if is_nsubj_wh_word(sentence, chunk_list, i) \
                    else get_conj_phrases(sentence, i)
                statements.append(Stmt(phrase_actions[j], phrase, next_phrase))

                for conj_phrase in conj_phrases:
                    statements.append(Stmt(phrase_actions[i], conj_phrase, next_phrase))

        # TODO: Stmt print method
        for stmt in statements:
            console.warning(stmt.actions)
            print(f'{stmt.phrase}      {stmt.related_phrase}')
            print('-----')
        return statements


def _get_action_list(sentence: Span):
    """
    Get the list of actions

    :param sentence: The target sentence
    :return: The list of actions
    """

    verb_list = prepare_verb_list(sentence)
    return [Action(verb) for verb in verb_list]
