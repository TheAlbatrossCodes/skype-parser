import json, re, sys
try:
    from bs4 import BeautifulSoup
    beautifulsoup_imported = True
except ImportError:
    beautifulsoup_imported = False
    print('\nBeautifulSoup is not installed on your system...')
    print('\nAs a result, the parsed files will NOT look desirable or pretty &')
    print('\nwill have weird symbols etc. in them.')
    print("\nYou can install BeautifulSoup using:\n")
    print('\t\t pip install beautifulsoup4 ')
    print('Continuing without it for now...')

def main():
    # take the json file as input
    filename = sys.argv[-1]

    # open the skype json file
    with open(filename, encoding='utf-8') as f:
        main_file = json.load(f)

    # map from user's skype username to display name
    display_name = input('In the logs, your name should be displayed as: ')

    # find the user's skype username & general metadata
    user_id = main_file['userId'] 
    export_date, export_time = timestamp_parser(main_file['exportDate'])
    no_of_conversations = len(main_file['conversations'])

    # store the usernames of everyone the user has chatted with and map to their prettier display name
    ids = []
    id_to_display_name = {user_id:str(display_name)}  # for now map your username to display name
    export_file_name = {}  # the name we use for the chat log file
    messages_with_id = {}

    # get general data and store chats with each username in a dict
    for i in range(no_of_conversations):
        # find usernames of those you chatted with and do the actual mapping
        ids.append(main_file['conversations'][i]['id'])
        d_name = main_file['conversations'][i]['displayName']
        if d_name is None:
            id_to_display_name[ids[i]] = ids[i].split(':')[1]
            export_file_name[ids[i]] = "[{}]-{}.txt".format(export_date, ids[i].split(':')[1])
        else:
            id_to_display_name[ids[i]] = d_name
            export_file_name[ids[i]] = "[{}]-{}({}).txt".format(export_date, d_name, ids[i].split(':')[1])

        messages_with_id[ids[i]] = main_file['conversations'][i]['MessageList']


    # extract the good info from the messages
    message_box = {}
    for i in ids:
        no_of_messages = len(messages_with_id[i])
        message_content={}
        # reverse it because we want messages to show up chronologically
        for j in reversed(range(no_of_messages)):
            msg_timestamp = messages_with_id[i][j]['originalarrivaltime']
            msg_time = msg_timestamp.split('T')[1].split('.')[0]
            msg_from = messages_with_id[i][j]['from']
            msg_content = messages_with_id[i][j]['content']
            msg_type = messages_with_id[i][j]['messagetype']

            # map the weirder message types to explanatory text 
            if msg_type != 'RichText':
                msg_content = type_parser(msg_type)

            # construct how each individual message is going to look like
            message_content[msg_timestamp] = "[" + msg_time + "] " + id_to_display_name[msg_from] + ": " + msg_content

        # now we have a dict whose key are the ids and it's content are messages displayed the way we want
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
        if beautifulsoup_imported:
            parsed_content = content_parser(compiled_message)
        # display quotes better and have them make more sense
        parsed_content = re.sub(r'\[[+-]?\d+(?:\.\d+)?\]', '\n\t*** Quoting the following message: ***\n\t', parsed_content)
        parsed_content = re.sub(r'\<\<\<', '\t*** And responding with: ***\n\t', parsed_content)

        with open(export_file_name[person], 'w+', encoding='utf-8') as f:
            f.write(parsed_content)


def type_parser(msg_type):
    # map message types to their true meaning, saving us useless strings/urls
    valid_msg_types = {
                'Event/Call': '***A call started/ended***',
                'Poll' : '***Created a poll***',
                'RichText/Media_Album' : '***Sent an album of images***',
                'RichText/Media_AudioMsg': '***Sent a voice message***',
                'RichText/Media_CallRecording': '***Sent a call recording***',
                'RichText/Media_Card': '***Sent a media card***',
                'RichText/Media_FlikMsg': '***Sent a moji***',
                'RichText/Media_GenericFile': '***Sent a file***',
                'RichText/Media_Video': '***Sent a video message***',
                'RichText/UriObject': '***Sent a photo***',
                'RichText/ScheduledCallInvite':'***Scheduled a call***',
                'RichText/Location':'***Sent a location***',
                'RichText/Contacts':'***Sent a contact***',
                }
    try:
        return valid_msg_types[msg_type]
    except KeyError:
        return '***Sent a ' + msg_type + '***'


def content_parser(msg_content):
    if beautifulsoup_imported:
    # use beautifulsoup to clean the weird xml stuff in the json
        soup = BeautifulSoup(msg_content, 'lxml')
        return soup.get_text()
    else:
        pass


def timestamp_parser(timestamp):
    # skype timestamp has date and time up to the milisecond
    # we'd like to seperate the two and create a better looking version
    date = timestamp.split('T')[0]
    time = timestamp.split('T')[1].split('.')[0]
    return str(date), str(time)


def banner_constructor(display_name, person, export_date, export_time, timestamp):
    # create a banner on the top of each exported file, showing the general metadata
    first_conv_date, first_conv_time = timestamp_parser(timestamp[0])
    last_conv_date, last_conv_time = timestamp_parser(timestamp[-1])
    conv_with = "Conversation with: {} ({})\n".format(display_name, person)
    export_on = "Exported on: {}, at: {}\n".format(export_date, export_time)
    conv_from = "Conversations From: {}, at: {}\n".format(first_conv_date, first_conv_time)
    conv_to = "                To: {}, at: {}\n".format(last_conv_date, last_conv_time)
    disclaimer = "***** All times are in GMT *****\n"
    return conv_with + export_on + conv_from + conv_to + disclaimer

if __name__ == "__main__":
    main()
