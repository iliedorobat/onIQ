from typing import List, Union

from ro.webdata.oniq.endpoint.models.RDFElement import RDFCategory, RDFClass, RDFElement, RDFProperty


class RDFElements:
    """
    Representation of the list of RDF elements (RDFElement, RDFCategory,
    RDFClass, RDFProperty).

    Attributes:
        elements (List[Union[RDFElement, RDFCategory, RDFClass, RDFProperty]]):
            List of RDFElement, RDFCategory, RDFClass, RDFProperty items.
    """

    elements: List[Union[RDFElement, RDFCategory, RDFClass, RDFProperty]]

    def __init__(self, elements: List[Union[RDFElement, RDFCategory, RDFClass, RDFProperty]]):
        """
        Args:
            elements (List[Union[RDFElement, RDFCategory, RDFClass, RDFProperty]]):
                Initial list of RDFElement, RDFCategory, RDFClass, RDFProperty items.
        """

        self.elements = elements

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, item):
        return self.elements[item]

    def __str__(self):
        string = ", ".join(
            [str(element) for element in self.elements]
        )

        return f'[{string}]'

    def append(self, element: Union[RDFElement, RDFCategory, RDFClass, RDFProperty]):
        """
        Add a new element to the list of elements.

        Args:
            element (RDFElement, RDFCategory, RDFClass, RDFProperty):
                New element (RDFElement, RDFCategory, RDFClass, RDFProperty).
        """

        self.elements.append(element)

    def unique(self):
        """
        Remove duplicates.
        """

        self.elements = list(set(self.elements))

    def sort(self):
        """
        Sort the elements based on the URI.
        """

        self.elements = sorted(self.elements, key=lambda item: item.uri)

    def exists(self, uri):
        """
        Check if the input URI exists in the input list of elements.

        E.g.:
            * RDFClass:
                - uri = "http://dbpedia.org/ontology/MusicalArtist"
                - parent_uris = [
                    "http://schema.org/MusicGroup",
                    "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#NaturalPerson",
                    "http://dbpedia.org/ontology/Artist"
                ]

        Args:
            uri (str): Target URI.

        Returns:
            bool: Validation result.
        """

        return uri in [rdf_prop.uri for rdf_prop in self.elements]

    def find(self, uri):
        """
        Find the element corresponding to the provided URI.

        Args:
            uri (str): Target URI.

        Returns:
            RDFElement, RDFCategory, RDFClass, RDFProperty:
                The element which contains the input URI.
        """

        if self.exists(uri):
            filtered_props = [
                rdf_prop for rdf_prop in self.elements
                if rdf_prop.uri == uri
            ]

            return filtered_props[0]

        return None
