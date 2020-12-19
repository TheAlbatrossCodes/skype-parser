import json
import re
from bs4 import BeautifulSoup

def type_parser(msg_type):
    valid_msg_types = {
                'Event/Call': '***---a call took place---***',
                'Poll' : '***---created a poll---***',
                'RichText/Media_Album' : '***---sent an album of images---***',
                'RichText/Media_AudioMsg': '***---sent a voice message---***',
                'RichText/Media_CallRecording': '***---sent a call recording---***',
                'RichText/Media_Card': '***---sent a media card---***',
                'RichText/Media_FlikMsg': '***---sent a moji---***',
                'RichText/Media_GenericFile': '***---file---***',
                'RichText/Media_Video': '***s---ent a video message---***',
                'RichText/UriObject': '***---sent a photo---***',
                'RichText/ScheduledCallInvite':'***---scheduled a call---***',
                'RichText/Location':'***---sent a location---***',
                'RichText/Contacts':'***---sent a contact---***',
                }
    try:
        return valid_msg_types[msg_type]
    except KeyError:
        return '***--- sent a ' + msg_type + '---***'
        
    

def content_parser(msg_content):
    soup = BeautifulSoup(msg_content)
    return soup.get_text()

with open('messages.json', encoding='utf-8') as f:
    main_file = json.load(f)

display_name = input('Please enter your desired display name: ')
user_id = main_file['userId']
export_date = main_file['exportDate'].replace('T', '@')
no_of_conversations = len(main_file['conversations'])


ids = []
id_to_display_name = {user_id:str(display_name)}
messages_with_id = {}

# get general data
for i in range(no_of_conversations):
    ids.append(main_file['conversations'][i]['id'])
    id_to_display_name[ids[i]] = main_file['conversations'][i]['displayName']
    messages_with_id[ids[i]] = main_file['conversations'][i]['MessageList']


# extract the really good info
message_box = {}
for i in ids:
    no_of_messages = len(messages_with_id[i])
    message_content={}
    for j in reversed(range(no_of_messages)):
        msg_timestamp = messages_with_id[i][j]['originalarrivaltime']
        msg_date = msg_timestamp.split('T')[0]
        msg_time = msg_timestamp.split('T')[1].split('.')[0]

        msg_from = messages_with_id[i][j]['from']
        msg_content = messages_with_id[i][j]['content']
        msg_type = messages_with_id[i][j]['messagetype']
        if msg_type != 'RichText':
            msg_content = type_parser(msg_type)
        

    
        message_content[msg_timestamp] = "[" + msg_time + "] " + id_to_display_name[msg_from] + ": " + msg_content
    
    message_box[i] = message_content

for person in ids:
    compiled_message =''
    date = set([])
    for j in list(message_box[person].keys()):
        d = j.split('T')[0]
        if d not in date:
            date.add(d)
            compiled_message +="\n----------Convo On " + str(d) + "----------\n"    
        compiled_message += message_box[person][j] + '\n'
    parsed_content = content_parser(compiled_message)
    parsed_content = re.sub(r'\[[+-]?\d+(?:\.\d+)?\]', 'In response to this message: \n', parsed_content)
    print(parsed_content)
