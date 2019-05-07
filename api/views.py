from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.decorators import renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from data_generator import DataGenerator
from data_generator.formula import fake

from api.models import DatasetManager


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@renderer_classes((JSONRenderer,))
def datasets(request):
    if 'type' in request.data:
        dataset_type = request.data['type']
        selected_filters = None
        if 'filters' in request.data:
            selected_filters = request.data['filters']
        columns = None
        if 'columns' in request.data:
            columns = request.data['columns']
        count = 5
        if 'count' in request.data:
            count = request.data['count']
        return Response(DatasetManager().get_dataset(dataset_type, selected_filters, columns, count))
    else:
        return Response(DatasetManager().get_datasets())

@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@renderer_classes((JSONRenderer,))
def generate(request):
    data_gen = DataGenerator()
    count = int(request.data['count'])
    type = request.data['type']
    data_gen.row_count = count
    if type == 'name':
        data_gen.add_formula_column('name', formula=fake.name)
    elif type == 'name_male':
        data_gen.add_formula_column('name_male', formula=fake.name_male)
    elif type == 'name_female':
        data_gen.add_formula_column('name_female', formula=fake.name_female)
    elif type == 'first_name':
        data_gen.add_formula_column('first_name', formula=fake.first_name)
    elif type == 'first_name_male':
        data_gen.add_formula_column('first_name_male', formula=fake.first_name_male)
    elif type == 'first_name_female':
        data_gen.add_formula_column('first_name_female', formula=fake.first_name_female)
    elif type == 'last_name':
        data_gen.add_formula_column('last_name', formula=fake.last_name)
    elif type == 'last_name_male':
        data_gen.add_formula_column('last_name_male', formula=fake.last_name_male)
    elif type == 'last_name_female':
        data_gen.add_formula_column('first_name_female', formula=fake.first_name_female)
    elif type == 'prefix':
        data_gen.add_formula_column('prefix', formula=fake.prefix)
    elif type == 'prefix_male':
        data_gen.add_formula_column('prefix_male', formula=fake.prefix_male)
    elif type == 'prefix_female':
        data_gen.add_formula_column('prefix_female', formula=fake.prefix_female)
    elif type == 'suffix':
        data_gen.add_formula_column('suffix', formula=fake.suffix)
    elif type == 'suffix_male':
        data_gen.add_formula_column('suffix_male', formula=fake.suffix_male)
    elif type == 'suffix_female':
        data_gen.add_formula_column('suffix_female', formula=fake.suffix_female)
    elif type == 'phone_number':
        data_gen.add_formula_column('phone_number', formula=fake.phone_number)
    elif type == 'ssn':
        data_gen.add_formula_column('ssn', formula=fake.ssn)
    elif type == 'address':
        data_gen.add_formula_column('address', formula=fake.address)
    elif type == 'building_number':
        data_gen.add_formula_column('building_number', formula=fake.building_number)
    elif type == 'street_name':
        data_gen.add_formula_column('street_name', formula=fake.street_name)
    elif type == 'street_address':
        data_gen.add_formula_column('street_address', formula=fake.street_address)
    elif type == 'street_suffix':
        data_gen.add_formula_column('street_suffix', formula=fake.street_suffix)
    elif type == 'secondary_address':
        data_gen.add_formula_column('secondary_address', formula=fake.secondary_address)
    elif type == 'city':
        data_gen.add_formula_column('city', formula=fake.city)
    elif type == 'state':
        data_gen.add_formula_column('state', formula=fake.state)
    elif type == 'state_abbr':
        data_gen.add_formula_column('state_abbr', formula=fake.state_abbr)
    elif type == 'zipcode':
        data_gen.add_formula_column('zipcode', formula=fake.zipcode)
    elif type == 'zipcode_plus4':
        data_gen.add_formula_column('zipcode_plus4', formula=fake.zipcode_plus4)
    elif type == 'country':
        data_gen.add_formula_column('country', formula=fake.country)
    elif type == 'country_code':
        data_gen.add_formula_column('country_code', formula=fake.country_code)
    elif type == 'company':
        data_gen.add_formula_column('company', formula=fake.company)
    elif type == 'job':
        data_gen.add_formula_column('job', formula=fake.job)
    elif type == 'ipv4':
        data_gen.add_formula_column('ipv4', formula=fake.ipv4)
    elif type == 'ipv6':
        data_gen.add_formula_column('ipv6', formula=fake.ipv6)
    elif type == 'url':
        data_gen.add_formula_column('url', formula=fake.url)
    elif type == 'free_email':
        data_gen.add_formula_column('free_email', formula=fake.free_email)
    elif type == 'safe_email':
        data_gen.add_formula_column('safe_email', formula=fake.safe_email)
    elif type == 'company_email':
        data_gen.add_formula_column('company_email', formula=fake.company_email)
    elif type == 'browser':
        data_gen.add_formula_column('browser', formula=fake.browser)
    elif type == 'md5':
        data_gen.add_formula_column('md5', formula=fake.md5)
    elif type == 'user_agent':
        data_gen.add_formula_column('user_agent', formula=fake.user_agent)
    elif type == 'sentence':
        data_gen.add_formula_column('sentence', formula=fake.sentence)
    else:
        data_gen.add_formula_column('name', formula=fake.name)

    data_gen.apply_transformations()
    flat = [val for sublist in data_gen.rows for val in sublist]
    return Response(flat)

