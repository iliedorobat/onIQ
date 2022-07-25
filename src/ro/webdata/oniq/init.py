import os

import nltk

from ro.webdata.oniq.endpoint.dbpedia.setup import DBpediaSetup
from ro.webdata.oniq.endpoint.dbpedia.setup import ENTITY_TYPES


# install spacy & download models
def _init_spacy():
    os.system("pip install -U pip setuptools wheel")
    os.system("pip install -U spacy")
    os.system("pip install spacy-transformers")
    os.system("python -m spacy download en_core_web_sm")
    os.system("python -m spacy download en_core_web_md")
    os.system("python -m spacy download en_core_web_trf")
    os.system("pip install spacy-wordnet")


# install NLTK & download models
def _init_nltk():
    os.system("pip install --user -U nltk")
    os.system("pip install --user -U numpy")
    nltk.download('wordnet')


# install dependencies
def _install_deps():
    os.system("pip install langdetect")
    os.system("pip install SPARQLWrapper")
    os.system("pip install iteration-utilities")
    os.system("pip install progress")
    os.system("pip install pydash")
    os.system("pip install sphinx")


# cache DBpedia on local files
def _init_dbpedia():
    DBpediaSetup.init_classes()
    DBpediaSetup.init_main_classes()
    DBpediaSetup.init_properties()
    DBpediaSetup.init_categories()

    for entity_type in [a for a in dir(ENTITY_TYPES) if not a.startswith('__')]:
        DBpediaSetup.init_entities(entity_type)


_init_spacy()
_init_nltk()
_install_deps()
_init_dbpedia()
