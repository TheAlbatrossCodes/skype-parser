import json
import re
import argparse
import tarfile

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP = True
except ImportError:
    BEAUTIFULSOUP = False
    import html

def main():
    args = get_commandline_args()
    # take the json file as input and open the skype json file
    main_file = read_file(args.filename) if not args.tar else read_tarfile(args.filename)

    if not BEAUTIFULSOUP:
        print("\n--- WARNING ---\n")
        print("BeautifulSoup is not installed on your system. "
              "\nIt is safer to use this script with BeautifulSoup "
              "installed.\nYou can install BeautifuSoup using this "
              "command:\n\n\t\t pip install beautifulsoup4\n\n")

    # map from user's skype username to display name
    user_display_name = input('\nIn the logs, your name should be displayed as: ')
    while len(user_display_name.split()) == 0:
        user_display_name = input('\nPlease enter how you want your name to be displayed: ')

    # find the user's skype username & general metadata
    user_id = main_file['userId']
    export_date, export_time = timestamp_parser(main_file['exportDate'])
    no_of_conversations = len(main_file['conversations'])

    # map username of everyone you chatted with to their display name
    ids = []
    id_to_display_name = {user_id:str(user_display_name)}
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

    # if program is run with --choose flag, just iter through the ids selected by the user
    if args.choose:
        ids = id_selector(ids)

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

            # edited messages show up twice, but so do normal messages sent twice
            # so a safe way to get rid of them is as follows
            if msg_content == messages_with_id[i][j-1]['content'] and re.search(r'<e_m.*>',  msg_content):
                msg_content = ('--This user edited the following message at {}, you '
                               'are viewing the edited version--'.format(msg_time))

            # construct how each individual message is going to look like
            message_content[msg_timestamp] = "[" + msg_time + "] " + id_to_display_name[msg_from] + ": " + msg_content

        # this dict will have ids as keys and actual messages as formatted vals
        message_box[i] = message_content

    # parse and clean the messages of it's weirder XML style tags and whatnot
    for person in ids:
        timestamps = list(message_box[person].keys())
        display_name = str(id_to_display_name[person])
        banner = banner_constructor(display_name, person, export_date, export_time, timestamps)
        compiled_message = banner
        date = set([])
        for j in timestamps:
            d, _ = timestamp_parser(j)
            if d not in date:
                date.add(d)
                compiled_message +="\n---------- Conversations on " + str(d) + " ----------\n"
            compiled_message += message_box[person][j] + '\n'

        if BEAUTIFULSOUP:
            # get rid of the weirder skype XML
            pretty_parsed_content = content_parser(compiled_message)
            write_to_file(export_file_name[person], pretty_parsed_content)

        else:
            # no bs4, so we use regex
            compiled_message = tag_stripper(compiled_message)
            write_to_file(export_file_name[person], compiled_message)

    print("\nAll done!")


def get_commandline_args():
    command = argparse.ArgumentParser("parser")
    command.add_argument('filename',
                         help='The path/name to the Skype json file you want to parse')
    command.add_argument('-c', '--choose',
                         action='store_true',
                         help="Use this flag to choose which convos you'd like to parse")
    command.add_argument('-t', '--tar',
                         action='store_true',
                         help='Use this flag to feed in a tar file (at your own risk)')
    args = command.parse_args()
    return args


def read_file(filename):
    with open(filename, encoding='utf-8') as f:
        main_file = json.load(f)
        # exception handling goes here
    return main_file


def read_tarfile(filename):
    # would rather a *.json pattern match implementation
    with tarfile.open(filename) as f:
        # find files inside the tar
        tar_contents = f.getnames()

        # only get the file with .json extension
        pattern = re.compile(r'.*\.json')
        tar_files = list(filter(pattern.match, tar_contents))

        # read that file and assign it to main_file
        main_file = f.extractfile(f.getmember(tar_files[0]))
        main_file = json.load(main_file)
        return main_file


def write_to_file(file_name, parsed_content):
    with open(file_name, 'w+', encoding='utf-8') as f:
        f.write(parsed_content)
        print("Sucessfully parsed {}...".format(file_name))


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
    soup = BeautifulSoup(msg_content, 'lxml')
    text = soup.get_text()
    text = pretty_quotes(text)
    return text


def tag_stripper(text):
    match = re.compile(r'<.*?>')
    text = match.sub('', text)
    text = html.unescape(text)
    text = pretty_quotes(text)
    return text


def pretty_quotes(cleaned_text):
    # display quotes better and have them make more sense
    match = re.compile(r'\[[+-]?\d+(?:\.\d+)?\]')
    cleaned_text= match.sub(r'\n\t*** Quoting the following message: ***\n\t', cleaned_text)
    match = re.compile(r'\<\<\<')
    cleaned_text = match.sub('\t*** And responding with: ***\n\t', cleaned_text)
    return cleaned_text


def timestamp_parser(timestamp):
    # skype timestamp has date and time up to the milisecond
    # we'd like to seperate the two and create a better looking version
    date = timestamp.split('T')[0]
    time = timestamp.split('T')[1].split('.')[0]
    return str(date), str(time)


def id_selector(ids):
    print("You have conversations with the following ids: ")
    valid_selections = {}
    for i in range(len(ids)):
        print('\t{} ----> {}'.format(i+1, ids[i]))
        valid_selections[str(i+1)] = ids[i]

    user_selection = input('Enter the number associated with the chats '
                            'you want to export, separated by a space: ')
    selected_ids = set(user_selection.split())

    while not selected_ids.issubset(set(valid_selections.keys())) or len(selected_ids) == 0:
        user_selection = input('Please enter valid numbers, separated by a space: ')
        selected_ids = set(user_selection.split())

    return [valid_selections[j] for j in selected_ids]


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
