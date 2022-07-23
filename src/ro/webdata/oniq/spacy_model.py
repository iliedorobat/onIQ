import spacy

# nlp_model = spacy.load('en_core_web_sm')
nlp_model = spacy.load('en_core_web_md')

# TODO:
# https://spacy.io/universe/project/spacy-wordnet
# nlp_model.add_pipe("spacy_wordnet", after='tagger', config={'lang': nlp_model.lang})
