from ro.webdata.oniq.endpoint.dbpedia.lookup import LookupService
from ro.webdata.oniq.spacy_model import nlp_model


class TestLookupService:
    @staticmethod
    def run():
        TestLookupService.test_entities_lookup()
        TestLookupService.test_noun_chunk_lookup()
        TestLookupService.test_property_lookup()

    @staticmethod
    def test_entities_lookup():
        question = "What did James Cagney win in the 15th Academy Awards?"
        document = nlp_model(question)

        ents = list(document.ents)
        entries = LookupService.entities_lookup(ents[0])  # ents[0] == James Cagney

        print("test_entities_lookup():")
        for entry in entries:
            print(f'\t{entry}')

    @staticmethod
    def test_noun_chunk_lookup():
        question = "When was barda mausoleum built?"
        document = nlp_model(question)

        for noun_chunk in list(document.noun_chunks):
            root = noun_chunk.root
            # if root.pos_ == "PROPN" and noun_chunk.text != root.text:
            #     # e.g. "rizal monument" is compound PROPN
            if noun_chunk.text != root.text:
                entries = LookupService.noun_chunk_lookup(noun_chunk)
                print(entries)

    @staticmethod
    def test_property_lookup():
        # document = nlp_model("When was Barda Mausoleum built?")
        document = nlp_model("Where is Barda Mausoleum located?")

        verb = document[4]
        resource_name = "Barda_Mausoleum"
        prop = LookupService.property_lookup(resource_name, verb, None)

        print(
            f'test_property_lookup():\n'
            f'\tresource_name: {resource_name}\n'
            f'\tprop: {prop}'
        )
