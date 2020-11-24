from spacy.tokens import Token


class Verb:
    def __init__(self, aux_vb: [Token], neg: Token, main_vb: Token, modal_vb: Token):
        self.aux_vb = aux_vb
        self.neg = neg
        self.main_vb = main_vb
        self.modal_vb = modal_vb

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        aux_vb = self.aux_vb if self else None
        neg = self.neg if self else None
        main_vb = self.main_vb if self else None
        modal_vb = self.modal_vb if self else None

        return (
            f'{{'
            f'\n{indentation}\taux_vb: {aux_vb},'
            f'\n{indentation}\tneg: {neg},'
            f'\n{indentation}\tmain_vb: {main_vb},'
            f'\n{indentation}\tmodal_vb: {modal_vb},'
            f'\n{indentation}}}'
        )

    def get_verb(self):
        if self.main_vb is not None:
            return self.main_vb
        return self.aux_vb
