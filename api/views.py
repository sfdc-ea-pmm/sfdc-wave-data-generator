from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.decorators import renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from data_generator import DataGenerator
from data_generator.formula import fake


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
@renderer_classes((JSONRenderer,))
def generate(request):
    data_gen = DataGenerator()
    data_gen.row_count = 20
    data_gen.add_formula_column("names", formula=fake.name)
    data_gen.apply_transformations()
    flat = [val for sublist in data_gen.rows for val in sublist]
    return Response(flat)
