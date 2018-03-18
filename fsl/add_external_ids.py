import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fsl import add_external_id

add_external_id.run('data/input/Account.csv', 'W_FSL_Account', 'data/output/Account.csv')
add_external_id.run('data/input/AssignedResource.csv', 'W_FSL_AssignedResource', 'data/output/AssignedResource.csv')
add_external_id.run('data/input/Case.csv', 'W_FSL_Case', 'data/output/Case.csv')
add_external_id.run('data/input/OperatingHours.csv', 'W_FSL_OperatingHours', 'data/output/OperatingHours.csv')
add_external_id.run('data/input/PricebookEntry.csv', 'W_FSL_PricebookEntry', 'data/output/PricebookEntry.csv')
add_external_id.run('data/input/Product2.csv', 'W_FSL_Product', 'data/output/Product2.csv')
add_external_id.run('data/input/ProductConsumed.csv', 'W_FSL_ProductConsumed', 'data/output/ProductConsumed.csv')
add_external_id.run('data/input/ResourceAbsence.csv', 'W_FSL_ResourceAbsence', 'data/output/ResourceAbsence.csv')
add_external_id.run('data/input/ServiceAppointment.csv', 'W_FSL_ServiceAppointment', 'data/output/ServiceAppointment.csv')
add_external_id.run('data/input/ServiceResource.csv', 'W_FSL_ServiceResource', 'data/output/ServiceResource.csv')
add_external_id.run('data/input/ServiceTerritory.csv', 'W_FSL_ServiceTerritory', 'data/output/ServiceTerritory.csv')
add_external_id.run('data/input/TimeSlot.csv', 'W_FSL_TimeSlot', 'data/output/TimeSlot.csv')
add_external_id.run('data/input/User.csv', 'W_FSL_User', 'data/output/User.csv')
add_external_id.run('data/input/WorkOrder.csv', 'W_FSL_WorkOrder', 'data/output/WorkOrder.csv')
add_external_id.run('data/input/WorkType.csv', 'W_FSL_WorkType', 'data/output/WorkType.csv')