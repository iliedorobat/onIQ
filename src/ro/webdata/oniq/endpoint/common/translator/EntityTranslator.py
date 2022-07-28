import json
from typing import List

from progress.bar import Bar

from ro.webdata.oniq.endpoint.common.CSVService import CSVService
from ro.webdata.oniq.endpoint.common.CSVService import CSV_COLUMN_SEPARATOR
from ro.webdata.oniq.endpoint.common.path_const import DBPEDIA_ENTITIES_PATH
from ro.webdata.oniq.endpoint.common.path_const import ENTITIES_PATH
from ro.webdata.oniq.endpoint.common.path_utils import get_filenames, get_dbpedia_file_path, get_root_path
from ro.webdata.oniq.endpoint.dbpedia.constants import DBPEDIA_CLASS_TYPES


class EntityTranslator:
    """
    Service used for translating DBpedia entities to lists of names
    and labels.

    Methods:
        csv_files_to_json():
            Save lists of names and labels of each entity type to disk.
        csv_file_to_json(entity_type, separator=CSV_COLUMN_SEPARATOR):
            Save lists of names and labels of a specific entity type to disk.
        write_list_to_json(path, target_list):
            Save the list to disk.
        read_csv_entity_files(entity_type, separator=CSV_COLUMN_SEPARATOR):
            Read the content of the files of an entity type.
        read_entity_data(entity_type):
            Read the contents of a given entity's name and label lists.
    """

    @staticmethod
    def csv_files_to_json():
        """
        Save lists of names and labels of each entity type to disk.
        """

        accessors = [
            accessor for accessor in dir(DBPEDIA_CLASS_TYPES)
            if not accessor.startswith('__')
        ]

        for accessor in accessors:
            entity_type = getattr(DBPEDIA_CLASS_TYPES, accessor)
            EntityTranslator.csv_file_to_json(entity_type)

    @staticmethod
    def csv_file_to_json(entity_type, separator=CSV_COLUMN_SEPARATOR):
        """
        Save lists of names and labels of a specific entity type to disk.

        Args:
            entity_type (str): Type of entity (E.g.: Organisation, Person, etc.).
            separator (str): CSV column separator.
        """

        entities = EntityTranslator.read_csv_entity_files(entity_type, separator)

        labels_path = get_root_path() + ENTITIES_PATH + entity_type + ".labels.json"
        names_path = get_root_path() + ENTITIES_PATH + entity_type + ".names.json"

        EntityTranslator.write_list_to_json(labels_path, entities["labels"])
        EntityTranslator.write_list_to_json(names_path, entities["names"])

    @staticmethod
    def write_list_to_json(path, target_list):
        """
        Save the list to disk.

        Args:
            path (str): Full path of the target file.
            target_list (List[str]): List of unique names/labels.
        """

        if len(target_list) > 0:
            json_list = json.dumps(target_list)
            file = open(path, "w+")
            file.write(json_list)
            file.close()

    @staticmethod
    def read_csv_entity_files(entity_type, separator=CSV_COLUMN_SEPARATOR):
        """
        Read the content of the files of an entity type (E.g.: "files/dbpedia/entities/Person/Person0.csv", etc.).
        Throw an exception if the file extension does not end with <b>.csv</b>.

        Args:
            entity_type (str): Type of entity (E.g.: Organisation, Person, etc.).
            separator (str): CSV column separator.

        Returns:
            dict: Dictionary containing sorted lists of unique names and labels.
        """

        labels = []
        names = []

        mid_path = entity_type + "/"
        filenames = get_filenames(DBPEDIA_ENTITIES_PATH, entity_type, mid_path)
        bar = Bar("Reading entities from DBpedia files", max=len(filenames))

        for filename in filenames:
            filepath = get_dbpedia_file_path(filename, "csv", f'entities/{entity_type}/')

            for csv_line in CSVService.read_lines(filepath, True):
                csv_entry = csv_line.strip().split(separator)
                labels.append(csv_entry[1])
                names.append(csv_entry[2])

            bar.next()

        bar.finish()

        labels = [label for label in list(set(labels)) if len(label) > 0]
        names = [name for name in list(set(names)) if len(name) > 0]
        labels.sort()
        names.sort()

        return {
            "labels": labels,
            "names": names
        }

    @staticmethod
    def read_entity_data(entity_type):
        """
        Read the contents of a given entity's name and label lists
        (E.g.: "files/entities/Person.labels.json", etc.).

        Args:
            entity_type (str): Type of entity (E.g.: Organisation, Person, etc.).

        Returns:
            dict: Dictionary containing local lists of names and labels.
        """

        labels_path = get_root_path() + ENTITIES_PATH + entity_type + ".labels.json"
        names_path = get_root_path() + ENTITIES_PATH + entity_type + ".names.json"

        labels_file = open(labels_path)
        labels = json.load(labels_file)
        labels_file.close()

        names_file = open(names_path)
        names = json.load(names_file)
        names_file.close()

        return {
            "labels": labels,
            "names": names
        }
