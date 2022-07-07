from typing import List

import spacy

from ro.webdata.oniq.common.text_utils import WORD_SEPARATOR
from ro.webdata.oniq.common.text_utils import split_camel_case_string
from ro.webdata.oniq.endpoint.common.CSVService import CSV_COLUMN_SEPARATOR, CSV_VALUE_SEPARATOR
from ro.webdata.oniq.endpoint.namespace import NAMESPACE_SEPARATOR
from ro.webdata.oniq.endpoint.namespace import NamespaceService

ROOT_CLASS_URI = "http://www.w3.org/2002/07/owl#Thing"
ROOT_PROPERTY_CLASS_URI = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


class RDFElement:
    """
    Representation of an RDF element (category, class, property).

    Attributes:
        label (str):
            Label of the resource.
        lemma (str):
            Lemma of the name of the resource.
        name (str):
            Name of the resource.
        ns (str):
            Namespace of the resource.
        ns_label (str):
            Label of the namespace of the resource.
        parent_uris (List[str]):
            List of parent resource URIs.
        uri (str):
            Resource URI.
    """

    def __init__(self, uri, parent_uris, label, namespace=None, ns_label=None):
        """
        Args:
            uri (str):
                Resource URI.
            parent_uris (List[str]):
                List of parent resource URIs.
            label (str):
                Label of the resource.
            namespace (str):
                Namespace of the resource.
            ns_label (str):
                Label of the namespace of the resource.
        """

        ns = namespace if namespace is not None else NamespaceService.get_namespace(uri)
        name = uri.replace(ns, "")

        self.label = _prepare_label(name, label)
        self.lemma = WORD_SEPARATOR.join([
            token.lemma_ for token in self.label_to_tokens()
        ])
        self.name = name
        self.ns = ns
        self.ns_label = ns_label if ns_label is not None else NamespaceService.get_ns_label(ns)
        self.parent_uris = parent_uris
        self.uri = uri

    def __hash__(self):
        return hash(self.uri)

    def __eq__(self, other):
        # only equality tests to other 'RDFElement' instances are supported
        if not isinstance(other, RDFElement):
            return NotImplemented
        return self.uri == other.uri

    def __str__(self):
        return self.to_str()

    def to_csv(self, separator: str = CSV_COLUMN_SEPARATOR):
        values = [self.ns_label, self.label, self.ns, self.uri, CSV_VALUE_SEPARATOR.join(self.parent_uris)]
        return separator.join(values)

    def to_str(self):
        return self.ns_label + NAMESPACE_SEPARATOR + self.name

    def label_to_tokens(self):
        """
        Split the label into tokens.

        Returns:
             List[Token]: List of tokens.
        """

        document = nlp(self.label)

        return [
            token for token in document
            if not token.is_punct  # E.g.: "acceleration (s)"
               and len(token) > 1  # E.g.: "acceleration (s)"
            # TODO: check if are necessary
            # and token.dep_ in [None, "", "ROOT"]
            # and token.pos_ not in ["ADJ"] # E.g.: "current place"
        ]

    def label_to_non_stop_tokens(self):
        """
        Split the label into tokens but ignores stop words.

        Returns:
             List[Token]: List of tokens.
        """

        tokens = self.label_to_tokens()
        return [token for token in tokens if not token.is_stop]


class RDFCategory(RDFElement):
    """
    Representation of an RDF category.

    Attributes:
        label (str):
            Label of the resource.
        lemma (str):
            Lemma of the name of the resource.
        name (str):
            Name of the resource.
        ns (str):
            Namespace of the resource.
        ns_label (str):
            Label of the namespace of the resource.
        parent_uris (List[str]):
            List of parent resource URIs.
        uri (str):
            Resource URI.
    """

    def __init__(self, uri, parent_uris, label, namespace=None, ns_label=None):
        """
        Args:
            uri (str):
                Resource URI.
            parent_uris (List[str]):
                List of parent resource URIs.
            label (str):
                Label of the resource.
            namespace (str):
                Namespace of the resource.
            ns_label (str):
                Label of the namespace of the resource.
        """

        super().__init__(uri, parent_uris, label, namespace, ns_label)

    def __eq__(self, other):
        # only equality tests to other 'RDFCategory' instances are supported
        if not isinstance(other, RDFCategory):
            return NotImplemented
        return self.uri == other.uri

    def __hash__(self):
        return hash(self.uri)


class RDFClass(RDFElement):
    """
    Representation of an RDF class.

    Attributes:
        label (str):
            Label of the resource.
        lemma (str):
            Lemma of the name of the resource.
        name (str):
            Name of the resource.
        ns (str):
            Namespace of the resource.
        ns_label (str):
            Label of the namespace of the resource.
        parent_uris (List[str]):
            List of parent resource URIs.
        uri (str):
            Resource URI.
    """

    def __init__(self, uri, parent_uris, label, namespace=None, ns_label=None):
        """
        Args:
            uri (str):
                Resource URI.
            parent_uris (List[str]):
                List of parent resource URIs.
            label (str):
                Label of the resource.
            namespace (str):
                Namespace of the resource.
            ns_label (str):
                Label of the namespace of the resource.
        """

        super().__init__(uri, parent_uris, label, namespace, ns_label)

    def __eq__(self, other):
        # only equality tests to other 'RDFClass' instances are supported
        if not isinstance(other, RDFClass):
            return NotImplemented
        return self.uri == other.uri

    def __hash__(self):
        return hash(self.uri)


class RDFProperty(RDFElement):
    """
    Representation of an RDF property.

    Attributes:
        label (str):
            Label of the resource.
        lemma (str):
            Lemma of the name of the resource.
        name (str):
            Name of the resource.
        ns (str):
            Namespace of the resource.
        ns_label (str):
            Label of the namespace of the resource.
        parent_uris (List[str]):
            List of parent resource URIs.
        uri (str):
            Resource URI.
    """

    def __init__(self, uri, parent_uris, label, namespace=None, ns_label=None):
        """
        Args:
            uri (str):
                Resource URI.
            parent_uris (List[str]):
                List of parent resource URIs.
            label (str):
                Label of the resource.
            namespace (str):
                Namespace of the resource.
            ns_label (str):
                Label of the namespace of the resource.
        """

        super().__init__(uri, parent_uris, label, namespace, ns_label)

    def __eq__(self, other):
        # only equality tests to other 'RDFProperty' instances are supported
        if not isinstance(other, RDFProperty):
            return NotImplemented
        return self.uri == other.uri

    def __hash__(self):
        return hash(self.uri)


def _prepare_label(name, label):
    """
    Retrieve the resource label if it already exists otherwise,
    extract if from the resource name.

    Args:
        name (str):
            Name of the resource.
        label (str):
            Label of the resource (if exists).

    Returns:
        str: Label of the resource.
    """

    if label is None:
        return split_camel_case_string(name)

    # E.g.: RDF Property: "agglomerationPopulationYear", "announcedFrom", etc.
    if label == name:
        return split_camel_case_string(name)

    return label
