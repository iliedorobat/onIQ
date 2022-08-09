import warnings

from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.nlp.stmt_utils import get_statement_list
from ro.webdata.oniq.spacy_model import nlp_model

_QUERY_SKELETON = "{prefixes}" \
                  "SELECT {targets}" \
                  "WHERE {{" \
                  "{where_block}" \
                  "{filter_statement}" \
                  "}}"


class MetaQuery:
    # nl_query: The query provided by the user in natural language

    warnings.warn("deprecated in favour of SPARQLQuery", DeprecationWarning)

    def __init__(self, endpoint, question):
        document = nlp_model(question)
        statements = get_statement_list(document)

        for stmt in statements:
            for ent in stmt.phrase.chunk.ents:
                classes = LookupService.entities_lookup(ent)
                print(classes)

            for ent in stmt.related_phrase.chunk.ents:
                classes = LookupService.entities_lookup(ent)
                print(classes)

            noun_chunks = stmt.related_phrase.chunk.noun_chunks
            for noun_chunk in noun_chunks:
                root = noun_chunk.root
                if root.pos_ == "PROPN" and noun_chunk.text != root.text:
                    # e.g. "rizal monument" is compound PROPN
                    classes = LookupService.noun_chunk_lookup(noun_chunk)
                    print(classes)

        # query = Query(endpoint, statements)
        #
        # TODO: query.get_str method
        # self.query = _QUERY_SKELETON.format(
        #     prefixes=Query.get_prefixes(endpoint),
        #     targets=query.get_targets_str(),
        #     where_block=query.get_where_block(),
        #     filter_statement=query.get_filter_block()
        # )

        # nlp_query = nlp(question)
        # displacy.serve(nlp_query, style="dep", port=7700)
