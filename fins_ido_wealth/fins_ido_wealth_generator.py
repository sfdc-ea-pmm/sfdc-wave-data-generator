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

    current_year = today.year
    map_quota_year = {}
    def quotas_date_formula(dateToShift):
        def date_formula(column_values):
            if column_values[dateToShift] != "":                
                quota_year = column_values[dateToShift][:4]
                d = column_values[dateToShift].replace(quota_year, map_quota_year[quota_year])
                return d

        date_index = data_gen.column_names[dateToShift]
        dates = [e[date_index] for e in data_gen.rows]
        max_year = max(dates)[:4]
        min_year = min(dates)[:4]
        map_quota_year[max_year] = str(current_year)
        map_quota_year[min_year] = str(current_year - 1)

        data_gen.add_formula_column(dateToShift, date_formula)

    if not output_path:
        output_path = 'output/'

    for input_file in configs.get('inputFiles'):

        file_name = input_file.get('fileName')
        date_fields = input_file.get('dateFields', [])
        print("Timeshifting process for ", file_name, " will start ...")
        data_gen.load_source_file(input_path + file_name)

        for dateToShift in date_fields:
            if file_name != 'FscDemoQuota.csv':
                aux_date_formula(dateToShift)
            else:
                quotas_date_formula(dateToShift)
        data_gen.apply_transformations()
        data_gen.write(output_path + file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run('data/input/', 'data/output/latest/', 'config.json')
