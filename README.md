# Skype History Parser

`skype-parser` is a simple script to create pretty text files from your Skype chat history. This tool can either take in the `.tar` file or the `.json` file given to you by Skype and give you back your entire chat history in `.txt` format (beautifully formatted, too!).

## How do I just get this thing to work?

Download `parser.py` and invoke it like so:

- If you have a `.tar` file:

```bash
python3 parser.py -t your_skype_username_export.tar
```

where `your_skype_username_export.tar` is the `.tar` file your recieved from Skype upon requesting a conversation export.  

- If you have a `.json` file:

```bash
python3 parser.py messages.json
```

where `messages.json` is the extracted `.json` file you that contains your conversation history.  

If you are not sure how you can get your export from Skype, read the [this section](#how-do-i-export-my-skype-chat-history).

## Detailed Description

skype-parser is a simple python script that makes preserving chat history from Skype easier.

Skype tends be a niche choice for text chatting, but for those of you who you use it and would like to keep a chat log in pliin-text form, this is *the* tool to get the job done.

Skype's own parser is quite frankly, terrible. It produces an ugly HTML that is difficult to navigate and is riddled with unparsed XML.

This tool will take the tar/JSON file given to you by Skype, and creates .txt files containing every chat with every user.

Basic usage:

```bash
skype-parser [-h] [-c] [-t] filename

positional arguments:
  filename      The path/name to the Skype json/tar file you want to parse

optional arguments:
  -h, --help    show this help message and exit
  -t, --tar     Use this flag to feed in a .tar file (at your own risk)
  -c, --choose  Use this flag to choose which convos you'd like to parse
```

If you invoke the script **without** the `t` or `--tar` argument, `filename` must be the skype `.json` file.

If you invoke the script **with** the `-t` or `--tar` argument, `filename` must be the `.tar` file that you get from skype.

If you invoke the script with `-c` or `--choose`, it will let you choose between the conversations you'd like to export.

## Requirements

- python version 3.5 and above

- beautifulsoup4 (optional, but recommended)

## How do I even export my skype chat history?

Follow the instructions [here](https://support.skype.com/en/faq/FA34894/how-do-i-export-my-skype-files-and-chat-history).

Keep in mind that this tool parses your conversations, not your files; so be careful what you export.

Once you have downloaded your exported conversations (which is usually in `.tar` format), you can either to untar the downloaded file and use this tool to parse the resulting `.json` file, or you can take the `.tar` file itself and feed it into the script. Either way *should* work.

## TO DO

- Figure out whether we're being a fed a `.json` file or a tarball.
