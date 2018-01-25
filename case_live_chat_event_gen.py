import dateutil.parser
import definitions

from data_generator import DataGenerator
from data_generator.formula import fake
from numpy.random import choice


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'CreatedDate__c',
        'EndTime__c',
        'EndedBy__c',
        'Status__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('Owner.External_Id__c', 'Agent.External_Id__c')

    data_gen.add_copy_column('LiveChatTranscript.External_Id__c', 'External_Id__c')
    data_gen.add_copy_column('Time__c', 'CreatedDate__c')

    data_gen.add_constant_column('Type__c', '')
    data_gen.add_constant_column('Detail__c', '')

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()

    type_detail_map = {
        "ChatRequest": "Visitor requested chat.",
        "ChoiceRoute": "Choice chat request routed to all available qualified agents.",
        "CancelNoAgent": "Chat request canceled because no qualifying agents were available.",
        "Accept": "Chat request accepted by agent.",
        "CancelVisitor": "Visitor clicked Cancel Chat.",
        "LeaveAgent": "Agent left chat.",
        "EndAgent": "Agent clicked End Chat.",
        "LeaveVisitor": "Visitor left chat.",
        "EndVisitor": "Visitor clicked End Chat."
    }

    current_count = 1
    new_rows = []
    row_count = len(data_gen.rows)
    for i in range(row_count):
        row = data_gen.rows.pop()
        column_values = data_gen.row_to_column_values(row)

        live_chat = column_values['LiveChatTranscript.External_Id__c']
        agent = column_values['Agent.External_Id__c']
        create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        end_date = dateutil.parser.parse(column_values['EndTime__c'])
        ended_by = column_values['EndedBy__c']
        status = column_values['Status__c']

        # initialize chat request
        new_column_values = {
            'External_Id__c': 'W_LiveChatTranscriptEvent.' + str(current_count),
            'LiveChatTranscript.External_Id__c': live_chat,
            'Agent.External_Id__c': agent,
            'CreatedDate__c': create_date.isoformat(sep=' '),
            'Time__c': create_date.isoformat(sep=' '),
            'Type__c': 'ChatRequest',
            'Detail__c': 'Visitor requested chat.',
            'analyticsdemo_batch_id__c': batch_id
        }
        current_count += 1
        new_rows.append(data_gen.column_values_to_row(new_column_values))

        if status == 'Missed':
            type__c = choice(['CancelVisitor', 'CancelNoAgent'])
            if type__c == 'CancelNoAgent':
                # no agents
                create_date = fake.date_time_between_dates(create_date, end_date)
                new_column_values = {
                    'External_Id__c': 'W_LiveChatTranscriptEvent.' + str(current_count),
                    'LiveChatTranscript.External_Id__c': live_chat,
                    'Agent.External_Id__c': agent,
                    'CreatedDate__c': create_date.isoformat(sep=' '),
                    'Time__c': create_date.isoformat(sep=' '),
                    'Type__c': 'ChoiceRoute',
                    'Detail__c': 'Choice chat request routed to all available qualified agents.',
                    'analyticsdemo_batch_id__c': batch_id
                }
                current_count += 1
                new_rows.append(data_gen.column_values_to_row(new_column_values))

                create_date = fake.date_time_between_dates(create_date, end_date)
                new_column_values = {
                    'External_Id__c': 'W_LiveChatTranscriptEvent.' + str(current_count),
                    'LiveChatTranscript.External_Id__c': live_chat,
                    'Agent.External_Id__c': agent,
                    'CreatedDate__c': create_date.isoformat(sep=' '),
                    'Time__c': create_date.isoformat(sep=' '),
                    'Type__c': type__c,
                    'Detail__c': type_detail_map[type__c],
                    'analyticsdemo_batch_id__c': batch_id
                }
                current_count += 1
                new_rows.append(data_gen.column_values_to_row(new_column_values))

                type__c = choice(['LeaveVisitor', 'EndVisitor'])
                new_column_values = {
                    'External_Id__c': 'W_LiveChatTranscriptEvent.' + str(current_count),
                    'LiveChatTranscript.External_Id__c': live_chat,
                    'Agent.External_Id__c': agent,
                    'CreatedDate__c': end_date.isoformat(sep=' '),
                    'Time__c': end_date.isoformat(sep=' '),
                    'Type__c': type__c,
                    'Detail__c': type_detail_map[type__c],
                    'analyticsdemo_batch_id__c': batch_id
                }
                current_count += 1
                new_rows.append(data_gen.column_values_to_row(new_column_values))
            else:
                # visitor canceled
                new_column_values = {
                    'External_Id__c': 'W_LiveChatTranscriptEvent.' + str(current_count),
                    'LiveChatTranscript.External_Id__c': live_chat,
                    'Agent.External_Id__c': agent,
                    'CreatedDate__c': end_date.isoformat(sep=' '),
                    'Time__c': end_date.isoformat(sep=' '),
                    'Type__c': type__c,
                    'Detail__c': type_detail_map[type__c],
                    'analyticsdemo_batch_id__c': batch_id
                }
                current_count += 1
                new_rows.append(data_gen.column_values_to_row(new_column_values))
        else:
            type__c = 'ChoiceRoute'
            new_column_values = {
                'External_Id__c': 'W_LiveChatTranscriptEvent.' + str(current_count),
                'LiveChatTranscript.External_Id__c': live_chat,
                'Agent.External_Id__c': agent,
                'CreatedDate__c': create_date.isoformat(sep=' '),
                'Time__c': create_date.isoformat(sep=' '),
                'Type__c': type__c,
                'Detail__c': type_detail_map[type__c],
                'analyticsdemo_batch_id__c': batch_id
            }
            current_count += 1
            new_rows.append(data_gen.column_values_to_row(new_column_values))

            type__c = 'Accept'
            create_date = fake.date_time_between_dates(create_date, end_date)
            new_column_values = {
                'External_Id__c': 'W_LiveChatTranscriptEvent.' + str(current_count),
                'LiveChatTranscript.External_Id__c': live_chat,
                'Agent.External_Id__c': agent,
                'CreatedDate__c': create_date.isoformat(sep=' '),
                'Time__c': create_date.isoformat(sep=' '),
                'Type__c': type__c,
                'Detail__c': type_detail_map[type__c],
                'analyticsdemo_batch_id__c': batch_id
            }
            current_count += 1
            new_rows.append(data_gen.column_values_to_row(new_column_values))

            if ended_by == 'Visitor':
                type__c = choice(['LeaveVisitor', 'EndVisitor'])
                new_column_values = {
                    'External_Id__c': 'W_LiveChatTranscriptEvent.' + str(current_count),
                    'LiveChatTranscript.External_Id__c': live_chat,
                    'Agent.External_Id__c': agent,
                    'CreatedDate__c': end_date.isoformat(sep=' '),
                    'Time__c': end_date.isoformat(sep=' '),
                    'Type__c': type__c,
                    'Detail__c': type_detail_map[type__c],
                    'analyticsdemo_batch_id__c': batch_id
                }
                current_count += 1
                new_rows.append(data_gen.column_values_to_row(new_column_values))
            else:
                type__c = choice(['LeaveAgent', 'EndAgent'])
                new_column_values = {
                    'External_Id__c': 'W_LiveChatTranscriptEvent.' + str(current_count),
                    'LiveChatTranscript.External_Id__c': live_chat,
                    'Agent.External_Id__c': agent,
                    'CreatedDate__c': end_date.isoformat(sep=' '),
                    'Time__c': end_date.isoformat(sep=' '),
                    'Type__c': type__c,
                    'Detail__c': type_detail_map[type__c],
                    'analyticsdemo_batch_id__c': batch_id
                }
                current_count += 1
                new_rows.append(data_gen.column_values_to_row(new_column_values))

    data_gen.rows = new_rows

    # apply transformations and write file
    output_columns = [
        'External_Id__c',
        'LiveChatTranscript.External_Id__c',
        'Agent.External_Id__c',
        'Type__c',
        'Detail__c',
        'CreatedDate__c',
        'Time__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run('1', definitions.case_livechat_transcripts, definitions.case_livechat_transcript_events)


