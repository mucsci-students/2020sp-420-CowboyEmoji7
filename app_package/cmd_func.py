"""
- Contains core controller functionality to connect cmd commands to core_func functions
- Every function within this class MUST:
    - Accept a list as an argument (you do not need to use it)
    - return a List of strings
        - every string in this list will be printed to a new line in the console
        - Even if only one string is returned, it still must be in a list
"""
from app_package.core_func import core_add, core_delete
from app_package.models import ClassSchema
from app_package import app


def cmd_start_website(argList):
    """Starts the web app"""
    app.run(debug=False)


def cmd_add(argList):
    """Accepts a single class name OR a list separated by spaces and adds them to the database
        ex: add dog cat fish  <-- will add all three classes to database"""
    returnStrList = []
    if argList:
        for name in argList:
            if core_add(name):
                returnStrList.append('ERROR: Unable to add Class \'' + name + '\'')
            else:
                returnStrList.append('Successfully added class \'' + name + '\'')
    else:
        returnStrList.append("Please provide a class name")
    return returnStrList


def cmd_delete(argList):
    """Accepts a single class name OR a list separated by spaces and removes them from the database
        ex: delete dog cat fish  <-- will delete all three classes from database"""
    returnStrList = []
    if argList:
        for name in argList:
            if core_delete(name):
                returnStrList.append('ERROR: Unable to delete Class \'' + name + '\'')
            else:
                returnStrList.append('Successfully deleted class \'' + name + '\'')
    else:
        returnStrList.append("Please provide a class name")
    return returnStrList


def cmd_list_classes(argList):
    """Lists every class in the database"""
    classes = ClassSchema.query.order_by(ClassSchema.date_created).all()
    classList = []
    listStr = ""

    if not classes:
        listStr += "No Classes"

    for classObj in classes:
        listStr += (classObj.name + ", ")
    
    classList.append(listStr)
    return classList
