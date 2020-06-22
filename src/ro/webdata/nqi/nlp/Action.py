class Action:
    def __init__(self, dep, verb_stmt):
        self.dep = dep
        self.is_available = True
        self.verb_stmt = verb_stmt

    def __str__(self):
        return self.get_str()
    
    def get_str(self, indentation=''):
        return (
            f'{indentation}action: {{\n'
            f'{indentation}\tdep: {self.dep}\n'
            f'{indentation}\tis_available: {self.is_available}\n'
            f'{indentation}\tverb_stmt: {Verb.get_str(self.verb_stmt)}\n'
            f'{indentation}}}'
        )


class Verb:
    def __init__(self, aux_vb, neg, main_vb, modal_vb, wh_word):
        self.aux_vb = aux_vb
        self.neg = neg
        self.main_vb = main_vb
        self.modal_vb = modal_vb
        self.wh_word = wh_word

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{indentation}{{ '
            f'{indentation}aux_vb: {self.aux_vb}, '
            f'{indentation}neg: {self.neg}, '
            f'{indentation}main_vb: {self.main_vb}, '
            f'{indentation}modal_vb: {self.modal_vb}, '
            f'{indentation}wh_word: {self.wh_word} '
            f'{indentation}}}'
        )
