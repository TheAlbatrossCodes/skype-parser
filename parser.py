import json

with open('messages.json', encoding='utf-8') as f:
    main_file = json.load(f)

user_id = main_file['userId']
export_date = main_file['exportDate'].replace('T', '@')
no_of_conversations = len(main_file['conversations'])


ids = []
id_to_display_name = {}
messages_with_id = {}

# get general data
for i in range(no_of_conversations):
    ids.append(main_file['conversations'][i]['id'])
    id_to_display_name[ids[i]] = main_file['conversations'][i]['displayName']
    messages_with_id[ids[i]] = main_file['conversations'][i]['MessageList']

message_box = {}
for i in ids:
    no_of_messages = len(messages_with_id[i])

    for j in range(no_of_messages):
        msg_time = messages_with_id[i][j]['originalarrivaltime']
        msg_from = messages_with_id[i][j]['from']
        msg_content = messages_with_id[i][j]['content']
        msg_type = messages_with_id[i][j]['messagetype']

def type_parser(msg_type):
    valid_msg_types = {'Event/Call': "Call",
                'Poll' : "Poll",
                'RichText': "",
                'RichText/Media_Album' : "Album",
                'RichText/Media_AudioMsg': "Voice Message",
                'RichText/Media_CallRecording': "Call Recording",
                'RichText/Media_Card': "Media Card",
                'RichText/Media_FlikMsg':"FlikMsg",
                'RichText/Media_GenericFile': "File",
                'RichText/Media_Video': "Video",
                'RichText/UriObject': "Photo"}
    return(valid_msg_types[msg_type])
    
def content_parser(msg_content):
    pass

# messages_with = {}
# for convs in range(len(messages)):
#     messages_with[chat_with_id[convs]] = messages[convs]

