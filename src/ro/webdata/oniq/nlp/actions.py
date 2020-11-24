from spacy.tokens import Span

from ro.webdata.oniq.common.constants import SENTENCE_TYPE
from ro.webdata.oniq.model.sentence.Action import Action
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.nlp.nouns import get_nouns
from ro.webdata.oniq.nlp.verbs import prepare_verb_list

ACTION_EXCEPTIONS = [
    SENTENCE_TYPE.PRON,
    SENTENCE_TYPE.WH,
    SENTENCE_TYPE.WH_PRON_START,
    SENTENCE_TYPE.WH_START
]


def get_action(sentence: Span, chunks: [Span], chunk_index: int, action_list: [Action], statements: [Statement], stmt_type: str):
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
