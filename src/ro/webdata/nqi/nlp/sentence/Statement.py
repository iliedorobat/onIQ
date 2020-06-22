from ro.webdata.nqi.nlp.sentence.Noun import get_nouns
from ro.webdata.nqi.nlp.sentence.utils import PRONOUNS, SENTENCE_TYPE, get_wh_pronouns, get_wh_words


class Statement:
    def __init__(self, action, cardinality_constr, phrase, statements):
        self.action = action
        self.cardinality_constr = cardinality_constr
        self.phrase = phrase
        self.type = get_stmt_type(phrase, statements)


def get_stmt_type(chunk, statements):
    if chunk.text.lower() in PRONOUNS:
        return SENTENCE_TYPE["PRONOUN"]
    # "who is the director who own..." => classify only the first chunk which contains
    # the "who" word as being WH_PRONOUN_START
    elif chunk.root in get_wh_pronouns(chunk):
        if chunk.root.i == 0:
            return SENTENCE_TYPE["WH_PRONOUN_START"]
        else:
            return SENTENCE_TYPE["WH_START"]
    elif chunk.root in get_wh_words(chunk) and chunk.root.i == 0:
        return SENTENCE_TYPE["WH_START"]
    # if the type of the first sentence is not SENTENCE_TYPE["PRONOUN"] or SENTENCE_TYPE["WH_START"],
    # then the target subjects are found in the first sentence
    elif len(statements) == 0:
        return SENTENCE_TYPE["SELECT_CLAUSE"]
    else:
        nouns = get_nouns(chunk)
        conj_nouns = list(filter(lambda noun: noun["dependency"] == "conj", nouns))
        prev_statement = get_last_statement(statements)

        if prev_statement.type in [SENTENCE_TYPE["PRONOUN"], SENTENCE_TYPE["WH_START"], SENTENCE_TYPE["WH_PRONOUN_START"]]:
            return SENTENCE_TYPE["SELECT_CLAUSE"]
        elif prev_statement.type == SENTENCE_TYPE["SELECT_CLAUSE"] and len(conj_nouns) > 0:
            return SENTENCE_TYPE["SELECT_CLAUSE"]
        else:
            return SENTENCE_TYPE["WHERE_CLAUSE"]


def get_last_statement(statements):
    if len(statements) > 0:
        return statements[len(statements) - 1]
    return None
