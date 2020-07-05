import spacy

from ro.webdata.nqi.common.text_utils import split_camel_case_string
from ro.webdata.nqi.rdf.namespace.Namespace import get_ns_label, get_ns_name

nlp = spacy.load('../../../../lib/en_core_web_sm/en_core_web_sm-2.2.5', disable=['parser', 'ner'])


class Property:
    lemma = None
    ns_label = None
    ns_name = None
    prop_name = None
    prop_name_extended = None

    def __init__(self, uri):
        ns_name = get_ns_name(uri)
        ns_label = get_ns_label(ns_name)
        prop_name = _get_prop_name(uri)
        prop_label = split_camel_case_string(prop_name)

        # TODO: check for http://www.w3.org/1999/02/22-rdf-syntax-ns#_1 in the triple
        if prop_name != "_1":
            self.lemma = _Lemma(prop_label, prop_name)
            self.ns_label = ns_label
            self.ns_name = ns_name
            self.prop_name = prop_name
            self.prop_name_extended = ns_label + ":" + prop_name

    def __bool__(self):
        return self.lemma and self.ns_label and self.ns_name and self.prop_name and self.prop_name_extended

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{{'
            f'\n{indentation}\tlemma.prop_label: {self.lemma.prop_label},'
            f'\n{indentation}\tlemma.prop_name: {self.lemma.prop_name},'
            f'\n{indentation}\tns_name: {self.ns_name},'
            f'\n{indentation}\tns_label: {self.ns_label},'
            f'\n{indentation}\tprop_name: {self.prop_name},'
            f'\n{indentation}\tprop_name_extended: {self.prop_name_extended},'
            f'\n{indentation}}}'
        )


class _Lemma:
    def __init__(self, prop_label, prop_name):
        self.prop_label = _get_prop_label_lemma(prop_label)
        self.prop_name = _get_prop_name_lemma(prop_name)


def _get_prop_label_lemma(prop_label):
    document = nlp(prop_label)
    return " ".join(token.lemma_ for token in document)


def _get_prop_name(uri):
    """
    Remove the namespace and return the name of the property
    """
    ns_name = get_ns_name(uri)
    prop_name = uri[len(ns_name):]

    if prop_name == "basediameter":
        return "baseDiameter"
    elif prop_name == "conjugatediameter":
        return "conjugateDiameter"
    elif prop_name == "handlediameter":
        return "handleDiameter"
    elif prop_name == "maximaldiameter":
        return "maximalDiameter"
    elif prop_name == "mouthdiameter":
        return "mouthDiameter"
    elif prop_name == "sleevewidth":
        return "sleeveWidth"
    elif prop_name == "transversediameter":
        return "transverseDiameter"
    else:
        return prop_name


def _get_prop_name_lemma(prop_name):
    document = nlp(prop_name)
    return document[0].lemma_
