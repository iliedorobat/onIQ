import warnings

import spacy

from ro.webdata.oniq.common.text_utils import split_camel_case_string
from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.endpoint.namespace import NamespaceService

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


PROPERTIES_TYPE = {
    "AGE": [],
    "PLACE": [],
    "TIMESPAN": [
        {"ns_name": NAMESPACE.DC, "prop_name": "date"},
        {"ns_name": NAMESPACE.DC_TERMS, "prop_name": "issued"}
    ]
}


class Property:
    warnings.warn("Deprecated in favour or RDFProperty", PendingDeprecationWarning)

    # deprecated in favour of RDFProperty
    lemma = None
    ns_label = None
    ns_name = None
    prop_name = None
    prop_name_extended = None

    def __init__(self, uri):
        ns_name = NamespaceService.get_namespace(uri)
        ns_label = NamespaceService.get_ns_label(ns_name)
        prop_name = _get_prop_name(uri)
        prop_label = split_camel_case_string(prop_name)

        # TODO: check for http://www.w3.org/1999/02/22-rdf-syntax-ns#_1 in the triplestore
        if prop_name not in ["_1", "first", "object", "predicate", "rest", "subject", "value"]:
            self.lemma = _get_lemma(prop_label)
            self.ns_label = ns_label
            self.ns_name = ns_name
            self.prop_name = prop_name
            self.prop_name_extended = ns_label + ":" + prop_name

    def __bool__(self):
        return self.lemma and self.ns_label and self.ns_name and self.prop_name and self.prop_name_extended

    def __eq__(self, other):
        if not isinstance(other, Property):
            return NotImplemented
        return other is not None and \
            self.lemma == other.lemma and \
            self.ns_name == other.ns_name and \
            self.ns_label == other.ns_label and \
            self.prop_name == other.prop_name and \
            self.prop_name_extended == other.prop_name_extended

    def __str__(self):
        return self.get_str()

    def get_str(self, indentation=''):
        return (
            f'{{'
            f'\n{indentation}\tlemma: {self.lemma},'
            f'\n{indentation}\tns_name: {self.ns_name},'
            f'\n{indentation}\tns_label: {self.ns_label},'
            f'\n{indentation}\tprop_name: {self.prop_name},'
            f'\n{indentation}\tprop_name_extended: {self.prop_name_extended},'
            f'\n{indentation}}}'
        )


def _get_lemma(prop_label):
    # e.g.: prop_name = "currentLocation"
    # prop_label = "current location"
    # result = "location" (the adjective is removed)

    document = nlp(prop_label)
    label = next((
        token for token in document
        # TODO: check to see if we need more exceptions
        if token.dep_ in [None, "", "ROOT"] and token.pos_ not in ["ADJ"]),
        None
    )
    return label.lemma_


def _get_prop_name(uri):
    """
    Remove the namespace and return the name of the property
    """

    ns_name = NamespaceService.get_namespace(uri)
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
