import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import date
from datetime import datetime
from datetime import timedelta

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, source_service_resources, source_service_appointments):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    service_resources = data_gen.load_dataset("ServiceResources", source_service_resources, ['Id', 'External_ID__c']).dict('Id', 'External_ID__c')
    data_gen.add_map_column('ServiceResource.External_Id__c', 'ServiceResourceId', service_resources)

    service_appointments = data_gen.load_dataset("ServiceAppointments", source_service_appointments, ['Id', 'External_ID__c']).dict('Id', 'External_ID__c')
    data_gen.add_map_column('ServiceAppointment.External_Id__c', 'ServiceAppointmentId', service_appointments)

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_ID__c',
        'ServiceResource.External_Id__c',
        'ServiceAppointment.External_Id__c',
        'ActualTravelTime',
        'EstimatedTravelTime'
    ])

def updateCreatedDate(source_file_name, output_file_name, source_service_appointments, reference_datetime=today_datetime):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    service_appointments = data_gen.load_dataset("ServiceAppointments", source_service_appointments, ['External_ID__c']).dict('External_ID__c', 'External_ID__c')
    service_appointments[None] = 'None'

    data_gen.add_map_column('ServiceAppointment.External_Id__c', 'ServiceAppointment.External_Id__c', service_appointments)

    data_gen.apply_transformations()


    data_gen.filter(lambda cv: cv['ServiceAppointment.External_Id__c'].startswith('ServiceAppointment'))

    data_gen.apply_transformations()


    service_appointment_dates = data_gen.load_dataset("ServiceAppointmentDates", source_service_appointments, ['External_ID__c', 'CreatedDate__c']).dict('External_ID__c', 'CreatedDate__c')
    service_appointment_dates[None] = reference_datetime + timedelta(days=-1)
    data_gen.add_map_column('CreatedDate__c', 'ServiceAppointment.External_Id__c', service_appointment_dates)

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_ID__c',
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
