
# could (should) be a singleton.


class command_stack:
    commandStack = []
    redoStack = []

    def execute(self, command):

        if command.execute():
            return 1
            
        self.commandStack.insert(0, command)
        self.redoStack.clear()
        return 0

    def undo(self):
        if len(self.commandStack) == 0:
            return
        command = self.commandStack.pop(0)
        command.undo()
        self.redoStack.insert(0, command)

    def redo(self):
        if len(self.redoStack) == 0:
            return
        command = self.redoStack.pop(0)
        command.redo()
        self.commandStack.insert(0, command)
