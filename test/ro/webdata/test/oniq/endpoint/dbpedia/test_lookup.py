import spacy

from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.model.sentence.Statement import Statement
from ro.webdata.oniq.nlp.nlp_utils import is_wh_noun_chunk
from ro.webdata.oniq.nlp.stmt_utils import get_statement_list

nlp = spacy.load('en_core_web_sm')
# nlp = spacy.load('en_core_web_md')


class TestLookupService:
    @staticmethod
    def run():
        TestLookupService.test_entities_lookup()
        TestLookupService.test_noun_chunk_lookup()
        TestLookupService.test_property_lookup()

    @staticmethod
    def test_entities_lookup():
        question = "What did James Cagney win in the 15th Academy Awards?"
        document = nlp(question)
        statements = get_statement_list(document)

        for stmt in statements:
            ents = _get_named_entities(stmt)
            # ents[0] == James Cagney
            entries = LookupService.entities_lookup(ents[0])

            print("test_entities_lookup():")
            for entry in entries:
                print(f'\t{entry}')

    @staticmethod
    def test_noun_chunk_lookup():
        question = "When was barda mausoleum built?"
        document = nlp(question)
        statements = get_statement_list(document)

        for stmt in statements:
            noun_chunks = _get_noun_chunks(stmt)

            for noun_chunk in noun_chunks:
                root = noun_chunk.root
                # if root.pos_ == "PROPN" and noun_chunk.text != root.text:
                #     # e.g. "rizal monument" is compound PROPN
                if noun_chunk.text != root.text:
                    entries = LookupService.noun_chunk_lookup(noun_chunk)
                    print(entries)

    @staticmethod
    def test_property_lookup():
        resource_name = "Barda_Mausoleum"

        # question = "When was barda mausoleum built?"
        question = "Where is barda mausoleum located?"
        document = nlp(question)
        statements = get_statement_list(document)

        verb = statements[0].action.verb.main_vb
        prop = LookupService.property_lookup(resource_name, verb)

        print(
            f'test_property_lookup():\n'
            f'\tresource_name: {resource_name}\n'
            f'\tverbs: {verb.to_list()}\n'
            f'\tprop: {prop}'
        )


def _get_noun_chunks(stmt: Statement):
    noun_chunks = list(stmt.phrase.chunk.noun_chunks) + list(stmt.related_phrase.chunk.noun_chunks)

    return [
        noun_chunk for noun_chunk in noun_chunks
        # exclude wh_noun_chunks
        if not is_wh_noun_chunk(noun_chunk)
    ]


def _get_named_entities(stmt: Statement):
    return list(stmt.phrase.chunk.ents) + list(stmt.related_phrase.chunk.ents)
