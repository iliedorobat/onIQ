from spacy.tokens import Token

from ro.webdata.oniq.common.nlp.word_utils import is_cardinal


class YearTracker:
    def __init__(self, token: Token):
        metadata = get_year_metadata(token)

        self.ante_notation = metadata["ANTE_NOTATION"]
        self.value = metadata["CARDINAL"]

    def exists(self):
        return self.value is not None


def get_year_metadata(token: Token):
    if isinstance(token, Token):
        # E.g.: "Which volcanos in Japan erupted since 2000?"
        rights = [token for token in list(token.rights) if token.pos_ in ["ADV", "ADP", "SCONJ"]]

        if len(rights) > 0:
            prep = rights[0]

            notation = prep.lower_
            prep_rights = [token for token in list(prep.rights) if token.pos_ in ["ADV", "ADP", "SCONJ"]]

            if len(prep_rights) > 0:
                # E.g.: "Which volcanos in Japan erupted up to 2000?"
                # E.g.: "Which volcanos in Japan erupted earlier than 2000?"
                prep = prep_rights[0]
                notation += " " + prep.lower_

            cardinals_rights = [token for token in list(prep.rights) if is_cardinal(token)]
            if len(cardinals_rights) > 0:
                return {
                    "ANTE_NOTATION": notation,
                    "CARDINAL": cardinals_rights[0]
                }

    return {
        "ANTE_NOTATION": None,
        "CARDINAL": None
    }
