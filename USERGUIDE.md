# Installation

### Python:
- Make sure that python3 is installed on your computer
- Also make sure that python is located as a path in your environment variables

### Install virtualenv:
- Type `pip install virtualenv`

### Create a virtual environment (only done once):
- Navigate to directory root
- Type `virtualenv env`

**Here is where different operating systems require different commands.**
- [Windows Installation](#windows)
- [Linux/Mac Installation](#linux-or-mac)

## LINUX or MAC

### Install all dependencies:
- Navigate to the main project folder (*'220 cowboy'*)
- Activate environment.
	- Type `source env/bin/activate`
- Type `python3 install.py` to install libraries

***The operation below assumes you are inside of the activated environment***

### To run the application:
- `python3 run.py`
- If you would like the web view, type `web` in the console that appears

## WINDOWS

### Install all dependencies:
- Navigate to the main project folder (*'220 cowboy'*)
- Activate environment.
	- Type `env\Scripts\activate`
- Type `python install.py` to install libraries

***The operation below assumes you are inside of the activated environment***

### To run the application:
- python run.py
- If you would like the web view, type 'web' in the console that appears

# Commands

## Graphical Interface
A graphical interface exists which allows you to do everything the command line interface does, as well as click and drag classes to give them position and create a useful UML diagram.

*Use the 'web' command to open this interface type in your browser.*

### Themes
Four default themes control the color scheme of your graphical diagram. If you wish to create your own, take a look at the existing "stylesheets" within app_package/static/css/themes and make your own theme! Adding a stylesheet to this folder will automatically show up in the menu within the navigation sidebar.

## Class

- add
	- Accepts a single class name OR a list separated by commas and adds them to the database.
	- Usage: add <class_name1>, <class_name2>, ... , <class_nameN>

- delete
	- Accepts a single class name OR a list separated by commas and removes them from the database.
	- Usage: delete <class_name1>, <class_name2>, ... , <class_nameN>
- edit
	- Accepts a single class name followed by a replacement name, separated by commas, and changes instances of old name in database with new name.
	- Usage: edit <old_name>, <new_name>
- list
	- Lists every class in the database.
	- Usage: list
- clear
	- Clears all existing classes from the database.
	- Usage: clear
- export
	- Saves an image of the current state of the database to the requested file.
	- Usage: export <file_location>
	    
## Attributes

- addAttr
	- Accepts a single class name and attribute type followed by a list of attribute names separated by commas and adds them to the class.
	- Usage: addAttr <class_name>, <field/method>, <attribute1>, <attribute2>, ... , <attributeN>
- delAttr
	- Accepts a single class name followed by a list of attribute names separated by commas and removes them from the class.
	- Usage: delAttr <class_name>, <attribute1>, <attribute2>, ... , <attributeN>
- editAttr
	- Accepts a single class name followed by an existing attribute within and a new name which will replace said attribute in the class, all separated by commas.
	- Usage: editAttr <class_name>, <old_attribute>, <new_attribute>
	
## Relationships

- addRel
	- Accepts a single 'from' class name and relationship type followed by a list of 'to' class names separated by commas and adds these relationships to the database.
	- Usage: addRel <class_name>, <relationship_type>, <relationship1>, <relationship2>, ... , <relationshipN>
	- Valid relationship types: agg, comp, gen, none
- delRel
	- Accepts a single 'from' class name followed by a list of 'to' class names separated by commas and removes these relationships from the database.
	- Usage: delRel <class_name>, <relationship1>, <relationship2>, ... , <relationshipN>
	
## Other Commands

- help
	- List available commands with "help" or detailed help with "help cmd". 
	- Usage: help <command_name> 
- exit
	- Exits the UML shell.
	- Usage: exit
- load
	- Loads the contents of a previously saved diagram into the database.
	- Usage: load <file_location>
- save
	- Saves the contents of the database into a requested file.
	- Usage: save <file_location>
- undo
	- Reverses your last action. Optionally provide amount.
	- Usage: undo <# of undo's>
- redo
	- Reverse of undo.  Will execute undone command again.
	- Usage: redo
- web
	- Starts the web app in the user's default browser.
	- Usage: web
	
## Future Commands

### Not implemented at this time, but possibly in the future

- playback
	- Playback commands from a file:  PLAYBACK rose.cmd
- record
	- Save future commands to filename:  RECORD rose.cmd

# Advanced
Database contents are saved and loaded using the JSON file format. It is entirely legal to edit an existing save file with other data and load that data into the system. Just be careful! The JSON must adhere to the specific format of a save file to be properly loaded.