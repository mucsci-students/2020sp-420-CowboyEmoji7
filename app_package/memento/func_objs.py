from ..core_func import (core_add, core_delete, core_add_attr, core_update, core_add_attr, core_del_attr, core_update_attr, core_add_rel, core_del_rel)
from ..models import Attribute


class Command:
    """The base class which all commands are a subclass
       All subclasses require these methods"""
    def execute(self):
        pass

    def undo(self):
        return

    def redo(self):
        pass


class add_class(Command):
    """Command class for core_add.  Accepts a class name"""
    className = ''

    def __init__(self, name):
        self.className = name

    def execute(self):
        return core_add(self.className)

    def undo(self):
        return core_delete(self.className)

    def redo(self):
        return core_add(self.className)


class delete_class(Command):
    """Command class for core_delete.  Accepts a class name"""
    className = ''
    attributes = []

    def __init__(self, name):
        self.className = name

    def execute(self):
        self.attributes = Attribute.query.filter(self.className == Attribute.class_name).all()
        return core_delete(self.className)

    def undo(self):
        result = core_add(self.className)
        if result == 0:
            for attr in self.attributes:
                core_add_attr(self.className, attr.attribute)
            
        return result

    def redo(self):
        return core_delete(self.className)


class edit_class(Command):
    """Command class for core_update.  Accepts a class name and a new name"""
    oldClassName = ''
    newClassName = ''

    def __init__(self, oldName, newName):
        self.oldClassName = oldName
        self.newClassName = newName

    def execute(self):
        return core_update(self.oldClassName, self.newClassName)

    def undo(self):
        return core_update(self.newClassName, self.oldClassName)

    def redo(self):
        return core_update(self.oldClassName, self.newClassName)


class add_attr(Command):
    """Command class for core_add_attr.  Accepts a class name and the name of an attribute"""
    className = ''
    attrName = ''

    def __init__(self, className, attrName):
        self.className = className
        self.attrName = attrName

    def execute(self):
        return core_add_attr(self.className, self.attrName)

    def undo(self):
        return core_del_attr(self.className, self.attrName)

    def redo(self):
        return core_add_attr(self.className, self.attrName)


class del_attr(Command):
    """Command class for core_del_attr.  Accepts a class name and the name of an attribute to remove"""
    className = ''
    attrName = ''

    def __init__(self, className, attrName):
        self.className = className
        self.attrName = attrName

    def execute(self):
        return core_del_attr(self.className, self.attrName)

    def undo(self):
        return core_add_attr(self.className, self.attrName)

    def redo(self):
        return core_del_attr(self.className, self.attrName)


class edit_attr(Command):
    """Command class for edit_attr.  Accepts a class name and a new name"""
    className = ''
    oldAttrName = ''
    newAttrName = ''

    def __init__(self, className, oldName, newName):
        self.oldAttrName = oldName
        self.newAttrName = newName

    def execute(self):
        return core_update_attr(self.className, self.oldAttrName, self.newAttrName)

    def undo(self):
        return core_update_attr(self.className, self.newAttrName, self.oldAttrName)

    def redo(self):
        return core_update_attr(self.className, self.oldAttrName, self.newAttrName)


class add_rel(Command):
    """Command class for core_add_rel.  Accepts a class name and the name of the child"""
    parentName = ''
    childName = ''

    def __init__(self, parentName, childName):
        self.parentName = parentName
        self.childName = childName

    def execute(self):
        return core_add_rel(self.parentName, self.childName)

    def undo(self):
        return core_del_rel(self.parentName, self.childName)

    def redo(self):
        return core_add_rel(self.parentName, self.childName)


class del_rel(Command):
    """Command class for core_del_rel.  Accepts a class name and the name of the child"""
    parentName = ''
    childName = ''

    def __init__(self, parentName, childName):
        self.parentName = parentName
        self.childName = childName

    def execute(self):
        return core_del_rel(self.parentName, self.childName)

    def undo(self):
        return core_add_rel(self.parentName, self.childName)

    def redo(self):
        return core_del_rel(self.parentName, self.childName)