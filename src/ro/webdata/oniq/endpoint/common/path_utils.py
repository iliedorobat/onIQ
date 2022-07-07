import os
from pathlib import Path


def get_dbpedia_file_path(filename, extension, mid_path=""):
    """
    Retrieve the full path of the file.

    Args:
        filename (str):
            Name of the file (E.g.: "class_list").
        extension (str):
            Name of the file extension (E.g.: "csv").
        mid_path (str):
            Path between DBpedia directory and the file.
            E.g.: get_dbpedia_file_path(filename, "csv", "categories/").

    Returns:
         str: Full path of the file.
    """

    path = get_root_path() + "/files/dbpedia/" + mid_path

    if not os.path.exists(path):
        os.makedirs(path)

    return path + filename + "." + extension


def get_input_file_path(filename, extension):
    """
    Retrieve the full input path of the file.

    Args:
        filename (str):
            Name of the file (E.g.: "test").
        extension (str):
            Name of the file extension (E.g.: "rdf").

    Returns:
         str: Full input path of the file.
    """

    return get_root_path() + "/files/input/" + filename + "." + extension


def get_output_file_path(filename, extension):
    """
    Retrieve the full output path of the file.

    Args:
        filename (str):
            Name of the file (E.g.: "test").
        extension (str):
            Name of the file extension (E.g.: "rdf").

    Returns:
         str: Full output path of the file.
    """

    return get_root_path() + "/files/output/" + filename + "." + extension


def get_root_path():
    """
    Retrieve the root path of the project.

    Returns:
         str: Root path of the project.
    """

    full_path = str(Path(__file__).parent.resolve())
    index = full_path.index("/src/ro/webdata")

    return full_path[0: index]


_CATEGORIES_PATH = get_root_path() + "/files/dbpedia/categories/"
_CATEGORIES_FILENAME_PREFIX = "category_list_"


def get_categories_filenames():
    """
    Read the category file names and return a sorted list of them.

    Returns:
        List[str]: Sorted list of category file names.
    """

    if not os.path.exists(_CATEGORIES_PATH):
        os.makedirs(_CATEGORIES_PATH)

    return sorted([
        filename.replace(".csv", "")
        for filename in os.listdir(_CATEGORIES_PATH)
        if filename.__contains__(_CATEGORIES_FILENAME_PREFIX)
    ], key=lambda filename: filename_to_number(filename))


def filename_to_number(filename):
    """
    If the file name ends with a number, extract it and convert
    it to an integer. Otherwise, throw an error.

    Args:
        filename (str):
            Name of the file.

    Returns:
         int: The integer at the end of the file name.

    Raises:
        ValueError: If the file name does not end with a number or
            the number cannot be converted to an integer.
    """

    try:
        return int(filename.replace(_CATEGORIES_FILENAME_PREFIX, "").replace(".csv", ""))
    except ValueError:
        return None
