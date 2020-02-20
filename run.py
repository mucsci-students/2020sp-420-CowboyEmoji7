from app_package.cmd_func import cmd_start_website, cmd_add, cmd_list_classes, cmd_delete

RUN_LOOP = True


def exit_loop(argsList):
    """Exits the application and displays goodbye message"""
    global RUN_LOOP
    RUN_LOOP = False
    return ["Exiting"]


# format is 'cmdname': function_name
cmdDict = {
    "add": cmd_add,
    "delete": cmd_delete,
    "remove": cmd_delete,
    "exit": exit_loop,
    "web": cmd_start_website,
    "list": cmd_list_classes
}


while RUN_LOOP:
    # 'UML: ' is printed before the area where users type
    userInput = input("UML: ")
    tokenInput = userInput.split()

    if tokenInput:
        firstArg = tokenInput.pop(0)
        if firstArg in cmdDict:
            result = cmdDict[firstArg](tokenInput)
            for line in result:
                print("- " + line)
        else:
            print("Unknown Command")
            
