import spacy
from spacy.tokens import Span
from iteration_utilities import unique_everseen

from ro.webdata.oniq.common.constants import APP_MODE
from ro.webdata.oniq.common.print_utils import console, echo
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sparql.Query import Query
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.model.sentence.LogicalOperation import LogicalOperation
from ro.webdata.oniq.nlp.verbs import prepare_verb_list
from ro.webdata.oniq.nlp.nlp_utils import get_cardinals, get_preposition, get_prev_chunk, retokenize


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
        action_list = _prepare_action_list(sentence)
        chunks = list(document.noun_chunks)

        echo.token_list(sentence)
        echo.action_list(action_list)
        console.debug(f'len(action_list) = {len(action_list)}')

        for i in range(len(chunks)):
            chunk = chunks[i]
            phrase = _get_phrase(sentence, chunk)
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
                                and sentence[phrase[0].i - 1].dep_ in ["acl", "acomp"]:
                            action.is_available = False
                            phrase_actions.append(action)

            # creaza cate un statement pentru fiecare actiune a unei fraze
            for j in range(len(phrase_actions)):
                #         cardinals = get_cardinals(chunk)
                #         logical_operation = LogicalOperation(sentence, chunk)

                next_phrase = _get_related_phrase(sentence, chunks, i, j)
                statements.append(Stmt(phrase_actions[j], phrase, next_phrase))

                conj_phrases = _get_conj_phrases(sentence, chunks, i)
                for conj_phrase in conj_phrases:
                    statements.append(Stmt(phrase_actions[i], conj_phrase, next_phrase))

        for stmt in statements:
            console.warning(stmt.actions)
            print(f'{stmt.phrase}      {stmt.related_phrase}')
            print('-----')
        return statements


def _prepare_action_list(sentence: Span):
    action_list = []
    verb_list = prepare_verb_list(sentence)

    for verb in verb_list:
        action_list.append(Action(verb))

    return action_list


def _get_conj_phrases(sentence, chunks, chunk_index):
    conj_chunks = list(filter(lambda chunk: chunk.root.dep_ == "conj" and chunk != chunks[chunk_index], chunks))
    return list(map(lambda chunk: _get_phrase(sentence, chunk), conj_chunks))


def _get_related_phrase(sentence: Span, chunks: [Span], chunk_index: int = 0, action_index: int = 0, increment: int = 1):
    index = chunk_index + action_index + increment
    if index >= len(chunks):
        return None
    if chunks[index].root.dep_ == 'conj':
        # e.g.: 'Which painting, swords or statues do not have more than three owners?'
        return _get_related_phrase(sentence, chunks, chunk_index, action_index, increment + 1)
    else:
        return _get_phrase(sentence, chunks[index])


# create a phrase by adding the preposition to the chunk
def _get_phrase(sentence: Span, chunk: Span):
    preposition = get_preposition(sentence, chunk)
    first_index = preposition.i if preposition is not None else chunk[0].i
    last_index = chunk[len(chunk) - 1].i + 1
    return sentence[first_index: last_index]
