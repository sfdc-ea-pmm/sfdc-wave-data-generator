import boto3
import codecs
import csv
import inspect
import io
import logging
import math
import operator
import os
import random
import sys
import warnings

from collections import OrderedDict
from numpy import random

logger = logging.getLogger(__name__)
logging.basicConfig(level=20, format='%(asctime)s - %(levelname)s - %(message)s')


class DataGenerator(object):
    """
    Utility to generate data based on a source CSV file, using datasets for reference data and a list of
    column transformations to apply to the source file. The result is a new set of data with columns that
    were either added or transformed from columns in the source file.

    Attributes
    ----------
    rows : list
        A list of rows containing all column values from the source file and any applied transformations.
    datasets : dict
        A dictionary of all loaded datasets by name.
    column_names : dict
        A dictionary of column names to their corresponding index in a single row of data.
    current_row : int
        The current row index this data generator is currently processing. Useful for some formula that 
        generate a value based on the current row.
    """

    def __init__(self):
        self.rows = []
        self.datasets = {}
        self.column_names = OrderedDict()
        self.pending_column_generators = []
        self.pending_custom_column_generators = []
        self.current_row = 0
        self._row_count = None

    @property
    def row_count(self):
        """The number of rows loaded.

        You can explicitly set the row count, which is useful when generating data
        but not loading any source data.
        """
        if self._row_count is not None:
            return self._row_count
        if self.rows:
            return len(self.rows)

    @row_count.setter
    def row_count(self, row_count):
        self._row_count = row_count

    def load_source_file(self, source_file_name, source_column_names=None):
        """Loads a CSV file to be used as the source data to add columns and apply column transformations to.

        The data will be loaded either from local disk or S3 depending on the READ_MODE
        environment variable. If READ_MODE=S3, it will load the source file using the
        load_source_file_from_s3 function, otherwise it will read from local disk using
        the load_source_file_from_disk function.

        Parameters
        ----------
        source_file_name : str
            The file name (including path) of the source CSV file.
        source_column_names : list, optional
            A optional list of column names to load. If None or not provided, it will load all columns in the CSV.
        """
        if os.environ.get('READ_MODE') == 'S3':
            self.load_source_file_from_s3(source_file_name, source_column_names)
        else:
            self.load_source_file_from_disk(source_file_name, source_column_names)

    def load_source_file_from_disk(self, source_file_name, source_column_names=None):
        """Loads a CSV file from disk to be used as the source data to add columns and apply column transformations to.

        The data is loaded into the rows property as a list of column values. If a list of source_column_names 
        is defined, only those columns will be loaded.

        Parameters
        ----------
        source_file_name : str
            The file name (including path) of the source CSV file.
        source_column_names : list, optional,
            A optional list of column names to load. If None or not provided, it will load all columns in the CSV.
        """
        logger.info("Loading " + source_file_name + " from disk")
        with open(source_file_name) as source_file:
            reader = csv.reader(source_file)
            self._load_source_file(reader, source_column_names)

    def load_source_file_from_s3(self, source_file_name, source_column_names=None):
        """Loads a CSV file from S3 to be used as the source data to add columns and apply column transformations to.

        In addition to a source_file_name, the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY 
        environment variable must be set to access the appropriate AWS account. A 
        S3_BUCKET_NAME environment variable where files will reside in S3 must also be set.

        Parameters
        ----------
        source_file_name : str
            The file name (including path) of the source CSV file in the S3_BUCKET_NAME bucket.
        source_column_names : list, optional
            A optional list of column names to load. If None or not provided, it will load all columns in the CSV.
        """
        logger.info("Loading " + source_file_name + " from S3")
        client = boto3.client('s3')
        s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
        source_file_object = client.get_object(Bucket=s3_bucket_name, Key=source_file_name)
        source_file_body = source_file_object['Body']

        text_stream = codecs.getreader("utf-8")(source_file_body)
        csv_reader = csv.reader(text_stream)

        self._load_source_file(csv_reader, source_column_names)

    def _load_source_file(self, csv_reader, source_column_names=None):
        self.rows = []
        self.column_names = OrderedDict()

        # the list of input column headers
        column_names_list = next(csv_reader)
        for index, column_name in enumerate(column_names_list):
            self.column_names[column_name.strip()] = index

        # add rows
        for source_row in csv_reader:
            row = []
            for index, column_value in enumerate(source_row):
                column_name = column_names_list[index]
                # only include source column names if given
                if source_column_names is not None:
                    if column_name in source_column_names:
                        row.append(column_value)
                else:
                    row.append(column_value)
            self.rows.append(row)

        # remove column names not included in source column names
        # and shift indexes if necessary
        if source_column_names is not None:
            shift = 0
            for column_name in column_names_list:
                if column_name in source_column_names:
                    self.column_names[column_name] -= shift
                else:
                    shift += 1
            self.column_names = {column_name: index for column_name, index in self.column_names.items()
                                 if column_name in source_column_names}

    def load_dataset(self, dataset_name, dataset_file_name, source_column_names=None):
        """Loads a CSV file to be used as reference data for the data generator.

        This data will be loaded either from local disk or S3 depending on the READ_MODE
        environment variable. If READ_MODE=S3, it will load the dataset file using the
        load_dataset_from_s3 function, otherwise it will read from local disk using
        the load_dataset_from_s3 function.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.        
        dataset_file_name : str
            The file name (including path) of the dataset CSV file.
        source_column_names : list, optional
            A optional list of column names to load. If None or not provided, it will load all columns in the CSV.

        Returns
        -------
        Dataset
            A dataset containing a list of rows where each row is a dictionary of column names to their 
            values for that row.
        """
        logger.info("Loading " + dataset_name + " dataset from " + dataset_file_name)
        if os.environ.get('READ_MODE') == 'S3':
            return self.load_dataset_from_s3(dataset_name, dataset_file_name, source_column_names)
        else:
            return self.load_dataset_from_disk(dataset_name, dataset_file_name, source_column_names)

    def load_dataset_from_disk(self, dataset_name, dataset_file_name, source_column_names=None):
        """Loads a CSV file to be used as reference data for the data generator.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.        
        dataset_file_name : str
            The file name (including path) of the dataset CSV file.
        source_column_names : list, optional
            A optional list of column names to load. If None or not provided, it will load all columns in the CSV.

        Returns
        -------
        Dataset
            A dataset containing a list of rows where each row is a dictionary of column names to their 
            values for that row.
        """
        with open(dataset_file_name) as dataset_file:
            csv_reader = csv.reader(dataset_file)
            dataset = self._load_dataset(dataset_name, csv_reader, source_column_names)

        return dataset

    def load_dataset_from_s3(self, dataset_name, dataset_file_name, source_column_names=None):
        """Loads a CSV file from S3 to be used as reference data for the data generator.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.        
        dataset_file_name : str
            The file name (including path) of the dataset CSV file in the S3_BUCKET_NAME bucket.
        source_column_names : list, optional
            A optional list of column names to load. If None or not provided, it will load all columns in the CSV.

        Returns
        -------
        Dataset
            A dataset containing a list of rows where each row is a dictionary of column names to their 
            values for that row.
        """
        client = boto3.client('s3')
        s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
        source_file_object = client.get_object(Bucket=s3_bucket_name, Key=dataset_file_name)
        source_file_body = source_file_object['Body']

        text_stream = codecs.getreader("utf-8")(source_file_body)
        csv_reader = csv.reader(text_stream)

        return self._load_dataset(dataset_name, csv_reader, source_column_names)

    def _load_dataset(self, dataset_name, csv_reader, source_column_names=None):
        # the list of input column headers
        dataset_column_names = next(csv_reader)
        dataset_column_names = [column_name.strip() for column_name in dataset_column_names]

        # add rows
        dataset_rows = []
        for row in csv_reader:
            # create ordered column map (column name -> column value)
            columns = OrderedDict()
            for index, column_value in enumerate(row):
                column_name = dataset_column_names[index]
                # only include source column names if given
                if source_column_names is not None:
                    if column_name in source_column_names:
                        columns[column_name] = column_value
                else:
                    columns[column_name] = column_value
            dataset_rows.append(columns)

        dataset = Dataset(dataset_rows)
        self.datasets[dataset_name] = dataset
        return dataset

    def add_dataset(self, dataset_name, data):
        """Add arbitrary data into the dictionary of datasets.

        This is useful when a column transformation will need to this dataset frequently.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.  
        data 
            The data to add.
        """
        self.datasets[dataset_name] = data

    def remove_dataset(self, dataset_name):
        """Remove a datset from the datasets dictionary.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset to remove. 
        """
        self.datasets.pop(dataset_name)

    def rename_column(self, source_column_name, new_column_name):
        """Renames a column.

        Parameters
        ----------
        source_column_name : str
            The name of the column to rename.
        new_column_name: str
            The new name of the column.
        """
        self.column_names[new_column_name] = self.column_names.pop(source_column_name)

    def rename_columns(self, column_rename_map):
        """Renames multiple columns.

        Parameters
        ----------
        column_rename_map : dict
            A dictionary of source columns names to their new names.
        """
        for source_column_name, new_column_name in column_rename_map.items():
            self.rename_column(source_column_name, new_column_name)

    def add_constant_column(self, column_name, constant):
        """Generate a constant value or function for every row in this column.

        The provided value can be a constant value, a list of values, or a callable function. 
        If provided a list of values, a random value will be selected from the list. 
        If provided a callable function, it will be called to generate a value. 
        The callable function must either accept no parameters or a single parameter consisting of 
        column_values, a dictionary of column names to their values for the current row.

        Parameters
        ----------
        column_name : str
            The name of the column to create.
        constant : value, list, or callable
            The constant to apply.
        """
        self.pending_column_generators.append(ConstantColumnGenerator(column_name, constant))

    def add_copy_column(self, column_name, source_column_name):
        """Generate a new column by copying values from an existing column.

        Parameters
        ----------
        column_name : str
            The name of the column to create.
        source_column_name : str
            The name of the column to copy.
        """
        self.pending_column_generators.append(CopyColumnGenerator(column_name, source_column_name))

    def add_map_column(self, column_name, source_column_name, value_map):
        """Generate a value by mapping an existing value from the provided source column to a new value.

        If the column name and source column name provided are the same, it will replace the old
        values in the source column.

        The value_map provides of mapping of source column values to its new value. The new value 
        can be a constant value, a list of values, or a callable function. A mapping with key None, is used
        as a default value if no mapping exists in the value_map provided. If a mapping does not exist
        in the value_map provided and a None key is not defined, the source column value will be used instead. 

        If provided a list of values, a random value will be selected from the list. If provided a callable function, 
        it will be called to generate a value. The callable function must either accept no parameters or a single 
        parameter consisting of column_values, a dictionary of column names to their values for the current row.

        Parameters
        ----------
        column_name : str
            The name of the column to create.
        source_column_name: str
            The name of the source column.
        value_map : dict
            A mapping of source column values to their new value.
        """
        self.pending_column_generators.append(MapColumnGenerator(column_name, source_column_name, value_map))

    def add_formula_column(self, column_name, formula):
        """Generate a value by applying the given formula function.

        If the column name provided is an existing column, it replaces the old values in that column.

        The callable formula function must either accept no parameters or a single parameter consisting of 
        column_values, a dictionary of column names to their values for the current row.

        Parameters
        ----------
        column_name : str
            The name of the column to create.
        formula : callable
            The formula to apply.        
        """
        self.pending_column_generators.append(FormulaColumnGenerator(column_name, formula))

    def add_custom_column_generator(self, generator_function):
        """Generate the entire list of values to be added as columns.

        Used to create columns which cannot be formulated with any of the basic column generators. This
        column generator must provide a callable function that accepts a 3-argument parameter list consisting
        of (column_names, rows, datasets) where:

            column_names: is the dictionary of column names to their index in a single row

            rows: is all the data in a list of lists

            datasets: is the dictionary of all defined datasets

        The provided generator_function must return a dictionary of column names to add to a list of columns
        values. That list of column values must match the number of rows that exist in the data.

        If one of the entries in the dictionary is an existing column, it will replace the old data.

        Parameters
        ----------
        generator_function : callable
            The custom generator function to apply.
        """
        self.pending_custom_column_generators.append(CustomColumnGenerator(generator_function))

    def apply_transformations(self):
        """Apply all the column transformations added so far. 

        This will generate all column values and append them to the source data.
        """

        logger.info("Applying transformations")
        # reset current row
        self.current_row = 0

        # add new column names
        new_column_names = set()
        max_index = max(self.column_names.values())
        for column_generator in self.pending_column_generators:
            if column_generator.column_name not in self.column_names:
                max_index += 1
                new_column_names.add(column_generator.column_name)
                self.column_names[column_generator.column_name] = max_index

        # generate new columns from configured column generators
        for current_row, row in enumerate(self.rows):
            self.current_row = current_row
            column_values = self.row_to_column_values(row)
            new_column_values = []
            for column_generator in self.pending_column_generators:
                column_name = column_generator.column_name
                new_column_value = column_generator.generate_value(column_values)
                column_values[column_name] = new_column_value

                if column_name in new_column_names:
                    # add new column
                    new_column_values.append(new_column_value)
                else:
                    # transform existing column
                    column_index = self.column_names[column_name]
                    row[column_index] = new_column_value
            row.extend(new_column_values)

        # generate new columns from configured custom column generators
        for custom_column_generator in self.pending_custom_column_generators:
            custom_columns = custom_column_generator.generate_columns(self.column_names, self.rows)
            for column_name, column_values in custom_columns.items():
                is_new_column = False
                if len(column_values) != len(self.rows):
                    warnings.warn(column_name + ' does not have the same number of rows as source data')

                if column_name not in self.column_names:
                    max_index += 1
                    self.column_names[column_name] = max_index
                    is_new_column = True

                for index, row in enumerate(self.rows):
                    if is_new_column:
                        # new column
                        row.append(column_values[index])
                    else:
                        # existing column
                        column_index = self.column_names[column_name]
                        row[column_index] = column_values[index]

        # clear pending column generators
        self.current_row = 0
        self.pending_column_generators = []
        self.pending_custom_column_generators = []

    def filter(self, filter_function):
        """Filter rows given a filter_function to evaluate against each row.

        All rows which in which the filter_function evaluates to true will be kept. The filter_function
        will be called with a single argument that contains a dict of column names to their corresponding
        value.

        Parameters
        ----------
        filter_function : callable
            The function to filter against.
        """
        if not callable(filter_function):
            raise ValueError("filter_function must be a callable function")

        filtered_rows = []
        for i in range(len(self.rows)):
            row = self.rows.pop()
            if filter_function(self.row_to_column_values(row)):
                filtered_rows.append(row)

        self.rows = filtered_rows
        self.reverse()

    def sort_by(self, column_name, reverse=False):
        """Sort rows by a given column.

        An optional reverse boolean can be specified to reverse the order of the list.

        Parameters
        ----------
        column_name : str
            The column to sort by.
        reverse : bool, optional
            The order will be reversed if true.
        """
        column_index = self.column_names[column_name]
        self.rows.sort(key=operator.itemgetter(column_index), reverse=reverse)

    def shuffle(self):
        """Shuffle rows randomly in place."""
        random.shuffle(self.rows)

    def reverse(self):
        """Reverse rows in place."""
        self.rows.reverse()

    def unique(self):
        """Filters rows to just unique data with no duplicate rows"""
        unique_tuples = set()
        unique_rows = []
        for i in range(len(self.rows)):
            row = self.rows.pop()
            row_tuple = tuple(row)
            if row_tuple not in unique_tuples:
                unique_rows.append(row)
                unique_tuples.add(row_tuple)

        self.rows = unique_rows
        self.reverse()

    def duplicate_rows(self, duplication_factor):
        """Duplicates rows in the data by the given duplication factor.
        
        The duplication factor can be a constant int value or a callable function. If provided a 
        int value, each row will be duplicated that many times.  If provided a callable function, 
        it will be called to generate a int value for every row. The callable function must either 
        accept no parameters or a single parameter consisting of column_values, a dictionary of 
        column names to their values for the current row.
        
        Parameters
        ----------
        duplication_factor: int, callable
            A constant int value or callable function.
        """
        is_callable = callable(duplication_factor)
        call_with_args = False
        if is_callable and inspect.getfullargspec(duplication_factor).args:
            call_with_args = True

        new_rows = []
        count = len(self.rows)
        for i in range(count):
            row = self.rows.pop()
            column_values = self.row_to_column_values(row)

            if is_callable:
                # this is a callable function
                if call_with_args:
                    # call function with arguments
                    duplication_count = duplication_factor(column_values)
                else:
                    # call function without arguments
                    duplication_count = duplication_factor()
            else:
                duplication_count = duplication_factor

            for j in range(duplication_count):
                new_rows.append(row[:])
        self.rows = new_rows
        self.reverse()

    def write(self, output_file_name, columns=None, max_rows=sys.maxsize):
        """Writes the specified list of columns to a CSV file.

        The data will be written to local disk or S3 depending on the WRITE_MODE
        environment variable. If WRITE_MODE=S3, it will write the file using the
        write_to_s3 function, otherwise it will write to local disk with the 
        write_to_disk function.

        Parameters
        ----------
        output_file_name : str
            The file name (including path) of the output CSV file.
        columns : list, optional
            A optional list of column names to write. If None or not provided, it will write all columns to the CSV.
        max_rows: int, optional
            A maximum number of rows to write before continuing to a new file
            
        Returns
        -------
        list
            A list of output file names that were written.
        """
        if os.environ.get('WRITE_MODE') == 'S3':
            return self.write_to_s3(output_file_name, columns, max_rows)
        else:
            return self.write_to_disk(output_file_name, columns, max_rows)

    def write_to_disk(self, output_file_name, columns=None, max_rows=sys.maxsize):
        """Writes the specified list of columns to a CSV file.

        Parameters
        ----------
        output_file_name : str
            The file name (including path) of the output CSV file.
        columns : list, optional
            A optional list of column names to write. If None or not provided, it will write all columns to the CSV.
        max_rows: int, optional
            A maximum number of rows to write before continuing to a new file
            
        Returns
        -------
        list
            A list of output file names that were written.
        """
        if self.pending_column_generators or self.pending_custom_column_generators:
            logger.warning('Pending column generators have not been applied. ' +
                           'Did you forget to run apply_transformations()?')
        logger.info("Writing " + output_file_name + " to disk")

        if columns is None:
            # use all columns and sort by column index
            column_order = sorted(self.column_names.items(), key=operator.itemgetter(1))
        else:
            # use provided columns and column order
            column_order = [(column_name, self.column_names[column_name]) for column_name in columns]

        files = []
        file_count = int(math.ceil(self.row_count / max_rows))

        if file_count > 1:
            base_output_file_name = output_file_name.split('.')[0]
            base_output_ext = output_file_name.split('.')[1]
            for i in range(file_count):
                file_name = base_output_file_name + '-' + str(i) + '.' + base_output_ext
                if i == 0:
                    file_name = base_output_file_name + '.' + base_output_ext

                files.append(file_name)
                with open(file_name, 'w') as output_file:
                    writer = csv.writer(output_file, delimiter=',')

                    # write header
                    writer.writerow([column_name for column_name, index in column_order])

                    for r in range(max_rows):
                        index = (i * max_rows) + r
                        if index < self.row_count:
                            # write columns in order
                            ordered_row = []
                            for column_name, index in column_order:
                                ordered_row.append(self.rows[(i * max_rows) + r][index])
                            writer.writerow(ordered_row)
        else:
            files.append(output_file_name)
            with open(output_file_name, 'w') as output_file:
                writer = csv.writer(output_file, delimiter=',')

                # write header
                writer.writerow([column_name for column_name, index in column_order])

                for row in self.rows:
                    # write columns in order
                    ordered_row = []
                    for column_name, index in column_order:
                        ordered_row.append(row[index])
                    writer.writerow(ordered_row)
        return files

    def write_to_s3(self, output_file_name, columns=None, max_rows=sys.maxsize):
        """Writes the specified list of columns to a CSV file in S3.

        The AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variable must be set to 
        write to a AWS account. A S3_BUCKET_NAME environment variable where files will reside 
        in S3 must also be set.

        Parameters
        ----------
        output_file_name : str
            The file name (including path) of the output CSV file.
        columns : list, optional
            A optional list of column names to write. If None or not provided, it will write all columns to the CSV.
        max_rows: int, optional
            A maximum number of rows to write before continuing to a new file
            
        Returns
        -------
        list
            A list of output file names that were written.
        """
        if self.pending_column_generators or self.pending_custom_column_generators:
            logger.warning('Pending column generators have not been applied. ' +
                           'Did you forget to run apply_transformations()?')
        logger.info("Writing " + output_file_name + " to S3")
        client = boto3.client('s3')
        s3_bucket_name = os.environ.get('S3_BUCKET_NAME')

        if columns is None:
            # use all columns and sort by column index
            column_order = sorted(self.column_names.items(), key=operator.itemgetter(1))
        else:
            # use provided columns and column order
            column_order = [(column_name, self.column_names[column_name]) for column_name in columns]

        files = []
        file_count = int(math.ceil(self.row_count / max_rows))

        if file_count > 1:
            base_output_file_name = output_file_name.split('.')[0]
            base_output_ext = output_file_name.split('.')[1]

            for i in range(file_count):
                file_name = base_output_file_name + '-' + str(i) + '.' + base_output_ext
                if i == 0:
                    file_name = base_output_file_name + '.' + base_output_ext
                files.append(file_name)

                csv_output = io.StringIO()
                writer = csv.writer(csv_output, delimiter=',')

                # write header
                writer.writerow([column_name for column_name, index in column_order])

                for r in range(max_rows):
                    index = (i * max_rows) + r
                    if index < self.row_count:
                        # write columns in order
                        ordered_row = []
                        for column_name, index in column_order:
                            ordered_row.append(self.rows[(i * max_rows) + r][index])
                        writer.writerow(ordered_row)

                csv_output.seek(0)
                output_fileobj = io.BytesIO(bytes(csv_output.read(), 'utf-8'))
                csv_output.close()
                client.upload_fileobj(output_fileobj, s3_bucket_name, file_name)
                output_fileobj.close()
                client.put_object_acl(ACL='public-read', Bucket=s3_bucket_name, Key=file_name)
        else:
            files.append(output_file_name)
            csv_output = io.StringIO()
            writer = csv.writer(csv_output, delimiter=',')

            # write header
            writer.writerow([column_name for column_name, index in column_order])

            for row in self.rows:
                # write columns in order
                ordered_row = []
                for column_name, index in column_order:
                    ordered_row.append(row[index])
                writer.writerow(ordered_row)

            csv_output.seek(0)
            output_fileobj = io.BytesIO(bytes(csv_output.read(), 'utf-8'))
            csv_output.close()
            client.upload_fileobj(output_fileobj, s3_bucket_name, output_file_name)
            output_fileobj.close()
            client.put_object_acl(ACL='public-read', Bucket=s3_bucket_name, Key=output_file_name)
        return files

    def row_to_column_values(self, row):
        """Convert a row of data into a dictionary of column names to values.

        Parameters
        ----------
        row: list
            The row of data to convert.

        Returns
        -------
        dict
            A dictionary of column names to values.
        """
        column_values = {}
        for column_name, index in self.column_names.items():
            if index < len(row):
                column_values[column_name] = row[index]
        return column_values

    def column_values_to_row(self, column_values):
        """Convert dictionary of column names to values to a row of data.

        Parameters
        ----------
        column_values: dict
            The dictionary of column names to values to convert.

        Returns
        -------
        list
            A row of data.
        """
        row = []
        column_order = sorted(self.column_names.items(), key=operator.itemgetter(1))
        for column_name, index in column_order:
            value = column_values.get(column_name)
            if value is None:
                row.append('')
            else:
                row.append(value)
        return row

    def rows_to_dataset(self):
        """Convert the the rows of this data to a Dataset.

        Returns
        -------
        Dataset
            The rows of this data as a Dataset.
        """
        data = []
        for row in self.rows:
            data.append(self.row_to_column_values(row))
        return Dataset(data)


class Dataset(object):
    """Reference data loaded and used by a data generator.

    The data is loaded as a list of rows where each row contains a dictionary
    of column names to their values for that row.

    Attributes
    ----------
    data : list
        A list of rows where each row is a dictionary of column names to their values for that row.
    """

    def __init__(self, data):
        self.data = data

    def group_by(self, column_name):
        """Creates a dictionary grouped by the given column.

        The result is a dictionary where the key is a unique column value in the given column and the value is
        a list of rows matching that column value.

        Parameters
        ----------
        column_name : str
            The name of the column to group by.

        Returns
        -------
        dict
            A dictionary where the key is a unique column value in the provided column and the value
            is a list of rows that matching that column value.
        """
        grouping = {}
        for row in self.data:
            value = row.get(column_name)
            if value not in grouping:
                grouping[value] = []

            grouping[value].append(row)
        return grouping

    def unique(self, column_name):
        """Returns a list of unique values for the given column.

        Parameters
        ----------
        column_name : str
            The name of the column to extract unique values from.

        Returns
        -------
        list
            A list of unique values in the column.
        """
        unique_values = set()
        for row in self.data:
            value = row.get(column_name)
            unique_values.add(value)
        return list(unique_values)


class ColumnGenerator(object):
    """Base class that generates the values of a specific column."""

    def __init__(self, column_name, generator_type):
        self.name = column_name + '_' + generator_type
        self.column_name = column_name
        self.generator_type = generator_type

    def generate_value(self, column_values):
        """Overriden by subclasses to generate a column value."""
        raise NotImplementedError("Subclasses must implement this method")


class ConstantColumnGenerator(ColumnGenerator):
    """Generate a constant value or function for every row in this column.

    This generator must provide a value to use for the column. This value can be a constant value, 
    a list of values, or a callable function. If provided a list of values, a random value will be 
    selected from the list. If provided a callable function, it will be called to generate a value. 
    The callable function must either accept no parameters or a single parameter consisting of 
    column_values, a dictionary of column names to their values for the current row.
    """

    def __init__(self, column_name, constant, generator_type='constant'):
        super(ConstantColumnGenerator, self).__init__(column_name, generator_type)
        self.constant = constant
        self._is_callable = callable(self.constant)
        self._call_with_args = False
        if self._is_callable and inspect.getfullargspec(self.constant).args:
            self._call_with_args = True
        self._is_list = isinstance(self.constant, (list, tuple))

    def generate_value(self, column_values):
        if self._is_callable:
            # this is a callable function
            if self._call_with_args:
                # call function with arguments
                return self.constant(column_values)
            else:
                # call function without arguments
                return self.constant()
        elif self._is_list:
            # if constant is a list, randomly assign a value in the list
            return random.choice(self.constant)
        else:
            # add constant value
            return self.constant


class CopyColumnGenerator(ColumnGenerator):
    """Generate a copy of an existing column for each row in this column.

    This generator must provide the column name of the new column and the source column name
    to copy.
    """

    def __init__(self, column_name, source_column_name, generator_type='copy'):
        super(CopyColumnGenerator, self).__init__(column_name, generator_type)
        self.source_column_name = source_column_name

    def generate_value(self, column_values):
        return column_values[self.source_column_name]


class MapColumnGenerator(ColumnGenerator):
    """Generate a value by mapping an existing value from the provided source column to a new value.

    This generator must provide a mapping of source column values to its new value. The new value 
    can be a constant value, a list of values, or a callable function. A mapping with key None, is used
    as a default value if no mapping exists in the value_map provided. If a mapping does not exist
    in the value_map provided and a None key is not defined, the source column value will be used instead. 

    If provided a list of values, a random value will be selected from the list. If provided a callable function, 
    it will be called to generate a value. The callable function must either accept no parameters or a single 
    parameter consisting of column_values, a dictionary of column names to their values for the current row.
    """

    def __init__(self, column_name, source_column_name, value_map, generator_type='map'):
        super(MapColumnGenerator, self).__init__(column_name, generator_type)
        self.source_column_name = source_column_name
        self.value_map = value_map
        self._value_map_metadata = {}
        for source_value, new_value in self.value_map.items():
            metadata = {}
            metadata['is_callable'] = callable(new_value)
            metadata['call_with_args'] = False
            if metadata['is_callable'] and inspect.getfullargspec(new_value).args:
                metadata['call_with_args'] = True
            metadata['is_list'] = isinstance(new_value, (list, tuple))
            self._value_map_metadata[source_value] = metadata

    def generate_value(self, column_values):
        source_value = column_values[self.source_column_name]
        new_value = self.value_map.get(source_value)

        if new_value is None:
            # check for None entry in map
            new_value = self.value_map.get(None)
            if new_value is None:
                # if None mapping defined, default to source value
                return source_value
            source_value = None

        metadata = self._value_map_metadata[source_value]
        if metadata['is_callable']:
            # this is a callable function
            if metadata['call_with_args']:
                # call function with arguments
                return new_value(column_values)
            else:
                # call function without arguments
                return new_value()
        elif metadata['is_list']:
            # if new value is a list, randomly assign a value in the list
            return random.choice(new_value)
        else:
            # add new value
            return new_value


class FormulaColumnGenerator(ColumnGenerator):
    """Generate a value by applying the given formula function.

    This generator must provide a callable function. This callable formulat function must either accept 
    no parameters or a single parameter consisting of column_values, a dictionary of column names to 
    their values for the current row.
    """

    def __init__(self, column_name, formula, generator_type='formula'):
        super(FormulaColumnGenerator, self).__init__(column_name, generator_type)
        self.formula = formula
        self._is_callable = callable(self.formula)
        self._call_with_args = False
        if self._is_callable and inspect.getfullargspec(self.formula).args:
            self._call_with_args = True
        self._is_list = isinstance(self.formula, (list, tuple))

    def generate_value(self, column_values):
        if self._is_callable:
            # this is a callable function
            if self._call_with_args:
                # call function with arguments
                return self.formula(column_values)
            else:
                # call function without arguments
                return self.formula()
        elif self._is_list:
            # if formula is a list, randomly assign a value in the list
            return random.choice(self.formula)
        else:
            # formula is a constant value
            return self.formula


class CustomColumnGenerator(object):
    """Generate the entire list of values to be added as columns in the data generator.

    Used to create columns which cannot be formulated with any of the basic column generators. This
    column generator must provide a callable function that accepts a 2-argument parameter list consisting
    of (column_names, rows) where:

        column_names: is the dictionary of column names to their index in a single row

        rows: is all the data in a list of lists

    The provided generator_function must return a dictionary of column names to add to a list of columns
    values. That list of column values must match the number of rows that exist in the data.
    """

    def __init__(self, generator_function):
        if not callable(generator_function):
            raise ValueError('generator_function must be a callable function')
        self.generator_function = generator_function

    def generate_columns(self, column_names, rows):
        return self.generator_function(column_names, rows)
