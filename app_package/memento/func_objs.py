from ..core_func import core_add, core_delete, core_add_attr
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
    class_name = ''

    def __init__(self, name):
        self.class_name = name

    def execute(self):
        return core_add(self.class_name)

    def undo(self):
        return core_delete(self.class_name)

    def redo(self):
        return core_add(self.class_name)


class delete_class(Command):
    """Command class for core_delete.  Accepts a class name"""
    class_name = ''
    attributes = []

    def __init__(self, name):
        self.class_name = name

    def execute(self):
        self.attributes = Attribute.query.filter(self.class_name == Attribute.class_name).all()
        return core_delete(self.class_name)

    def undo(self):
        result = core_add(self.class_name)
        if result == 0:
            for attr in self.attributes:
                core_add_attr(self.class_name, attr.attribute)
            
        return result

    def redo(self):
        return core_delete(self.class_name)
