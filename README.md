# Skype History Parser
A simple script to create prettier text files from your Skype chat history.

- [How do I just get it to work?](#how-do-i-just-get-it-to-work)
- [Detailed Description](#detailed-description)
  - [Requirements](#requirements)
  - [How do I even export my skype chat history?](#how-do-i-even-export-my-skype-chat-history)
- [TO DO](#to-do)
# How do I just get it to work?
Download `parser.py` and invoke it like so:
```bash
python3 parser.py messages.json
```
Where `messages.json` is the extracted json file you that you get from Skype. This script will create .txt files containing every chat with every user.



If you are not sure how you can get your export from Skype, read the [this section](#how-do-i-export-my-skype-chat-history).

# Detailed Description

Skype JSON Parser is a simple python script that makes preserving chat history from Skype easier.
 
Skype tends be a niche choice for text messages, but for those of who you use it and would like to keep a chat log in pliantext form, this is the tool for you.

Skype's own parser is quite frankly, terrible. It's slow, it produces an ugly HTML that does not even attempt to parse URLS, quotes, emojis, etc. and as I said, it's generally terrible.

This tool will take the JSON file given to you by Skype, and creates .txt files containing every chat with every user.

Basic usage:
```bash
python3 parser.py [-h] [-c] filename

positional arguments:
  filename      The name of the Skype json file you want to parse

optional arguments:
  -h, --help    show this help message and exit
  -c, --choose  Use this flag to choose which convos you want to parse
```

If you invoke the script with `-c` of `--choose` flag, the script will let you choose between the conversations you'd like to export.


## Requirements

 - python version 3.5 and above

- beautifulsoup4 (optional, heavily recommended though)

The script will work without beautiful soup as well, but the parsed files will be much weirder/difficult to read, you'll encounter repeating messages, weird symbols etc. 

## How do I even export my skype chat history?
Follow the instructions [here](https://support.skype.com/en/faq/FA34894/how-do-i-export-my-skype-files-and-chat-history).

Keep in mind that this tool parses your conversations, not your files; so be careful what you export.

Once you have downloaded your exported conversations, you need to untar the downloaded file. This can be done using the tar utility on Linux/Mac or using a program like 7zip on Windows.

The resulting JSON file (usually named 'messages.json' is what this script needs.

# TO DO

- Add untar capability.

