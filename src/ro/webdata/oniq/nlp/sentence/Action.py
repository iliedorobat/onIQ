from ro.webdata.oniq.nlp.sentence.Noun import get_nouns
from ro.webdata.oniq.nlp.sentence.Verb import Verb, get_verb_statements
from ro.webdata.oniq.nlp.sentence.constants import TYPE_PRON, TYPE_WH, TYPE_WH_PRON_START, TYPE_WH_START

ACTION_EXCEPTIONS = [
    TYPE_PRON,
    TYPE_WH,
    TYPE_WH_PRON_START,
    TYPE_WH_START
]


class Action:
    def __init__(self, dep, verb_stmt):
        self.dep = dep
        self.is_available = True
        self.verb_stmt = verb_stmt

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        dep = self.dep if self else None
        is_available = self.is_available if self else None
        verb_stmt = self.verb_stmt if self else None
        verb_indentation = "\t\t"

        return (
            f'{indentation}action: {{\n'
            f'{indentation}\tdep: {dep},\n'
            f'{indentation}\tis_available: {is_available},\n'
            f'{indentation}\tverb_stmt: {Verb.get_str(verb_stmt, verb_indentation)}\n'
            f'{indentation}}}'
        )


def get_action(sentence, chunks, chunk_index, actions, statements, stmt_type):
    if stmt_type not in ACTION_EXCEPTIONS:
        chunk = chunks[chunk_index]
        conj_nouns = get_nouns(chunk, ["conj"])
        last_action = statements[len(statements) - 1].action if len(statements) > 0 else {}
        prev_word = sentence[chunk.start - 1] if chunk.start > 0 else None

        for action in actions:
            # e.g.: chunk[0].tag_ == "WDT": "which paintings are located in Tulcea"
            if chunk[0].tag_ == "WDT" or \
                    (prev_word is not None and prev_word.tag_ != "IN"):
                if action.is_available is True:
                    action.is_available = False
                    return action
                if len(conj_nouns) > 0:
                    return last_action


def get_actions(sentence):
    actions = []
    verb_statements = get_verb_statements(sentence)

    for verb_stmt in verb_statements:
        dep = verb_stmt.main_vb.dep_ \
            if verb_stmt.main_vb is not None \
            else verb_stmt.aux_vb.dep_
        actions.append(Action(dep, verb_stmt))

    return actions
