from progress.bar import Bar

from ro.webdata.oniq.endpoint.namespace import NAMESPACE
from ro.webdata.oniq.endpoint.common.path_utils import get_categories_filenames
from ro.webdata.oniq.endpoint.common.path_utils import get_dbpedia_file_path
from ro.webdata.oniq.endpoint.common.CSVService import CSVService, CSV_COLUMN_SEPARATOR
from ro.webdata.oniq.endpoint.models.CSVEntry import CSVEntry
from ro.webdata.oniq.endpoint.models.RDFElement import RDFCategory, RDFClass, RDFProperty, ROOT_CLASS_URI, \
    ROOT_PROPERTY_CLASS_URI
from ro.webdata.oniq.endpoint.models.RDFElements import RDFElements


class CSVTranslator:
    """
    Service used for translating categories, classes and properties from
    CSV files to RDFElements data structure.

    Methods:
        to_categories(extract_label, separator=CSV_COLUMN_SEPARATOR):
            Read categories from the disk and keep them in an RDFElements
            data structure.
        to_classes(extract_label, separator=CSV_COLUMN_SEPARATOR):
            Read classes from the disk and keep them in an RDFElements
            data structure.
        to_props(extract_label, separator=CSV_COLUMN_SEPARATOR):
            Read properties from the disk and keep them in an RDFElements
            data structure.
    """

    @staticmethod
    def to_categories(extract_label=True, separator=CSV_COLUMN_SEPARATOR):
        """
        Read categories from **categories.csv** file and convert each line
        to RDFCategory element.

        Args:
            extract_label (bool): Specify if "_extract_resource_label" method
                will be used or not to get the resource's label.
            separator (str): CSV column separator.

        Returns:
            RDFElements[RDFCategory]: List of RDFCategory elements.
        """

        categories = []
        filenames = get_categories_filenames()
        bar = Bar("Reading categories from DBpedia files", max=len(filenames))

        for filename in filenames:
            filepath = get_dbpedia_file_path(filename, "csv", "categories/")
            categories += CSVBasicTranslator.csv_file_to_categories(filepath, extract_label, separator)
            bar.next()

        bar.finish()

        return RDFElements(categories)

    @staticmethod
    def to_classes(extract_label=False, separator=CSV_COLUMN_SEPARATOR):
        """
        Read classes from **class_list.csv** file, exclude custom properties,
        convert each line to RDFClass element and update the list of the class's
        parents with parents of the parent.

        Args:
            extract_label (bool): Specify if "_extract_resource_label" method
                will be used or not to get the resource's label.
            separator (str): CSV column separator.

        Returns:
            RDFElements[RDFClass]: List of RDFClass elements.
        """

        filepath = get_dbpedia_file_path("class_list", "csv")
        classes = CSVBasicTranslator.csv_file_to_classes(filepath, extract_label, separator)

        return RDFElements([
            rdf_class for rdf_class in classes
            # exclude custom properties
            if ROOT_PROPERTY_CLASS_URI not in rdf_class.parent_uris
        ])

    @staticmethod
    def to_props(extract_label=False, separator=CSV_COLUMN_SEPARATOR):
        """
        Read properties from **prop_list.csv** file and convert each line to
        RDFProperty element.
        Read classes from **class_list.csv** file, filter by custom properties,
        convert each line to RDFProperty element and update the list of the
        propriety's parents with the parent of the parent.

        Args:
            extract_label (bool): Specify if "_extract_resource_label" method
                will be used or not to get the resource's label.
            separator (str): CSV column separator.

        Returns:
            RDFElements[RDFProperty]: List of RDFProperty elements.
        """

        classes_filepath = get_dbpedia_file_path("class_list", "csv")
        props_filepath = get_dbpedia_file_path("prop_list", "csv")

        custom_props = CSVBasicTranslator.csv_file_to_custom_props(classes_filepath, extract_label, separator)
        init_props = CSVBasicTranslator.csv_file_to_props(props_filepath, extract_label, separator)
        props = init_props + custom_props

        return RDFElements(props)


class CSVBasicTranslator:
    """
    Service used for reading categories, classes and properties from the
    disk and keeping them in an RDFElements data structure.

    Methods:
        csv_file_to_categories(filepath, extract_label, separator):
            Read categories from the disk and keep them in an RDFElements
            data structure.
        csv_file_to_classes(filepath, extract_label, separator):
            Read classes from the disk and keep them in an RDFElements
            data structure.
        csv_file_to_props(filepath, extract_label, separator):
            Read properties from the disk and keep them in an RDFElements
            data structure.
        csv_file_to_custom_props(filepath, extract_label, separator):
            Read classes from the disk, filter by custom properties and
            keep them in an RDFElements data structure.
    """

    @staticmethod
    def csv_file_to_categories(filepath, extract_label=False, separator=CSV_COLUMN_SEPARATOR):
        """
        Read categories from the provided filepath and convert each line to
        RDFCategory element.

        Args:
            filepath (str): Full path of the target file.
            extract_label (bool): Specify if "_extract_resource_label" method
                will be used or not to get the resource's label.
            separator (str): CSV column separator.

        Returns:
            RDFElements[RDFCategory]: List of RDFCategory elements.
        """

        return _csv_file_to_basic_categories(filepath, extract_label, separator)

    @staticmethod
    def csv_file_to_classes(filepath, extract_label=False, separator=CSV_COLUMN_SEPARATOR):
        """
        Read classes from the provided filepath, convert each line to RDFClass
        element and update the list of the class's parents with parents of the
        parent.

        Args:
            filepath (str): Full path of the target file.
            extract_label (bool): Specify if "_extract_resource_label" method
                will be used or not to get the resource's label.
            separator (str): CSV column separator.

        Returns:
            List[RDFClass]: List of RDFClass elements.
        """

        classes = _csv_file_to_basic_classes(filepath, extract_label, separator)
        basic_classes = _csv_file_to_basic_classes(filepath, extract_label, separator)
        basic_props_filepath = get_dbpedia_file_path("prop_list", "csv")
        basic_props = _csv_file_to_basic_props(basic_props_filepath)

        for rdf_class in classes.elements:
            _update_parent_class_uris(basic_classes, basic_props, rdf_class)

        return classes

    @staticmethod
    def csv_file_to_props(filepath, extract_label=False, separator=CSV_COLUMN_SEPARATOR):
        """
        Read properties from the provided filepath, convert each line to
        RDFProperty and update the list of the property's parents with
        parents of the parent.

        Args:
            filepath (str): Full path of the target file.
            extract_label (bool): Specify if "_extract_resource_label" method
                will be used or not to get the resource's label.
            separator (str): CSV column separator.

        Returns:
            List[RDFProperty]: List of RDFProperty elements.
        """

        return _csv_file_to_basic_props(filepath, extract_label, separator).elements

    @staticmethod
    def csv_file_to_custom_props(classes_filepath, extract_label=False, separator=CSV_COLUMN_SEPARATOR):
        """
        Read classes from the provided filepath, filter by custom properties,
        convert each line to RDFProperty element and update the list of the
        propriety's parents with parent of the parent.

        Args:
            classes_filepath (str): Full path of the target classes file.
            extract_label (bool): Specify if "_extract_resource_label" method
                will be used or not to get the resource's label.
            separator (str): CSV column separator.

        Returns:
            List[RDFProperty]: List of RDFProperty elements.
        """

        classes = CSVBasicTranslator.csv_file_to_classes(classes_filepath, extract_label, separator)

        return [
            RDFProperty(rdf_class.uri, rdf_class.parent_uris, rdf_class.label, rdf_class.ns, rdf_class.ns_label)
            for rdf_class in classes
            # filter for custom properties
            if ROOT_PROPERTY_CLASS_URI in rdf_class.parent_uris
        ]


def _csv_file_to_basic_categories(filepath, extract_label=False, separator=CSV_COLUMN_SEPARATOR):
    """
    Read categories from the provided filepath and convert each line to
    RDFCategory element.

    Args:
        filepath (str): Full path of the target file.
        extract_label (bool): Specify if "_extract_resource_label" method
            will be used or not to get the resource's label.
        separator (str): CSV column separator.

    Returns:
        RDFElements[RDFCategory]: List of RDFCategory elements.
    """

    categories = []

    for line in CSVService.read_lines(filepath, True):
        csv_entry = CSVEntry(line, extract_label, separator)
        categories.append(
            RDFCategory(
                csv_entry.resource_uri,
                csv_entry.parent_uris,
                csv_entry.resource_label,
                csv_entry.namespace,
                csv_entry.namespace_label
            )
        )

    return RDFElements(categories)


def _csv_file_to_basic_classes(filepath, extract_label=False, separator=CSV_COLUMN_SEPARATOR):
    """
    Read classes from the provided filepath and convert each line to
    RDFClass.

    Args:
        filepath (str): Full path of the target file.
        extract_label (bool): Specify if "_extract_resource_label" method
            will be used or not to get the resource's label.
        separator (str): CSV column separator.

    Returns:
        RDFElements[RDFClass]: List of RDFClass elements.
    """

    classes = []

    for line in CSVService.read_lines(filepath, True):
        csv_entry = CSVEntry(line, extract_label, separator)
        classes.append(
            RDFClass(
                csv_entry.resource_uri,
                csv_entry.parent_uris,
                csv_entry.resource_label,
                csv_entry.namespace,
                csv_entry.namespace_label
            )
        )

    return RDFElements(classes)


def _csv_file_to_basic_props(filepath, extract_label=False, separator=CSV_COLUMN_SEPARATOR):
    """
    Read properties from the provided filepath and convert each line to
    RDFProperty element.

    Args:
        filepath (str): Full path of the target file.
        extract_label (bool): Specify if "_extract_resource_label" method
            will be used or not to get the resource's label.
        separator (str): CSV column separator.

    Returns:
        RDFElements[RDFProperty]: List of RDFProperty elements.
    """

    props = []

    for line in CSVService.read_lines(filepath, True):
        csv_entry = CSVEntry(line, extract_label, separator)
        props.append(
            RDFProperty(
                csv_entry.resource_uri,
                csv_entry.parent_uris,
                csv_entry.resource_label,
                csv_entry.namespace,
                csv_entry.namespace_label,
                csv_entry.res_domain,
                csv_entry.res_range
            )
        )

    return RDFElements(props)


def _update_parent_class_uris(basic_classes, basic_props, rdf_class):
    """
    Complete the list of the class's parents with parents of the parent.

    Example:
        1. classes:
            - "http://dbpedia.org/ontology/File"
                => initial parent: "http://dbpedia.org/ontology/Document".
                => parents of the parent:
                [
                    "http://dbpedia.org/ontology/Document",
                    "http://dbpedia.org/ontology/Work",
                    "http://www.w3.org/2002/07/owl#Thing"
                ].
            - "http://dbpedia.org/ontology/Document"
                => initial parent: "http://dbpedia.org/ontology/Work"
                => parents of the parent:
                [
                    "http://dbpedia.org/ontology/Work",
                    "http://www.w3.org/2002/07/owl#Thing"
                ]
            - "http://dbpedia.org/ontology/Work"
                => initial parent: "http://www.w3.org/2002/07/owl#Thing"
                => parents of the parent:
                [
                    "http://www.w3.org/2002/07/owl#Thing"
                ]
        2. properties:
            - "http://dbpedia.org/ontology/Anime"
                  => initial parent: "http://dbpedia.org/ontology/Cartoon"
                  => parents of the parent:
                  [
                      "http://dbpedia.org/ontology/work",
                      "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
                   ]

    Args:
        basic_classes (RDFElements[RDFClass]): List of basic classes retrieved
            through the means of the <b>_csv_file_to_basic_classes</b> method.
        basic_props (RDFElements[RDFProperty]): List of basic properties retrieved
            through the means of the <b>_csv_file_to_basic_props</b> method.
        rdf_class (RDFClass): Target class.
    """

    if rdf_class is not None and len(rdf_class.parent_uris) > 0:
        for parent_uri in rdf_class.parent_uris:
            parent_class = basic_classes.find(parent_uri)

            # E.g.: "http://dbpedia.org/ontology/Anime"
            if parent_class is None:
                parent_class = basic_props.find(parent_uri)

            if parent_class is not None and parent_uri != ROOT_CLASS_URI and NAMESPACE.DBP_ONTOLOGY in parent_uri:
                for parent_parent_uri in parent_class.parent_uris:
                    rdf_class.parent_uris.append(parent_parent_uri)

                    if parent_parent_uri != ROOT_CLASS_URI:
                        parent_parent_class = basic_classes.find(parent_parent_uri)
                        _update_parent_class_uris(basic_classes, basic_props, parent_parent_class)
                    else:
                        return
