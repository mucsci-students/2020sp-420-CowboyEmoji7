import cmd
from app_package.core_func import (core_save, core_load, core_parse)
from app_package.memento.func_objs import add_class, delete_class, edit_class, add_attr, del_attr, edit_attr, add_rel, del_rel
from app_package.models import Class, Attribute, Relationship
from app_package import app, cmd_stack, db
import webbrowser
import json
import readline

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
    
    def complete_delete(self, text, line, begidx, endidx):
        """Provides tab completion data for delete"""
        btext = core_parse(line[7:])[-1]
        allClasses = Class.query.all()
        ClassNames = []
        for Klass in allClasses:
            if Klass.name.startswith(btext):
                tokens = btext.split(" ")
                classTokens = Klass.name.split(" ")
                
                while tokens[0] == classTokens[0]:
                    tokens.pop(0)
                    classTokens.pop(0)
                    
                ClassNames.append(" ".join(classTokens))
                
        return ClassNames

    def do_edit(self, args):
        """Accepts a single class name followed by a replacement name, separated by commas, and changes instances of old name in database with new name.
    Usage: edit <old_name>, <new_name>
    """
        argList = core_parse(args)
        if len(argList) == 2:
            old_name = argList.pop(0)
            new_name = argList.pop(0)
            editCmd = edit_class(old_name, new_name)
            if cmd_stack.execute(editCmd):
                print('ERROR: Unable to update class \'' + old_name + '\' to \'' + new_name + '\'')
            else:
                print('Successfully updated class \'' + old_name + '\' to \'' + new_name + '\'')
        else:
            print("Usage: edit <old_name>, <new_name>")

    def complete_edit(self, text, line, begidx, endidx):
        """Provides tab completion data for edit"""
        allClasses = Class.query.all()
        ClassNames = []
        for Klass in allClasses:
            if Klass.name.startswith(text):
                ClassNames.append(Klass.name)
        return ClassNames
    
######################################## Attribute level #########################################

    def do_addAttr(self, args):
        """Accepts a single class name and attribute type followed by a list of attribute names separated by commas and adds them to the class.
    Usage: addAttr <class_name>, <field/method>, <attribute1>, <attribute2>, ... , <attributeN>
    """
        argList = core_parse(args)
        if len(argList) > 2:
            class_name = argList.pop(0)
            attr_type = argList.pop(0).lower()
            if not attr_type in ["field", "method"]:
                print('ERROR: Invalid attribute type: ' + attr_type + "\n\tValid attribute types: field, method")
                return
            for attr in argList:
                addAttrCmd = add_attr(class_name, attr, attr_type)
                if cmd_stack.execute(addAttrCmd):
                    print('ERROR: Unable to add ' + attr_type + ' \'' + attr + '\'')
                else:
                    print('Successfully added ' + attr_type + ' \'' + attr + '\'')
        else:
            print("Usage: addAttr <class_name>, <field/method>, <attribute1>, <attribute2>, ... , <attributeN>")
        
    def complete_addAttr(self, text, line, begidx, endidx):
        """Provides tab completion data for addAttr"""
        btext = core_parse(line[7:])[-1]
        allClasses = Class.query.all()
        allClassNames = []
        
        for Klass in allClasses:
            allClassNames.append(Klass.name)
            
        allClassNames.append("field")
        allClassNames.append("method")
        
        ClassNames = []
        for Klass in allClassNames:
            if Klass.startswith(btext):
                tokens = btext.split(" ")
                classTokens = Klass.split(" ")
                
                while tokens[0] == classTokens[0]:
                    tokens.pop(0)
                    classTokens.pop(0)
                    
                
                ClassNames.append(" ".join(classTokens))
                
        return ClassNames

    def do_delAttr(self, args):
        """Accepts a single class name followed by a list of attribute names separated by commas and removes them from the class.
    Usage: delAttr <class_name>, <attribute1>, <attribute2>, ... , <attributeN>
    """
        argList = core_parse(args)
        if len(argList) > 1:
            class_name = argList.pop(0)
            for attr in argList:
                delAttrCmd = del_attr(class_name, attr)
                if cmd_stack.execute(delAttrCmd):
                    print('ERROR: Unable to delete attribute \'' + attr + '\'')
                else:
                    print('Successfully deleted attribute \'' + attr + '\'')
        else:
            print("Usage: delAttr <class_name>, <attribute1>, <attribute2>, ... , <attributeN>")
    
    def complete_delAttr(self, text, line, begidx, endidx):
        """Provides tab completion data for delAttr"""
        bline = core_parse(line[8:])
        btext = bline[-1]
        possibleMatches = []
        
        if len(bline) < 2:
            allClasses = Class.query.all()
            for Klass in allClasses:
                possibleMatches.append(Klass.name)
        else:
            allAttrs = Attribute.query.filter(bline[0] == Attribute.class_name).all()
            for Attr in allAttrs:
                possibleMatches.append(Attr.attribute)
        
        Matches = []
        for PM in possibleMatches:
            if PM.startswith(btext):
                tokens = btext.split(" ")
                PMTokens = PM.split(" ")
                
                while tokens[0] == PMTokens[0]:
                    tokens.pop(0)
                    PMTokens.pop(0)
                    
                
                Matches.append(" ".join(PMTokens))
                
        return Matches

    def do_editAttr(self, args):
        """Accepts a single class name followed by an existing attribute within and a new name which will replace said attribute in the class, all separated by commas.
    Usage: editAttr <class_name>, <old_attribute>, <new_attribute>
    """
        argList = core_parse(args)
        if len(argList) == 3:
            class_name = argList.pop(0)
            old_name = argList.pop(0)
            new_name = argList.pop(0)
            editAttrCmd = edit_attr(class_name, old_name, new_name)
            if cmd_stack.execute(editAttrCmd):
                print('ERROR: Unable to update attribute \'' + old_name + '\' to \'' + new_name + '\'')
            else:
                print('Successfully updated attribute \'' + old_name + '\' to \'' + new_name + '\'')
        else:
            print("Usage: editAttr <class_name>, <old_attribute>, <new_attribute>")
    
    def complete_editAttr(self, text, line, begidx, endidx):
        """Provides tab completion data for editAttr"""
        bline = core_parse(line[8:])
        btext = bline[-1]
        possibleMatches = []
        
        if len(bline) < 2:
            allClasses = Class.query.all()
            for Klass in allClasses:
                possibleMatches.append(Klass.name)
        elif len(bline) == 2:
            allAttrs = Attribute.query.filter(bline[0] == Attribute.class_name).all()
            for Attr in allAttrs:
                possibleMatches.append(Attr.attribute)
        
        Matches = []
        for PM in possibleMatches:
            if PM.startswith(btext):
                tokens = btext.split(" ")
                PMTokens = PM.split(" ")
                
                while tokens[0] == PMTokens[0]:
                    tokens.pop(0)
                    PMTokens.pop(0)
                    
                
                Matches.append(" ".join(PMTokens))
                
        return Matches

########################################## Relationship level ########################################

    def do_addRel(self, args):
        """Accepts a single 'from' class name and relationship type followed by a list of 'to' class names separated by commas and adds these relationships to the database.
    Usage: addRel <class_name>, <relationship type>, <relationship1>, <relationship2>, ... , <relationshipN>
        Valid relationship types: agg, comp, gen, none
    """
        argList = core_parse(args)
        if len(argList) > 2:
            class_name = argList.pop(0)
            rel_type = argList.pop(0).lower()
            if not rel_type in ["agg", "comp", "gen", "none"]:
                print('ERROR: Invalid relationship type: ' + rel_type + "\n  Valid relationship types: agg, comp, gen, none")
                return
            for rel in argList:
                addRelCmd = add_rel(class_name, rel, rel_type)
                if cmd_stack.execute(addRelCmd):
                    print('ERROR: Unable to add relationship from \'' + class_name + '\' to \'' + rel + '\' of type \'' + rel_type + '\'')
                else:
                    print('Successfully added relationship from \'' + class_name + '\' to \'' + rel + '\' of type \'' + rel_type + '\'')
        else:
            print("Usage: addRel <class_name>, <relationship type>, <relationship1>, <relationship2>, ... , <relationshipN>\n  Valid relationship types: agg, comp, gen, none")

    def complete_addRel(self, text, line, begidx, endidx):
        """Provides tab completion data for addRel"""
        btext = core_parse(line[7:])[-1]
        allClasses = Class.query.all()
        allClassNames = []
        
        for Klass in allClasses:
            allClassNames.append(Klass.name)
            
        allClassNames.append("agg")
        allClassNames.append("comp")
        allClassNames.append("gen")
        allClassNames.append("none")
        
        ClassNames = []
        for Klass in allClassNames:
            if Klass.startswith(btext):
                tokens = btext.split(" ")
                classTokens = Klass.split(" ")
                
                while tokens[0] == classTokens[0]:
                    tokens.pop(0)
                    classTokens.pop(0)
                    
                
                ClassNames.append(" ".join(classTokens))
                
        return ClassNames
    
    def do_delRel(self, args):
        """Accepts a single 'from' class name followed by a list of 'to' class names separated by commas and removes these relationships from the database.
    Usage: delRel <class_name>, <relationship1>, <relationship2>, ... , <relationshipN>
    """
        argList = core_parse(args)
        if len(argList) > 1:
            class_name = argList.pop(0)
            for rel in argList:
                delRelCmd = del_rel(class_name, rel)
                if cmd_stack.execute(delRelCmd):
                    print('ERROR: Unable to delete relationship from \'' + class_name + '\' to \'' + rel + '\'')
                else:
                    print('Successfully deleted relationship from \'' + class_name + '\' to \'' + rel + '\'')
        else:
            print("Usage: delRel <class_name>, <relationship1>, <relationship2>, ... , <relationshipN>")
            
    def complete_delRel(self, text, line, begidx, endidx):
        """Provides tab completion data for delRel"""
        bline = core_parse(line[7:])
        btext = bline[-1]
        possibleMatches = []
        
        if len(bline) < 2:
            allClasses = Class.query.all()
            for Klass in allClasses:
                possibleMatches.append(Klass.name)
        else:
            allRels = Relationship.query.filter(bline[0] == Relationship.from_name).all()
            for Rel in allRels:
                possibleMatches.append(Rel.to_name)
        
        Matches = []
        for PM in possibleMatches:
            if PM.startswith(btext):
                tokens = btext.split(" ")
                PMTokens = PM.split(" ")
                
                while tokens[0] == PMTokens[0]:
                    tokens.pop(0)
                    PMTokens.pop(0)
                    
                
                Matches.append(" ".join(PMTokens))
                
        return Matches

#################################### Other ############################################

    def do_web(self, args):
        """Starts the web app in the user's default browser.
    Usage: web
    """
        webbrowser.open_new_tab("http://127.0.0.1:5000")
        app.run(port=5000, debug=False)

    def do_undo(self, args):
        """Reverses your last action. Optionally provide amount.
    Usage: undo <# of undo's>
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
                listStrFields = '  > Fields:'
                showFields = False
                for attr in attributes:
                    if attr.attr_type == "field":
                        showFields = True
                        listStrFields += (" " + attr.attribute + ",")
                listStrFields = listStrFields[0:-1] + '\n'
                if showFields:
                    listStr += listStrFields
                    
                listStrMethods = '  > Methods:'
                showMethods = False
                for attr in attributes:
                    if attr.attr_type == "method":
                        showMethods = True
                        listStrMethods += (" " + attr.attribute + ",")
                listStrMethods = listStrMethods[0:-1] + '\n'
                if showMethods:
                    listStr += listStrMethods
            
        relationships = Relationship.query.order_by(Relationship.from_name).all()
        listStr += "Relationships:\n"
        for rel in relationships:
            listStr += "  " + rel.from_name + " -> " + rel.to_name + " (" + rel.rel_type + ")\n"
      
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
    db.create_all()
    replShell().cmdloop()
