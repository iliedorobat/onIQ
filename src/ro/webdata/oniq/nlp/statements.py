from ro.webdata.oniq.common.constants import PRONOUNS, SENTENCE_TYPE
from ro.webdata.oniq.nlp.nouns import get_nouns
from ro.webdata.oniq.nlp.nlp_utils import get_wh_pronouns, get_wh_words


def get_stmt_type(chunk, statements):
    if chunk.text.lower() in PRONOUNS:
        return SENTENCE_TYPE.PRON
    # "who is the director who own..." => classify only the first chunk
    # which contains the "who" word as being TYPE_WH_PRON_START
    elif chunk.root in get_wh_pronouns(chunk):
        return SENTENCE_TYPE.WH_PRON_START if chunk.root.i == 0 else SENTENCE_TYPE.WH
    elif chunk.root in get_wh_words(chunk):
        return SENTENCE_TYPE.WH_START if chunk.root.i == 0 else SENTENCE_TYPE.WH
    # if the type of the first sentence is not TYPE_PRON or TYPE_WH_START,
    # then the target subjects are found in the first sentence
    elif len(statements) == 0:
        return SENTENCE_TYPE.SELECT_CLAUSE
    else:
        nouns = get_nouns(chunk)
        conj_nouns = list(filter(lambda noun: noun.dep == "conj", nouns))
        prev_statement = _get_last_statement(statements)

        if prev_statement.type in [SENTENCE_TYPE.PRON, SENTENCE_TYPE.WH_PRON_START, SENTENCE_TYPE.WH_START]:
            return SENTENCE_TYPE.SELECT_CLAUSE
        elif prev_statement.type == SENTENCE_TYPE.SELECT_CLAUSE and len(conj_nouns) > 0:
            return SENTENCE_TYPE.SELECT_CLAUSE
        else:
            return SENTENCE_TYPE.WHERE_CLAUSE


def _get_last_statement(statements):
    if len(statements) > 0:
        return statements[len(statements) - 1]
    return None
