from django.db import models

from data_generator import DataGenerator
from data_generator.formula import fake

class DatasetManager(object):
    def __init__(self):
        self.datasets = {}
        self.datasets["locations"] = LocationsDataset()
        self.datasets["people"] = PeopleDataset()

    def get_datasets(self):
        result = []
        for key, value in self.datasets.items():
            result.append({
                'name': key,
                'label': value.label
            })
        return result

    def get_dataset(self, dataset_name, selected_filters=None, columns=None, count=5):
        dataset = self.datasets[dataset_name]
        result = {}
        result['columns'] = dataset.get_columns()
        filters = []
        for filter in dataset.get_filters():
            filters.append({
                'name': filter.name,
                'label': filter.label,
                'required': filter.required,
                'options': filter.options
            })
        result['filters'] = filters
        result['data'] = dataset.generate(selected_filters, columns, count)
        return result


class Filter(object):
    def __init__(self, name, label, required):
        self.name = name
        self.label = label
        self.required = required
        self.options = []

    def add_option(self, name, label):
        self.options.append({'name': name, 'label': label})


class PeopleDataset(object):
    def __init__(self):
        self.label = "People"
        self.filters = []
        gender_filter = Filter('gender', 'Gender', False)
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


class LocationsDataset(object):
    def __init__(self):
        self.label = "Locations"
