import os

import nltk
import spacy

from progress.bar import Bar
from ro.webdata.oniq.common.print_utils import console
from ro.webdata.oniq.endpoint.common.path_const import PATTERNS_PATH
from ro.webdata.oniq.endpoint.common.path_utils import get_root_path
from ro.webdata.oniq.endpoint.common.translator.EntityTranslator import EntityTranslator
from ro.webdata.oniq.endpoint.dbpedia.constants import DBPEDIA_CLASS_TYPES
from ro.webdata.oniq.endpoint.dbpedia.setup import DBpediaSetup


class Initializer:
    @staticmethod
    def init():
        Initializer.init_spacy()
        Initializer.init_nltk()
        Initializer.install_deps()
        Initializer.init_dbpedia()
        Initializer.init_patterns()

    @staticmethod
    def init_spacy():
        """
        Install <b>spacy</b>, its dependencies and download models.
        """

        os.system("pip install -U pip setuptools wheel")
        os.system("pip install -U spacy")
        # TODO: to read: https://towardsdatascience.com/named-entity-recognition-with-spacy-and-the-mighty-roberta-97d879f981#c19e
        os.system("pip install spacy-transformers")
        os.system("pip install spacy-wordnet")
        os.system("python -m spacy download en_core_web_sm")
        os.system("python -m spacy download en_core_web_md")
        os.system("python -m spacy download en_core_web_trf")

    @staticmethod
    def init_nltk():
        """
        Install <b>NLTK</b> and download models.
        """

        os.system("pip install --user -U nltk")
        nltk.download('wordnet')
        nltk.download('punkt')

    @staticmethod
    def install_deps():
        """
        Install dependencies.
        """

        os.system("pip install --user -U numpy")
        os.system("pip install parse")
        os.system("pip install langdetect")
        os.system("pip install SPARQLWrapper")
        os.system("pip install iteration-utilities")
        os.system("pip install progress")
        os.system("pip install pydash")
        os.system("pip install sphinx")

    @staticmethod
    def init_dbpedia():
        """
        Save DBpedia classes, properties, categories and entities to disk.
        """

        DBpediaSetup.init_classes()
        DBpediaSetup.init_main_classes()
        DBpediaSetup.init_properties()
        DBpediaSetup.init_categories()

        # FIXME:
        # TODO: POLITICAL_PARTY is subclass of Organisation
        DBpediaSetup.init_entities(DBPEDIA_CLASS_TYPES.PERSON)
        DBpediaSetup.init_entities(DBPEDIA_CLASS_TYPES.ARCHITECTURAL_STRUCTURE)

        accessors = [
            accessor for accessor in dir(DBPEDIA_CLASS_TYPES)
            if not accessor.startswith('__') and accessor not in [
                DBPEDIA_CLASS_TYPES.ARCHITECTURAL_STRUCTURE,
                DBPEDIA_CLASS_TYPES.PERSON
            ]
        ]
        for accessor in accessors:
            entity_type = getattr(DBPEDIA_CLASS_TYPES, accessor)
            DBpediaSetup.init_entities(entity_type)

        EntityTranslator.csv_files_to_json()

    @staticmethod
    def init_patterns():
        """
        Initialize spacy patterns based on the saved entities.
        """

        console.info("Initializing of entities patterns started...")
        _add_ruler_patterns("FAC", DBPEDIA_CLASS_TYPES.ARCHITECTURAL_STRUCTURE)
        _add_ruler_patterns("PERSON", DBPEDIA_CLASS_TYPES.PERSON)
        console.info("All patterns have been written to disk!")


def _add_ruler_patterns(label, entity_type):
    console.info(f'Initializing of {entity_type} patterns started...')

    nlp_model = spacy.load('en_core_web_md')
    ruler_config = {"overwrite_ents": True}
    ruler = nlp_model.add_pipe("entity_ruler", config=ruler_config)

    entity_data = EntityTranslator.read_entity_data(entity_type)
    path = get_root_path() + PATTERNS_PATH

    max_len = len(entity_data["labels"]) + len(entity_data["names"])
    bar = Bar(f'Initializing {entity_type} patterns', max=max_len)

    for key, patterns in entity_data.items():
        ruler.add_patterns([
            {"label": label, "pattern": pattern}
            for pattern in patterns
        ])
        bar.next()

    bar.finish()

    if not os.path.exists(path):
        os.makedirs(path)

    # serialization
    ruler.to_disk(f'{path}{entity_type}.jsonl')
    console.info(f'{entity_type} patterns have been written to disk!')


Initializer.init()
