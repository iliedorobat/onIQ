from spacy.tokens import Span
from ro.webdata.oniq.nlp.sentence.Noun import get_nouns
from ro.webdata.oniq.nlp.sentence.Verb import Verb, prepare_verb_list
from ro.webdata.oniq.nlp.sentence.constants import TYPE_PRON, TYPE_WH, TYPE_WH_PRON_START, TYPE_WH_START

ACTION_EXCEPTIONS = [
    TYPE_PRON,
    TYPE_WH,
    TYPE_WH_PRON_START,
    TYPE_WH_START
]


class Action:
    def __init__(self, dep: str, verb: Verb):
        self.dep = dep
        self.is_available = True
        self.verb = verb

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        dep = self.dep if self else None
        is_available = self.is_available if self else None
        verb = self.verb if self else None
        verb_indentation = "\t\t"

        return (
            f'{indentation}action: {{\n'
            f'{indentation}\tdep: {dep},\n'
            f'{indentation}\tis_available: {is_available},\n'
            f'{indentation}\tverb: {Verb.get_str(verb, verb_indentation)}\n'
            f'{indentation}}}'
        )


def get_action(sentence: Span, chunks: [Span], chunk_index: int, action_list: [Action], statements, stmt_type: str): # statements: [Statement]
    if stmt_type not in ACTION_EXCEPTIONS:
        chunk = chunks[chunk_index]
        conj_nouns = get_nouns(chunk, ["conj"])
        last_action = statements[len(statements) - 1].action if len(statements) > 0 else {}
        prev_word = sentence[chunk.start - 1] if chunk.start > 0 else None

        for action in action_list:
            # E.g.: chunk[0].tag_ == "WDT": "which paintings are located in Bacau"
            if chunk[0].tag_ == "WDT" or \
                    (prev_word is not None and prev_word.tag_ != "IN"):
                if action.is_available is True:
                    action.is_available = False
                    return action
                if len(conj_nouns) > 0:
                    return last_action


def prepare_action_list(sentence: Span):
    action_list = []
    verb_list = prepare_verb_list(sentence)

    for verb in verb_list:
        dep = None

        if verb.main_vb is not None:
            dep = verb.main_vb.dep_
        elif verb.aux_vb is not None:
            last_index = len(verb.aux_vb) - 1
            dep = verb.aux_vb[last_index].dep_

        action_list.append(Action(dep, verb))

    return action_list
