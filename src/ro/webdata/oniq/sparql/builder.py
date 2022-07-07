import spacy

from ro.webdata.oniq.nlp.stmt_utils import get_statement_list

nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')


class SPARQLBuilder:
    def __init__(self, endpoint, question):
        """
        :param endpoint: API to the remote computing device
        :param question: Query provided by the user in natural language
                            (e.g.: "when was barda mausoleum built?")
        """
        # TODO: nlp("document", disable=["parser"])
        document = nlp(question)
        statements = get_statement_list(document)

        # TODO: SPARQLQuery: build the SPARQL query
