import os

CSV_COLUMN_SEPARATOR = "|"
CSV_VALUE_SEPARATOR = " && "


class CSVService:
    """
    Service used for common operations on CSV files.

    Methods:
        append_line(path, filename, csv_line, header, separator=CSV_COLUMN_SEPARATOR):
            Add a line to the target CSV file.
        read_lines(filepath, exclude_header=True):
            Read the content of a CSV file.
        get_string(value):
            Prepare the value read from a CSV file.
    """

    @staticmethod
    def append_line(path, filename, csv_line, header, separator=CSV_COLUMN_SEPARATOR):
        """
        Add a line to the target CSV file. Throw an exception if the
        file extension does not end with <b>.csv</b>.

        Args:
            path (str): Path of the target CSV file.
            filename (str): Name of the file (E.g.: "best_matched").
            csv_line (str): CSV line that will be written to disk.
            header (List[str]): List of column names.
            separator (str): CSV column separator.

        Raises:
            SyntaxError: If <b>filepath</b> does not end with <b>.csv</b>.
        """

        filepath = path + "/" + filename + ".csv"

        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.isfile(filepath):
            file = open(filepath, "w+")
            file.write(separator.join(header) + "\n")
            file.close()

        file = open(filepath, "a+")
        file.write(csv_line + "\n")
        file.close()

    @staticmethod
    def read_lines(filepath, exclude_header=True):
        """
        Read the content of the target CSV file. Throw an exception if
        the file extension does not end with <b>.csv</b>.

        Args:
            filepath (str): Full path of the target CSV file.
            exclude_header (bool): Flag used to remove or not the header
            (the first line of the CSV file).

        Returns:
            List[AnyStr]: The list of CSV lines.

        Raises:
            SyntaxError: If <b>filepath</b> does not end with <b>.csv</b>.
        """

        if not filepath.lower().endswith(".csv"):
            raise SyntaxError("CSVService.read_lines: The only supported file extension is \".csv\"!")

        if not os.path.isfile(filepath):
            return []

        file = open(filepath, 'r+')
        lines = file.readlines()

        if exclude_header and len(lines) > 0:
            lines.pop(0)  # exclude the header

        file.close()

        return lines

    @staticmethod
    def get_string(value):
        """
        Prepare the value read from a CSV file.

        Args:
            value (str): Input value.

        Returns:
            None if the input value is an empty string, otherwise return
            the value.
        """

        if isinstance(value, str) and len(value.strip()) == 0:
            return None

        return value
