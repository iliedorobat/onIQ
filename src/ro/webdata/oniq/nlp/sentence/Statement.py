from spacy.tokens import Span, Token

from ro.webdata.nqi.nlp.sentence.Action import Action
from ro.webdata.nqi.nlp.sentence.Noun import get_nouns
from ro.webdata.nqi.nlp.sentence.constants import PRONOUNS, TYPE_PRON, TYPE_WH, TYPE_WH_PRON_START, TYPE_WH_START, \
    TYPE_SELECT_CLAUSE, TYPE_WHERE_CLAUSE
from ro.webdata.nqi.nlp.sentence.utils import get_wh_pronouns, get_wh_words


class Statement:
    def __init__(self, action, cardinality, phrase, conjunction, statements):
        self.action = action
        self.cardinality = cardinality
        self.conjunction = conjunction
        self.phrase = phrase
        self.type = get_stmt_type(phrase, statements)

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        action_indentation = '\t'

        return (
            f'{indentation}statement: {{\n'
            f'{indentation}{Action.get_str(self.action, action_indentation)},\n'
            f'{indentation}\tcardinality: {self.cardinality},\n'
            f'{indentation}\tconjunction: {self.conjunction},\n'
            f'{indentation}\tphrase: {self.phrase},\n'
            f'{indentation}\ttype: {self.type}\n'
            f'{indentation}}}'
        )


def get_stmt_type(chunk, statements):
    if chunk.text.lower() in PRONOUNS:
        return TYPE_PRON
    # "who is the director who own..." => classify only the first chunk
    # which contains the "who" word as being TYPE_WH_PRON_START
    elif chunk.root in get_wh_pronouns(chunk):
        return TYPE_WH_PRON_START if chunk.root.i == 0 else TYPE_WH
    elif chunk.root in get_wh_words(chunk):
        return TYPE_WH_START if chunk.root.i == 0 else TYPE_WH
    # if the type of the first sentence is not TYPE_PRON or TYPE_WH_START,
    # then the target subjects are found in the first sentence
    elif len(statements) == 0:
        return TYPE_SELECT_CLAUSE
    else:
        nouns = get_nouns(chunk)
        conj_nouns = list(filter(lambda noun: noun.dep == "conj", nouns))
        prev_statement = get_last_statement(statements)

        if prev_statement.type in [TYPE_PRON, TYPE_WH_PRON_START, TYPE_WH_START]:
            return TYPE_SELECT_CLAUSE
        elif prev_statement.type == TYPE_SELECT_CLAUSE and len(conj_nouns) > 0:
            return TYPE_SELECT_CLAUSE
        else:
            return TYPE_WHERE_CLAUSE


def get_last_statement(statements):
    if len(statements) > 0:
        return statements[len(statements) - 1]
    return None
