from ..core_func import core_add, core_delete


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
    """Command class for core_add"""
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
    """Command class for core_delete"""
    class_name = ''

    def __init__(self, name):
        self.class_name = name

    def execute(self):
        return core_delete(self.class_name)

    def undo(self):
        return core_add(self.class_name)

    def redo(self):
        return core_delete(self.class_name)
