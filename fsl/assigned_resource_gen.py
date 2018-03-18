import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import date
from datetime import datetime

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, source_service_resources, source_service_appointments, reference_datetime=today_datetime):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    data_gen.add_constant_column('CreatedDate__c', reference_datetime.isoformat(sep=' '))

    service_resources = data_gen.load_dataset("ServiceResources", source_service_resources, ['Id', 'External_Id__c']).dict('Id', 'External_Id__c')
    data_gen.add_map_column('ServiceResource.External_Id__c', 'ServiceResourceId', service_resources)

    service_appointments = data_gen.load_dataset("ServiceAppointments", source_service_appointments, ['Id', 'External_Id__c']).dict('Id', 'External_Id__c')
    data_gen.add_map_column('ServiceAppointment.External_Id__c', 'ServiceAppointmentId', service_appointments)

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_Id__c',
        'ServiceResource.External_Id__c',
        'ServiceAppointment.External_Id__c',
        'CreatedDate__c',
        'ActualTravelTime',
        'EstimatedTravelTime'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/AssignedResource.csv', 'data/output/AssignedResource.csv',
        'data/output/ServiceResource.csv', 'data/output/ServiceAppointment.csv')
