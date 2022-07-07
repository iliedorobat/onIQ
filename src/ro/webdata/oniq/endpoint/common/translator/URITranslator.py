from typing import List

from ro.webdata.oniq.endpoint.common.translator.CSVTranslator import CSVTranslator
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements


class URITranslator:
    """
    Service used for translating URIs to classes and properties.

    Attributes:
        classes (RDFElements[RDFClass]):
            List of RDFClass elements.
        properties (RDFElements[RDFProperty]):
            List of RDFProperty elements.

    Methods:
        to_classes(uris):
            Get the list of RDFClass elements that match the list or URIs.
        to_class(uri):
            Get the RDFClass element that match the target URI.
        to_properties(uris)
            Get the list of RDFProperty elements that match the list or URIs.
        to_property(uri):
            Get the RDFProperty element that match the target URI.
    """

    classes: RDFElements = None
    properties: RDFElements = None

    def to_classes(self, uris):
        """
        Retrieve the list of RDFClass elements whose value of "uri"
        attribute exists in **class_list.csv** file.

        Args:
            uris (List[str]): The target list of URIs.

        Returns:
            RDFElements[RDFClass]: List of RDFClass elements.
        """

        if self.classes is None:
            self.classes = CSVTranslator.to_classes()

        return RDFElements([
            item for item in self.classes.elements
            if item.uri in uris
        ])

    def to_class(self, uri):
        """
        Retrieve the RDFClass elements whose value of "uri" attribute
        exists in **class_list.csv** file.

        Args:
            uri (str): The target URI.

        Returns:
            RDFClass: RDF class.
        """

        classes = self.to_classes([uri]).elements

        if len(classes) == 1:
            return classes[0]

        return None

    def to_properties(self, uris):
        """
        Retrieve the list of RDFProperty elements whose value of "uri"
        attribute exists in **prop_list.csv** file or in **class_list.csv**
        file (custom properties).

        Args:
            uris (List[str]): The input list of URIs.

        Returns:
            RDFElements[RDFProperty]: List of RDFProperty elements.
        """

        if self.properties is None:
            self.properties = CSVTranslator.to_props()

        return RDFElements([
            item for item in self.properties.elements
            if item.uri in uris
        ])

    def to_property(self, uri):
        """
        Retrieve the RDFProperty element whose value of "uri" attribute
        exists in **prop_list.csv** file or in **class_list.csv** file
        (custom properties).

        Args:
            uri (str): The target URI.

        Returns:
            RDFProperty: RDF property.
        """

        props = self.to_properties([uri]).elements

        if len(props) == 1:
            return props[0]

        return None
