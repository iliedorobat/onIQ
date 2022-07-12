from ro.webdata.oniq.endpoint.common.translator.URITranslator import URITranslator

uri_translator = URITranslator()


class TestURITranslator:
    @staticmethod
    def run():
        TestURITranslator.test_to_classes()
        TestURITranslator.test_to_class()
        TestURITranslator.test_to_properties()
        TestURITranslator.test_to_property()

    @staticmethod
    def test_to_classes():
        rdf_classes = uri_translator.to_classes([
            "http://dbpedia.org/ontology/Document",
            "http://dbpedia.org/ontology/File",
            "http://dbpedia.org/ontology/Work",
            "http://dbpedia.org/ontology/GraveMonument"
        ])

        print(
            f'test_to_classes():\n'
            f'\t{rdf_classes}'
        )

    @staticmethod
    def test_to_class():
        rdf_class = uri_translator.to_class("http://dbpedia.org/ontology/Document")
        print(
            f'test_to_class():\n'
            f'\tDocument: {rdf_class}'
        )

    @staticmethod
    def test_to_properties():
        rdf_props = uri_translator.to_properties([
            "http://dbpedia.org/ontology/address",
            "http://dbpedia.org/ontology/album",
            "http://dbpedia.org/ontology/Anime",
            "http://dbpedia.org/ontology/HollywoodCartoon"
        ])

        print(
            f'test_to_classes():\n'
            f'\t{rdf_props}'
        )

    @staticmethod
    def test_to_property():
        rdf_prop = uri_translator.to_property("http://dbpedia.org/ontology/address")
        print(
            f'test_to_property():\n'
            f'\tAnime: {rdf_prop}'
        )

