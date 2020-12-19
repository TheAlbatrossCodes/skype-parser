import json
import re
from bs4 import BeautifulSoup

def type_parser(msg_type):
    valid_msg_types = {
                'Event/Call': '***---a call started/ended---***',
                'Poll' : '***---created a poll---***',
                'RichText/Media_Album' : '***---sent an album of images---***',
                'RichText/Media_AudioMsg': '***---sent a voice message---***',
                'RichText/Media_CallRecording': '***---sent a call recording---***',
                'RichText/Media_Card': '***---sent a media card---***',
                'RichText/Media_FlikMsg': '***---sent a moji---***',
                'RichText/Media_GenericFile': '***---sent a file---***',
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


def timestamp_parser(timestamp):
    date = timestamp.split('T')[0]
    time = timestamp.split('T')[1].split('.')[0]
    return str(date), str(time)


def banner_constructor(display_name, person, export_date, export_time, timestamp):
    first_conv_date, first_conv_time = timestamp_parser(timestamps[0])
    last_conv_date, last_conv_time = timestamp_parser(timestamps[-1])
    conv_with = "Conversation with: {} ({})\n".format(display_name, person)
    export_on = "Exported on: {}, at: {}\n".format(export_date, export_time)
    conv_from = "Conversations From: {}, at: {}\n".format(first_conv_date, first_conv_time)
    conv_to = "                To: {}, at: {}\n".format(last_conv_date, last_conv_time)
    disclaimer = "***** All times are in GMT *****\n"
    return conv_with + export_on + conv_from + conv_to + disclaimer


# open the skype json file
with open('messages.json', encoding='utf-8') as f:
    main_file = json.load(f)

# map from user's skype username to display name
display_name = input('Your name should be displayed as: ')

# find the user's skype username
user_id = main_file['userId'] 
export_date, export_time = timestamp_parser(main_file['exportDate'])
no_of_conversations = len(main_file['conversations'])

# store the usernames of everyone user has chatted with and map to their prettier display name
ids = []
id_to_display_name = {user_id:str(display_name)}  # for now map your username to display name
messages_with_id = {}

# get general data and store chats with each username in a dict
for i in range(no_of_conversations):
    # find usernames of those you chatted with and do the actual mapping
    ids.append(main_file['conversations'][i]['id'])

    if main_file['conversations'][i]['displayName'] is None:
        id_to_display_name[ids[i]] = ids[i].split(':')[1]
    else:
        id_to_display_name[ids[i]] = main_file['conversations'][i]['displayName']

    messages_with_id[ids[i]] = main_file['conversations'][i]['MessageList']


# extract the good info from the messages
message_box = {}
for i in ids:
    no_of_messages = len(messages_with_id[i])
    message_content={}
    # reverse it because we want messages to show up chronologically
    for j in reversed(range(no_of_messages)):
        msg_timestamp = messages_with_id[i][j]['originalarrivaltime']
        msg_date = msg_timestamp.split('T')[0]
        msg_time = msg_timestamp.split('T')[1].split('.')[0]

        msg_from = messages_with_id[i][j]['from']
        msg_content = messages_with_id[i][j]['content']
        msg_type = messages_with_id[i][j]['messagetype']
        # map the weirder message types to explanatory text 
        if msg_type != 'RichText':
            msg_content = type_parser(msg_type)
        # construct how each individual message is going to look like
        message_content[msg_timestamp] = "[" + msg_time + "] " + id_to_display_name[msg_from] + ": " + msg_content
    # now we have a dict whose key are the ids and it's content are messages, without the useless stuff
    message_box[i] = message_content

# parse and clean the messages of it's weirder XML style tags and whatnot
for person in ids:
    timestamps = list(message_box[person].keys())
    display_name = str(id_to_display_name[person])
    banner = banner_constructor(display_name, person, export_date, export_time, timestamps)
    compiled_message = banner
    date = set([])
    for j in timestamps:
        d = j.split('T')[0]
        if d not in date:
            date.add(d)
            compiled_message +="\n----------Conversations on " + str(d) + "----------\n"    
        compiled_message += message_box[person][j] + '\n'
    
    # get rid of the weirder skype XML
    parsed_content = content_parser(compiled_message)
    # display quotes better and have them make more sense
    parsed_content = re.sub(r'\[[+-]?\d+(?:\.\d+)?\]', '\n\t*** Quoting the following message: ***\n\t', parsed_content)
    parsed_content = re.sub(r'\<\<\<', '\t*** And responding with: ***\n\t', parsed_content)

    file_name = display_name + ".txt"
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(parsed_content)