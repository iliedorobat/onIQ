import os
from pathlib import Path


def get_questions_file_path(filename: str, extension: str = "json"):
    return get_root_path() + "/files/questions/" + filename + "." + extension


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
            E.g.:
                - get_dbpedia_file_path(filename, "csv", "categories/");
                - get_dbpedia_file_path(filename, "csv", "entities/").

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


def get_filenames(relative_path, file_prefix):
    """
    Read file names from <b>filepath</b> and return a sorted list of them.

    Args:
        relative_path (List[str]):
            Relative path to the target files.
            E.g.:
                - "/files/dbpedia/categories/";
                - "/files/dbpedia/entities/".
        file_prefix (str):
            String from the beginning of the file which will be removed
            to determine the integer (check <b>filename_to_number</b>).

    Returns:
        List[str]: Sorted list of file names.
    """

    filepath = get_root_path() + relative_path

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    return sorted([
        filename.replace(".csv", "")
        for filename in os.listdir(filepath)
        if filename.__contains__(file_prefix)
    ], key=lambda filename: filename_to_number(filename, file_prefix))


def filename_to_number(filename, prefix):
    """
    If the file name ends with a number, extract it and convert
    it to an integer. Otherwise, throw an error.

    Args:
        filename (str): Name of the file.
        prefix (str): String from the beginning of the file which will
            be removed to determine the integer.

    Returns:
         int: The integer at the end of the file name.

    Raises:
        ValueError: If the file name does not end with a number or
            the number cannot be converted to an integer.
    """

    try:
        return int(filename.replace(prefix, "").replace(".csv", ""))
    except ValueError:
        return None
