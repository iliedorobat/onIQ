import spacy

from ro.webdata.oniq.endpoint.common.path_const import PATTERNS_PATH
from ro.webdata.oniq.endpoint.common.path_utils import get_root_path

# nlp_model = spacy.load('en_core_web_sm')
nlp_model = spacy.load('en_core_web_md')
# nlp_model = spacy.load('en_core_web_lg')

# TODO:
# https://spacy.io/universe/project/spacy-wordnet
# nlp_model.add_pipe("spacy_wordnet", after='tagger', config={'lang': nlp_model.lang})

books_path = get_root_path() + PATTERNS_PATH + "Test.jsonl"

# assign named entities based on pattern rules and dictionaries
ruler_config = {"overwrite_ents": True}
ruler = nlp_model.add_pipe("entity_ruler", config=ruler_config)
ruler.from_disk(books_path)

# TODO: after adding nlp.to_disk('my-ruler') in _add_ruler_patterns
# https://github.com/explosion/spaCy/discussions/9776
# ruler = spacy.load('hp_ner')
# nlp.add_pipe("entity_ruler", source=ruler)




nlp_dbpedia = spacy.load('en_core_web_md')
nlp_dbpedia.add_pipe('dbpedia_spotlight', config={'confidence': 0.75})
ruler_config = {"overwrite_ents": True}
ruler = nlp_dbpedia.add_pipe("entity_ruler", config=ruler_config)
ruler.from_disk(books_path)

