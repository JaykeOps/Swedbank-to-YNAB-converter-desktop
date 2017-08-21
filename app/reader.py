import io


class Reader:
    def __init__(self, path):
        self._path = path

    def read_file_line_by_line_from_path(self):
        try:
            with io.open(self._path, "rb") as file:
                lines = []
                for line in file:
                    lines.append(line.decode("utf-8", "ignore"))
                return lines

        except FileNotFoundError as error:
            print("Could not read file. Are you sure you have provided the right filepath?", error)















