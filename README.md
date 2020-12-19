# Skype History Parser
A simple script to create prettier text files from your Skype chat history.

## Description

Skype JSON Parser is a simple python script that makes preserving chat history from Skype easier.
 
Skype tends be a niche choice for text messages, but for those of who you use it and would like to keep a chat log in pliantext form, this is the tool for you.

Skype's own parser is quite frankly, terrible. It's slow, it produces an ugly HTML that does not even attempt to parse URLS, quotes, emojis, etc. and as I said, it's generally terrible.

This tool will take the JSON file given to you by Skype, and creates .txt files containing every chat with every user.




## Requirements
```python
python3
beautifulsoup4
```
## How does the script work?
Download the parser.py and invoke it like so:
```bash
python3 parser.py messages.json
```
Where messages.json is the json file you that you get from Skype. This script will create .txt files containing every chat with every user, plus some other  skype-specific stuff.


If you are not sure how you can get your export from Skype, read the next section.

## But how do I export my skype chat history?
Follow the instructions [here](https://support.skype.com/en/faq/FA34894/how-do-i-export-my-skype-files-and-chat-history).

Keep in mind that this tool parses your conversations, not your files; so be careful what you export.

Once you have downloaded your exported conversations, you need to untar the downloaded file. This can be done using the tar utility on Linux/Mac or using a program like 7zip on Windows.

The resulting JSON file (usually named 'messages.json' is what this script needs.




## TO DO
Give people the choice to export only the convos they want.


