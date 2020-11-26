from ro.webdata.oniq.model.sentence.Verb import Verb


class Action:
    def __init__(self, verb: Verb):
        self.dep = _get_dep(verb)
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


def _get_dep(verb):
    if verb.main_vb is not None:
        return verb.main_vb.dep_
    elif verb.aux_vb is not None:
        last_index = len(verb.aux_vb) - 1
        return verb.aux_vb[last_index].dep_
