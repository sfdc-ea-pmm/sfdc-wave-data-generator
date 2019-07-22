from django.db import models

from data_generator import DataGenerator
from data_generator.formula import fake

import os
dirname = os.path.dirname(__file__)

class DatasetManager(object):
    def __init__(self):
        self.datasets = {}
        self.datasets['france'] = FileGeneratedDataset(
            'France',
            os.path.join(dirname, 'data/France-GeoCoded.csv'),
            ['BillingStreet', 'BillingCity', 'BillingState', 'BillingPostalCode', 'BillingCountry', 'Country', 'lat', 'lon', 'latlong', 'Address'],
            ['BillingState', 'BillingCity'])
        self.datasets['people'] = PeopleDataset()
        self.datasets['address_japan'] = FileGeneratedDataset(
            'Address - Japan',
            os.path.join(dirname, 'data/address_Japanese.csv'),
            ['BillingCountry', 'BillingPostalCode', 'BillingStreet', 'BillingCity', 'BillingState', 'Country', 'lon', 'lat', 'latlong', 'Address'],
            ['BillingState', 'BillingCity'])
        self.datasets['person_japan'] = FileGeneratedDataset(
            'Person - Japan',
            os.path.join(dirname, 'data/personName_Japanese.csv'),
            ['FullName', 'FirstName', 'LastName', 'Gender'],
            ['Gender'])

    def get_datasets(self):
        result = []
        for key, value in self.datasets.items():
            result.append(self.get_dataset(key))
        return result

    def get_dataset(self, dataset_name, selected_filters=None, columns=None, count=5):
        dataset = self.datasets[dataset_name]
        result = {}
        result['name'] = dataset_name
        result['label'] = dataset.label
        result['columns'] = dataset.get_columns()
        filters = []
        for filter in dataset.get_filters():
            filters.append({
                'name': filter.name,
                'label': filter.label,
                'options': filter.options
            })
        result['filters'] = filters
        result['data'] = dataset.generate(selected_filters, columns, count)
        return result


class StringFilter(object):
    def __init__(self, name, label):
        self.type = 'String'
        self.name = name
        self.label = label
        self.options = []

    def add_option(self, name, label):
        self.options.append({'name': name, 'label': label})


class StringListFilter(object):
    def __init__(self, name, label, options_list):
        self.type = 'String'
        self.name = name
        self.label = label
        self.options = []

        for option in sorted(options_list):
            if option != '' or option != ',':
                self.options.append({'name': option, 'label': option})


class PeopleDataset(object):
    def __init__(self):
        self.label = "People"
        self.filters = []
        gender_filter = StringFilter('gender', 'Gender')
        gender_filter.add_option('male', 'Male')
        gender_filter.add_option('female', 'Female')
        self.filters.append(gender_filter)

        self.columns = ['Gender', 'First Name', 'Last Name', 'Name']

    def get_filters(self):
        return self.filters

    def get_columns(self):
        return self.columns

    def generate(self, selected_filters=None, columns=None, count=5):
        if selected_filters is None:
            selected_filters = {}
        if columns is None:
            columns = self.get_columns()

        data_gen = DataGenerator()
        data_gen.row_count = count

        if 'gender' in selected_filters:
            if selected_filters['gender'] == 'male':
                data_gen.add_constant_column('Gender', 'Male')
            else:
                data_gen.add_constant_column('Gender', 'Female')
        else:
            data_gen.add_formula_column('Gender', formula=fake.gender)

        def first_name_formula(column_values):
            if column_values['Gender'] == 'Male':
                return fake.first_name_male()
            else:
                return fake.first_name_female()

        data_gen.add_formula_column('First Name', first_name_formula)

        data_gen.add_formula_column('Last Name', formula=fake.last_name)
        data_gen.add_formula_column('Name', lambda cv: cv['First Name'] + ' ' + cv['Last Name'])

        data_gen.apply_transformations()
        return list(map(lambda r: data_gen.row_to_column_values(r, columns).values(), data_gen.rows))


class FileGeneratedDataset(object):
    def __init__(self, label, source_file_name, columns=None, string_filters=None):
        self.label = label
        self.filters = []
        self.source_file_name = source_file_name
        self.columns = columns
        self.string_filters = string_filters

        data_gen = DataGenerator()

        if columns is None:
            data_gen.load_source_file_from_disk(self.source_file_name)
        else:
            data_gen.load_source_file_from_disk(self.source_file_name, columns)

        filters_dataset = data_gen.load_dataset_from_disk('filters', source_file_name)

        for filter_name in string_filters:
            options_list = filters_dataset.unique(filter_name)
            self.filters.append(StringListFilter(filter_name, filter_name, options_list))

        if columns is None:
            self.columns = list(data_gen.column_names.keys())
        else:
            self.columns = columns

    def get_filters(self):
        return self.filters

    def get_columns(self):
        return self.columns

    def generate(self, selected_filters=None, columns=None, count=5):
        if selected_filters is None:
            selected_filters = {}
        if columns is None:
            columns = self.get_columns()

        data_gen = DataGenerator()
        data_gen.load_source_file_from_disk(self.source_file_name, columns)

        for filter_key, filter_value in selected_filters.items():
            data_gen.filter(lambda cv: cv[filter_key] == filter_value)

        if data_gen.row_count <= 0:
            return []


        remaining_count = count
        result = []
        while remaining_count > 0:
            data_gen.shuffle()

            if data_gen.row_count >= remaining_count:
                data_gen.row_count = remaining_count

            result += list(map(lambda r: data_gen.row_to_column_values(r, columns).values(), data_gen.rows))
            remaining_count -= data_gen.row_count

        return result


dataset_manager = DatasetManager()