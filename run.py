import cmd
from app_package.core_func import core_add, core_delete
from app_package.models import Class
from app_package import app


class replShell(cmd.Cmd):
    intro = 'Welcome to the UML editor shell.   Type help or ? to list commands.\n'
    prompt = '(UML): '
    file = None

    def do_web(self, args):
        'Starts the web app'
        app.run(debug=False)

    def do_add(self, args):
        """Accepts a single class name OR a list separated by spaces and adds them to the database
    ex: add dog cat fish  <-- will add all three classes to database"""
        argList = args.split()
        if argList:
            for name in argList:
                if core_add(name):
                    print('ERROR: Unable to add Class \'' + name + '\'')
                else:
                    print('Successfully added class \'' + name + '\'')
        else:
            print("Please provide a class name")

    def do_delete(self, args):
        """Accepts a single class name OR a list separated by spaces and removes them from the database
    ex: delete dog cat fish  <-- will delete all three classes from database"""
        argList = args.split()
        if argList:
            for name in argList:
                if core_delete(name):
                    print('ERROR: Unable to delete Class \'' + name + '\'')
                else:
                    print('Successfully deleted class \'' + name + '\'')
        else:
            print("Please provide a class name")

    def do_list(self, args):
        'Lists every class in the database'
        classes = Class.query.order_by(Class.date_created).all()
        listStr = ""

        if not classes:
            print("No Classes")

        for classObj in classes:
            # Code in if else prevents a comma from comming after the last element
            if classObj == classes[-1]:
                listStr += classObj.name
            else:
                listStr += (classObj.name + ", ")
        
        print(listStr)

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
