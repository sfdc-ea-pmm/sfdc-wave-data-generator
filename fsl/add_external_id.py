from data_generator import DataGenerator


def run(source_file_name, prefix, output_file_name):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    data_gen.add_formula_column('External_ID__c', formula=lambda cv: cv['External_ID__c'] if 'External_ID__c' in cv and not str(cv['External_ID__c']) == "" else prefix + '.' + str(data_gen.current_row + 1 + 100))

    data_gen.apply_transformations()

    # write to new path
    data_gen.write(output_file_name)
