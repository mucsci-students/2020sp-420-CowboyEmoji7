import cmd
from app_package.core_func import (core_add, core_delete, core_save, core_update,
                                   core_load, core_add_attr, core_del_attr, 
                                   core_update_attr, core_add_rel, core_del_rel,
                                   core_parse)
from app_package.memento.func_objs import add_class, delete_class
from app_package.models import Class, Attribute, Relationship
from app_package import app, cmd_stack
import webbrowser
import json


class replShell(cmd.Cmd):
    intro = 'Welcome to the UML editor shell.\nType help or ? to list commands.\nType web to open web app.\n'
    prompt = '(UML): '
    file = None

################################# Class level ############################################

    def do_add(self, args):
        """Accepts a single class name OR a list separated by commas and adds them to the database.
    Usage: add <class_name1>, <class_name2>, ... , <class_nameN>
    """
        argList = core_parse(args)
        if argList:
            for name in argList:
                addCmd = add_class(name)
                if cmd_stack.execute(addCmd):
                    print('ERROR: Unable to add class \'' + name + '\'')
                else:
                    print('Successfully added class \'' + name + '\'')
        else:
            print("Usage: add <class_name1>, <class_name2>, ... , <class_nameN>")

    def do_delete(self, args):
        """Accepts a single class name OR a list separated by commas and removes them from the database.
    Usage: delete <class_name1>, <class_name2>, ... , <class_nameN>
    """
        argList = core_parse(args)
        if argList:
            for name in argList:
                deleteCmd = delete_class(name)
                if cmd_stack.execute(deleteCmd):
                    print('ERROR: Unable to delete class \'' + name + '\'')
                else:
                    print('Successfully deleted class \'' + name + '\'')
        else:
            print("Usage: delete <class_name1>, <class_name2>, ... , <class_nameN>")

    def do_edit(self, args):
        """Accepts a single class name followed by a replacement name, separated by commas, and changes instances of old name in database with new name.
    Usage: edit <old_name>, <new_name>
    """
        argList = core_parse(args)
        if len(argList) == 2:
            old_name = argList.pop(0)
            new_name = argList.pop(0)
            if core_update(old_name, new_name):
                print('ERROR: Unable to update class \'' + old_name + '\' to \'' + new_name + '\'')
            else:
                print('Successfully updated class \'' + old_name + '\' to \'' + new_name + '\'')
        else:
            print("Usage: edit <old_name>, <new_name>")

######################################## Attribute level #########################################

    def do_addAttr(self, args):
        """Accepts a single class name followed by a list of attribute names separated by commas and adds them to the class.
    Usage: addAttr <class_name>, <attribute1>, <attribute2>, ... , <attributeN>
    """
        argList = core_parse(args)
        if len(argList) > 1:
            class_name = argList.pop(0)
            for attr in argList:
                if core_add_attr(class_name, attr):
                    print('ERROR: Unable to add attribute \'' + attr + '\'')
                else:
                    print('Successfully added attribute \'' + attr + '\'')
        else:
            print("Usage: addAttr <class_name>, <attribute1>, <attribute2>, ... , <attributeN>")

    def do_delAttr(self, args):
        """Accepts a single class name followed by a list of attribute names separated by commas and removes them from the class.
    Usage: delAttr <class_name>, <attribute1>, <attribute2>, ... , <attributeN>
    """
        argList = core_parse(args)
        if len(argList) > 1:
            class_name = argList.pop(0)
            for attr in argList:
                if core_del_attr(class_name, attr):
                    print('ERROR: Unable to delete attribute \'' + attr + '\'')
                else:
                    print('Successfully deleted attribute \'' + attr + '\'')
        else:
            print("Usage: delAttr <class_name>, <attribute1>, <attribute2>, ... , <attributeN>")

    def do_editAttr(self, args):
        """Accepts a single class name followed by an existing attribute within and a new name which will replace said attribute in the class, all separated by commas.
    Usage: editAttr <class_name>, <old_attribute>, <new_attribute>
    """
        argList = core_parse(args)
        if len(argList) == 3:
            class_name = argList.pop(0)
            old_name = argList.pop(0)
            new_name = argList.pop(0)
            if core_update_attr(class_name, old_name, new_name):
                print('ERROR: Unable to update attribute \'' + old_name + '\' to \'' + new_name + '\'')
            else:
                print('Successfully updated attribute \'' + old_name + '\' to \'' + new_name + '\'')
        else:
            print("Usage: editAttr <class_name>, <old_attribute>, <new_attribute>")

########################################## Relationship level ########################################

    def do_addRel(self, args):
        """Accepts a single parent class name followed by a list of child class names separated by commas and adds relationships from parents to children in database.
    Usage: addRel <class_name>, <relationship1>, <relationship2>, ... , <relationshipN>
    """
        argList = core_parse(args)
        if len(argList) > 1:
            class_name = argList.pop(0)
            for rel in argList:
                if core_add_rel(class_name, rel):
                    print('ERROR: Unable to add relationship from \'' + class_name + '\' to \'' + rel + '\'')
                else:
                    print('Successfully added relationship from \'' + class_name + '\' to \'' + rel + '\'')
        else:
            print("Usage: addRel <class_name>, <relationship1>, <relationship2>, ... , <relationshipN>")

    def do_delRel(self, args):
        """Accepts a single parent class name followed by a list of child class names separated by commas and removes relationships from parents to children in database.
    Usage: delRel <class_name>, <relationship1>, <relationship2>, ... , <relationshipN>
    """
        argList = core_parse(args)
        if len(argList) > 1:
            class_name = argList.pop(0)
            for rel in argList:
                if core_del_rel(class_name, rel):
                    print('ERROR: Unable to delete relationship from \'' + class_name + '\' to \'' + rel + '\'')
                else:
                    print('Successfully deleted relationship from \'' + class_name + '\' to \'' + rel + '\'')
        else:
            print("Usage: delRel <class_name>, <relationship1>, <relationship2>, ... , <relationshipN>")

#################################### Other ############################################

    def do_web(self, args):
        """Starts the web app in the user's default browser.
    Usage: web
    """
        webbrowser.open_new_tab("http://127.0.0.1:5000")
        app.run(port=5000, debug=False)

    def do_undo(self, args):
        """Reverses your last action.
    Usage: undo
    """
        cmd_stack.undo()
        print('undid action')

    # could add arg for amount, to undo/redo X times in a row
    def do_redo(self, args):
        """Reverse of undo.  Will execute undone command again.
    Usage: redo
    """
        cmd_stack.redo()
        print('redid action')

    def do_list(self, args):
        """Lists every class in the database.
    Usage: list
    """
        classes = Class.query.order_by(Class.date_created).all()
        listStr = ""

        if not classes:
            print("No Classes")

        for classObj in classes:
            # Code in if else prevents a comma from coming after the last element

            listStr += classObj.name + '\n'
            attributes = classObj.class_attributes

            if len(attributes) > 0:
                listStr += '  > Attributes: '
                for attr in attributes:
                    if attr == attributes[-1]:
                        listStr += attr.attribute + '\n'
                    else:
                        listStr += (attr.attribute + ", ")

            relationships = classObj.class_relationships
            if len(relationships) > 0:
                listStr += '  > Children: '
                for rel in relationships:
                    if rel == relationships[-1]:
                        listStr += rel.to_name + '\n'
                    else:
                        listStr += (rel.to_name + ", ")
        
        print(listStr)

    def do_save(self, args):
        """Saves the contents of the database into a requested file.
    Usage: save <file_location>
    """
        if len(args.split()) != 1:
            print("Usage: save <file_location>")
        else:
            try:
                Jfile = open(args, "w+")
                Jfile.write(core_save())
                print("Successfully saved file as \'" + args + '\'')
            except:
                print("ERROR: Unable to save file as \'" + args + '\'')

    def do_load(self, args):
        """Loads the contents of a previously saved diagram into the database.
    Usage: load <file_location>
    """
        if len(args.split()) != 1:
            print("Usage: load <file_location>")
        else:
            try:
                Jfile = open(args, "r")
                if core_load(json.load(Jfile)):
                    print("ERROR: Unable to load file \'" + args + '\'')
                else:
                    print("Successfully loaded file \'" + args + '\'')
            except:
                print("ERROR: Unable to open file \'" + args + '\'')


    def do_exit(self, args):
        """Exits the UML shell.
    Usage: exit
    """
        print('Thank you for using our UML editor')
        self.close()
        return True

    def emptyline(self):
        pass
    
    # ----- record and playback -----
    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')

    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK rose.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())

    def precmd(self, line):
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


if __name__ == '__main__':
    replShell().cmdloop()
