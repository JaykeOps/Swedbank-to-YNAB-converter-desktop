import re
from datetime import datetime
from datetime import date
from statement import Statement


class Converter:
    def __init__(self, swedbank_text_row_statements):
        self.__swedbank_text_row_statements = swedbank_text_row_statements
        self.__statement_objects = []

    def convert_from_swedbank_text_rows_to_ynab_csv_format(self):

        def remove_six_opening_lines():
            del self.__swedbank_text_row_statements[0:6]

        def remove_first_four_columns():
            for row in range(len(self.__swedbank_text_row_statements)):
                line = self.__swedbank_text_row_statements[row]
                self.__swedbank_text_row_statements[row] = line[47:]

        def set_statement_objects_from_swedbank_text_rows():

            def extract_dates_from_row(i):
                return re.findall("([0-9]{2}-[0-9]{2}-[0-9]{2})", self.__swedbank_text_row_statements[i])

            def extract_sum_from_row(i):
                s = re.search("(-|[\d])+(\d)+(,)+([\d]*)", self.__swedbank_text_row_statements[i].replace(" ", ""))
                return s.group(0).replace(",", ".")

            def extract_payee_from_row():
                return self.__swedbank_text_row_statements[row_index][33:66]

            for row_index in range(len(self.__swedbank_text_row_statements)):
                statement = Statement()

                statement.sum = extract_sum_from_row(row_index)

                dates = extract_dates_from_row(row_index)
                statement.entry_date = date.strftime(datetime.strptime(dates[0], "%y-%m-%d"), "%d-%m-%Y")
                statement.transaction_date = dates[1]

                statement.payee = extract_payee_from_row()

                statement.memo = "placeholder"

                self.__statement_objects.append(statement)

        def get_ynab_csv_rows_from_statement_objects():

            rows = []

            def format_to_inflow_statement(s):
                return (s.entry_date + "," +
                        s.payee + ",," +
                        s.memo + ",," +
                        s.sum + "," + "\n")

            def format_to_outflow_statement(s):
                return (s.entry_date + "," +
                        s.payee + ",," +
                        s.memo + "," +
                        s.sum.replace("-", "") + "," + "\n")

            def remove_csv_comma_separator_from_last_row():
                last_row = rows.pop()
                last_row = last_row[:len(last_row) - 2]
                rows.append(last_row)

            for i in range(len(self.__statement_objects)):

                statement = self.__statement_objects[i]
                result = format_to_outflow_statement(statement) if statement.sum[0] == "-" \
                    else format_to_inflow_statement(statement)

                result = result.replace(" ", "")
                rows.append(result)

            remove_csv_comma_separator_from_last_row()
            return rows

        remove_six_opening_lines()
        remove_first_four_columns()
        set_statement_objects_from_swedbank_text_rows()
        return get_ynab_csv_rows_from_statement_objects()
