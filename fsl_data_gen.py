import copy_data_file
import os

from datetime import date
from datetime import datetime
from fsl import account_gen
from fsl import assigned_resource_gen
from fsl import add_external_id
from fsl import case_gen
from fsl import operating_hours_gen
from fsl import pricebook_entry_gen
from fsl import product_gen
from fsl import product_consumed_gen
from fsl import resource_absence_gen
from fsl import service_appointment_gen
from fsl import service_resource_gen
from fsl import service_territory_gen
from fsl import time_slot_gen
from fsl import work_order_gen
from fsl import work_type_gen
from fsl import user_gen


def run():
    today = date.today()
    today_datetime = datetime.combine(today, datetime.min.time())
    source_path = 'fsl/data/input/'
    output_path = 'fsl/data/output/archive/{}/'.format(today.isoformat())

    batch_id = datetime.now().strftime("%Y%m%d%-H%M%S%f")

    # make output directory if it doesn't exist
    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    account_file = 'Account.csv'
    assigned_resource_file = 'AssignedResource.csv'
    case_file = 'Case.csv'
    operating_hours_file = 'OperatingHours.csv'
    pricebook_entry_file = 'PricebookEntry.csv'
    product_file = 'Product2.csv'
    product_consumed_file = 'ProductConsumed.csv'
    resource_absence_file = 'ResourceAbsence.csv'
    service_appointment_file = 'ServiceAppointment.csv'
    service_resource_file = 'ServiceResource.csv'
    service_territory_file = 'ServiceTerritory.csv'
    time_slot_file = 'TimeSlot.csv'
    user_file = 'User.csv'
    work_order_file = 'WorkOrder.csv'
    work_type_file = 'WorkType.csv'
    profile_file = 'Profile.csv'

    # add external ids to source files
    add_external_id.run(source_path + account_file, 'Account', output_path + account_file)
    add_external_id.run(source_path + assigned_resource_file, 'AssignedResource', output_path + assigned_resource_file)
    add_external_id.run(source_path + case_file, 'Case', output_path + case_file)
    add_external_id.run(source_path + operating_hours_file, 'OperatingHours', output_path + operating_hours_file)
    add_external_id.run(source_path + pricebook_entry_file, 'PricebookEntry', output_path + pricebook_entry_file)
    add_external_id.run(source_path + product_file, 'Product', output_path + product_file)
    add_external_id.run(source_path + product_consumed_file, 'W_FSL_ProductConsumed', output_path + product_consumed_file)
    add_external_id.run(source_path + resource_absence_file, 'ResourceAbsence', output_path + resource_absence_file)
    add_external_id.run(source_path + service_appointment_file, 'ServiceAppointment', output_path + service_appointment_file)
    add_external_id.run(source_path + service_resource_file, 'ServiceResource', output_path + service_resource_file)
    add_external_id.run(source_path + service_territory_file, 'ServiceTerritory', output_path + service_territory_file)
    add_external_id.run(source_path + time_slot_file, 'TimeSlot', output_path + time_slot_file)
    add_external_id.run(source_path + user_file, 'User', output_path + user_file)
    add_external_id.run(source_path + work_order_file, 'WorkOrder', output_path + work_order_file)
    add_external_id.run(source_path + work_type_file, 'WorkType', output_path + work_type_file)


    # generate product consumed
    product_consumed_gen.run(batch_id, output_path + product_consumed_file, output_path + product_consumed_file,
                             output_path + pricebook_entry_file, output_path + work_order_file)

    # generate assigned resources
    assigned_resource_gen.run(batch_id, output_path + assigned_resource_file, output_path + assigned_resource_file,
                              output_path + service_resource_file, output_path + service_appointment_file)

    # generate service appointments
    delta = service_appointment_gen.run(batch_id, output_path + service_appointment_file, output_path + service_appointment_file,
                                output_path + account_file, output_path + service_resource_file,
                                output_path + service_territory_file, output_path + work_order_file, today_datetime)

    assigned_resource_gen.updateCreatedDate(output_path + assigned_resource_file, output_path + assigned_resource_file,
                                            output_path + service_appointment_file, today_datetime)

    # generate resource absences
    resource_absence_gen.run(batch_id, output_path + resource_absence_file, output_path + resource_absence_file,
                             output_path + service_resource_file, delta)

    # generate work orders
    work_order_gen.run(batch_id, output_path + work_order_file, output_path + work_order_file, output_path + case_file,
                       output_path + account_file, output_path + work_type_file, output_path + service_appointment_file,
                       today_datetime)

    # generate time slots
    #time_slot_gen.run(batch_id, output_path + time_slot_file, output_path + time_slot_file,
    #                  output_path + operating_hours_file, today_datetime)

    # generate service resources
    service_resource_gen.run(batch_id, output_path + service_resource_file, output_path + service_resource_file,
                             output_path + user_file)

    # generate cases
    case_gen.run(batch_id, output_path + case_file, output_path + case_file, output_path + account_file)

    # generate accounts
    account_gen.run(batch_id, output_path + account_file, output_path + account_file)

    # generate work types
    work_type_gen.run(batch_id, output_path + work_type_file, output_path + work_type_file)

    # generate users
    user_gen.run(batch_id, output_path + user_file, output_path + user_file, source_path + profile_file)

    # generate service territories
    #service_territory_gen.run(batch_id, output_path + service_territory_file, output_path + service_territory_file,
    #                          output_path + operating_hours_file)

    # generate operating hours
    #operating_hours_gen.run(batch_id, output_path + operating_hours_file, output_path + operating_hours_file)

    # generate pricebook entries
    pricebook_entry_gen.run(batch_id, output_path + pricebook_entry_file, output_path + pricebook_entry_file,
                            output_path + product_file)

    # generate product
    product_gen.run(batch_id, output_path + product_file, output_path + product_file)

    product_consumed_gen.update(output_path + product_consumed_file, output_path + product_consumed_file,
                                output_path + work_order_file)

    # copy all files to the latest folder
    latest_output_path = 'fsl/data/output/latest/'

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(latest_output_path):
        os.makedirs(latest_output_path)

    copy_data_file.run(output_path + product_consumed_file, latest_output_path + product_consumed_file)
    copy_data_file.run(output_path + assigned_resource_file, latest_output_path + assigned_resource_file)
    copy_data_file.run(output_path + service_appointment_file, latest_output_path + service_appointment_file)
    copy_data_file.run(output_path + resource_absence_file, latest_output_path + resource_absence_file)
    copy_data_file.run(output_path + work_order_file, latest_output_path + work_order_file)
    #copy_data_file.run(output_path + time_slot_file, latest_output_path + time_slot_file)
    copy_data_file.run(output_path + service_resource_file, latest_output_path + service_resource_file)
    copy_data_file.run(output_path + case_file, latest_output_path + case_file)
    copy_data_file.run(output_path + account_file, latest_output_path + account_file)
    copy_data_file.run(output_path + work_type_file, latest_output_path + work_type_file)
    copy_data_file.run(output_path + user_file, latest_output_path + user_file)
    #copy_data_file.run(output_path + service_territory_file, latest_output_path + service_territory_file)
    #copy_data_file.run(output_path + operating_hours_file, latest_output_path + operating_hours_file)
    copy_data_file.run(output_path + pricebook_entry_file, latest_output_path + pricebook_entry_file)
    copy_data_file.run(output_path + product_file, latest_output_path + product_file)

if __name__ == "__main__":
    # execute only if running as a script
    run()
