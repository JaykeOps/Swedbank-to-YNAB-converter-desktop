from converter import Converter
from SwedbankToYNAB.reader import Reader
from writer import Writer


def ask_user_for_path_to_swedbank_statements():
    return input("Enter the absolute path to the text file containing your Swedbank statements:\t")


def ask_user_for_path_to_output_ynab_csv_file():
    return input("Now enter the absolute path to the directory you want your new formatted .csv file to be stored in:\t")


def ask_user_to_for_permission_to_execute_operation(input_path, output_path):
    return input("Swedbank statements will be converted from:\n" + input_path + "to a .csv file \n" + output_path +
                 "\nDo you want to proceed with the operation?\n (y/n - yes/no)")


def main():

    input_path = ask_user_for_path_to_swedbank_statements()
    output_path = ask_user_for_path_to_output_ynab_csv_file()
    ask_user_to_for_permission_to_execute_operation(input_path, output_path)

    reader = Reader(input_path)
    swedbank_statements = reader.read_file_line_by_line_from_path()

    converter = Converter(swedbank_statements)
    ynab_csv_statements = converter.convert_from_swedbank_text_rows_to_ynab_csv_format()

    writer = Writer(ynab_csv_statements, output_path)
    writer.write_new_ynab_csv_file()

main()
