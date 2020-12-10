from spacy.tokens import Token


class Verb:
    """
    A data structure for representing the verbs that are part of an event (Action)

    :attr aux_vb: The list of auxiliary verbs
    :attr neg: TODO move the attribute to the Action
    :attr main_vb: The main verb
    :attr modal_vb: The modal verb
    :attr adjective: TODO move the attribute to the Action
    """

    def __init__(self, aux_vb: [Token], neg: Token, main_vb: Token, modal_vb: Token, adjective: Token):
        self.aux_vb = aux_vb
        self.neg = neg
        self.main_vb = main_vb
        self.modal_vb = modal_vb
        self.adjective = adjective

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        aux_vb = self.aux_vb if self else None
        neg = self.neg if self else None
        main_vb = self.main_vb if self else None
        modal_vb = self.modal_vb if self else None
        adjective = self.adjective if self else None

        return (
            f'{{'
            f'\n{indentation}\taux_vb: {aux_vb},'
            f'\n{indentation}\tadjective: {adjective},'
            f'\n{indentation}\tneg: {neg},'
            f'\n{indentation}\tmain_vb: {main_vb},'
            f'\n{indentation}\tmodal_vb: {modal_vb}'
            f'\n{indentation}}}'
        )

    def get_verb(self):
        """
        Get the main verb if it exists, otherwise the auxiliary verb

        :return: The verb
        """

        if self.main_vb is not None:
            return self.main_vb
        return self.aux_vb
