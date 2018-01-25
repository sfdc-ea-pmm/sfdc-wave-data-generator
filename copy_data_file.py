from data_generator import DataGenerator


def run(source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    # write to new path
    data_gen.write(output_file_name)
