import io


class Writer:
    def __init__(self, statements, path):
        self.__statements = statements
        self.__path = path

    def write_new_ynab_csv_file(self):

        if self.__path[len(self.__path)-4:] != ".csv":
            self.__path.append(".csv")

        try:
            with io.open(self.__path, "w") as new_file:
                new_file.writelines(self.__statements)

        except FileExistsError as error:
            raise IOError from error
        except FileNotFoundError as error:
            raise IOError from error
