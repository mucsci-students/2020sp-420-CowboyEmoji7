import cmd
from app_package.core_func import (core_add, core_delete, core_save, core_update,
                                   core_load, core_add_attr, core_del_attr, 
                                   core_update_attr, core_add_rel, core_del_rel)
from app_package.models import Class
from app_package import app
import webbrowser
import json

class replShell(cmd.Cmd):
    intro = 'Welcome to the UML editor shell.   Type help or ? to list commands. \nType web to open web app.\n'
    prompt = '(UML): '
    file = None

    def do_web(self, args):
        """Starts the web app in the user's default browser."""
        webbrowser.open_new_tab("http://127.0.0.1:5000")
        app.run(port=5000, debug=False)

    def do_add(self, args):
        """Accepts a single class name OR a list separated by spaces and adds them to the database
    ex: add dog cat fish  <-- will add all three classes to database"""
        argList = args.split()
        if argList:
            for name in argList:
                if core_add(name):
                    print('ERROR: Unable to add class \'' + name + '\'')
                else:
                    print('Successfully added class \'' + name + '\'')
        else:
            print("Please provide a class name")

    def do_addAttr(self, args):
        """Accepts a single class name followed by a list of attribute names separated by spaces
      and adds them to the database
    ex: addAttr zoo dog cat catDog <-- will add all three attributes to the class "zoo" in database"""
        argList = args.split()
        if len(argList) > 1:
            class_name = argList.pop(0)
            for attr in argList:
                if core_add_attr(class_name, attr):
                    print('ERROR: Unable to add attribute \'' + attr + '\'')
                else:
                    print('Successfully added attribute \'' + attr + '\'')
        else:
            print("Please provide a class name and at least one attribute")

    def do_delAttr(self, args):
        """Accepts a single class name followed by a list of attribute names separated by spaces
      and removes them from the database
    ex: delAttr zoo dog cat catDog <-- will remove all three attributes from the class "zoo" in database"""
        argList = args.split()
        if len(argList) > 1:
            class_name = argList.pop(0)
            for attr in argList:
                if core_del_attr(class_name, attr):
                    print('ERROR: Unable to delete attribute \'' + attr + '\'')
                else:
                    print('Successfully deleted attribute \'' + attr + '\'')
        else:
            print("Please provide a class name and at least one attribute")

    def do_editAttr(self, args):
        """Accepts a single class name followed by an existing attribute within said class and a
      new name which will replace said attribute in the database
    ex: editAttr zoo dog cat <-- will update attribute 'dog' in class 'zoo' with the name 'cat'"""
        argList = args.split()
        if len(argList) > 2:
            class_name = argList.pop(0)
            old_name = argList.pop(0)
            new_name = argList.pop(0)
            if core_update_attr(class_name, old_name, new_name):
                print('ERROR: Unable to update attribute \'' + old_name + '\' to \'' + new_name + '\'')
            else:
                print('Successfully updated attribute \'' + old_name + '\' to \'' + new_name + '\'')
        else:
            print("Please provide a class name, followed by two attribute names")

    def do_addRel(self, args):
        """Accepts a single parent class name followed by a list of child class names separated by spaces
      and adds relationships from parents to children in database
    ex: addRel cat kitten catDog <-- will add both relationships to the class "cat" in database"""
        argList = args.split()
        if len(argList) > 1:
            class_name = argList.pop(0)
            for rel in argList:
                if core_add_rel(class_name, rel):
                    print('ERROR: Unable to add relationship from \'' + class_name + '\' to \'' + rel + '\'')
                else:
                    print('Successfully added relationship from \'' + class_name + '\' to \'' + rel + '\'')
        else:
            print("Please provide a class name and at least one relationship")

    def do_delRel(self, args):
        """Accepts a single parent class name followed by a list of child class names separated by spaces
      and removes relationships from parents to children in database
    ex: delRel cat kitten catDog <-- will delete both relationships from the class "cat" in database"""
        argList = args.split()
        if len(argList) > 1:
            class_name = argList.pop(0)
            for rel in argList:
                if core_del_rel(class_name, rel):
                    print('ERROR: Unable to delete relationship from \'' + class_name + '\' to \'' + rel + '\'')
                else:
                    print('Successfully deleted relationship from \'' + class_name + '\' to \'' + rel + '\'')
        else:
            print("Please provide a class name and at least one relationship")

    def do_delete(self, args):
        """Accepts a single class name OR a list separated by spaces and removes them from the database
    ex: delete dog cat fish  <-- will delete all three classes from database"""
        argList = args.split()
        if argList:
            for name in argList:
                if core_delete(name):
                    print('ERROR: Unable to delete class \'' + name + '\'')
                else:
                    print('Successfully deleted class \'' + name + '\'')
        else:
            print("Please provide a class name")

    def do_list(self, args):
        """Lists every class in the database"""
        classes = Class.query.order_by(Class.date_created).all()
        listStr = ""

        if not classes:
            print("No Classes")

        for classObj in classes:
            # Code in if else prevents a comma from coming after the last element
            if classObj == classes[-1]:
                listStr += classObj.name
            else:
                listStr += (classObj.name + ", ")
        
        print(listStr)

    def do_save(self, args):
        if len(args.split()) is not 1:
            print("Please provide one file name.")
        else:
            try:
                Jfile = open(args, "w+")
                Jfile.write(core_save())
                print("Successfully saved file as \'" + args + '\'')
            except:
                print("ERROR: Unable to save file as \'" + args + '\'')

    def do_load(self, args):
        if len(args.split()) is not 1:
            print("Please provide one file name.")
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
        'Exits the UML shell'
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
