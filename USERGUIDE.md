# Commands

  
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
	- Usage: addRel <class_name>, <relationship type>, <relationship1>, <relationship2>, ... , <relationshipN>
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
