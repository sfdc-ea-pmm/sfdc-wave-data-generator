import json

from datetime import timedelta, date
from datetime import datetime
import dateutil

from data_generator import DataGenerator

today = date.today()

def file_to_string(relative_path):
    str_file = open(relative_path, 'r').read()
    return str_file

def run(input_path, output_path, config_source):
    configs = json.loads(file_to_string(config_source))
    time_shifting_file = configs.get('timeShiftingPivot').get('fileName')
    time_shifting_field = configs.get('timeShiftingPivot').get('fieldName')

    data_gen = DataGenerator()

    data_gen.load_source_file(input_path + time_shifting_file, time_shifting_field)

    aux_date = max([x[0] for x in data_gen.rows])[:10]

    delta_to_increase = (today - datetime.strptime(aux_date, "%Y-%m-%d").date()).days


    def aux_date_formula(dateToShift):
        def date_formula(column_values):
            if column_values[dateToShift] != "":
                create_date = dateutil.parser.parse(column_values[dateToShift])
                if len(column_values[dateToShift]) == 19:
                    return (create_date + timedelta(days=delta_to_increase)).strftime('%Y-%m-%d %H:%M:%S')
                elif len(column_values[dateToShift]) < 24:
                    return (create_date + timedelta(days=delta_to_increase)).strftime('%Y-%m-%d')
                else:
                    return (create_date + timedelta(days=delta_to_increase)).strftime('%Y-%m-%dT%H:%M:%S.000Z')

        data_gen.add_formula_column(dateToShift, date_formula)

    if not output_path:
        output_path = 'output/'

    for input_file in configs.get('inputFiles'):

        file_name = input_file.get('fileName')
        date_fields = input_file.get('dateFields', [])

        data_gen.load_source_file(input_path + file_name)

        for dateToShift in date_fields:
            aux_date_formula(dateToShift)
            data_gen.apply_transformations()
        data_gen.write(output_path + file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run('data/input/', 'data/output/latest/', 'config.json')
