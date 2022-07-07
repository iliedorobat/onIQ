CSV_COLUMN_SEPARATOR = "|"
CSV_VALUE_SEPARATOR = " && "


class CSVService:
    """
    Service used for common operations with CSV files.

    Methods:
        read_lines(filepath, exclude_header=True):
            Read the content of a CSV file.
    """

    @staticmethod
    def read_lines(filepath, exclude_header=True):
        """
        Read the content of a CSV file. Throw an exception if the file
        extension does not end with <b>.csv</b>.

        Args:
            filepath (str): Full path of the target file.
            exclude_header (bool): Flag used to remove or not the header
            (the first line of the CSV file).

        Returns:
            List[AnyStr]: The list of CSV lines.

        Raises:
            SyntaxError: If <b>filepath</b> does not end with <b>.csv</b>.
        """

        if not filepath.lower().endswith(".csv"):
            raise SyntaxError("CSVService.read_lines: The only supported file extension is \".csv\"!")

        file = open(filepath, 'r+')
        lines = file.readlines()

        if exclude_header and len(lines) > 0:
            lines.pop(0)  # exclude the header

        file.close()

        return lines
