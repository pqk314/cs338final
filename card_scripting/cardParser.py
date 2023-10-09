import commands
# This module provides classes for parsing and executing Dominion card commands.
# multicommand parses a command string into multiple command instances.
# command represents a single command that can be executed, handling built-in
# functions like set/get/cond as well as calling external functions. 
# command instances are created by multicommand and executed.



class multicommand:
    def __init__(self, multicommand):
        self.commands = [command(c) for c in self.getSubcommands(self.replaceMacros(multicommand))]

    def execute(self):
        vals = {}
        res = None
        for cmd in self.commands:
            cmd.setVals(vals)
            res = cmd.execute()
            vals = cmd.getVals()
        return res

    @staticmethod
    def replaceMacros(cmd: str) -> str:
        i = cmd.find("&")
        while i != -1:
            j = i + 1
            while j < len(cmd) and cmd[j] not in ',;':
                j += 1
            macro = cmd[i+1:j]
            cmd = cmd[:i] + cards.macros[macro] + cmd[j:]
            
            i = cmd.find("&")
        return cmd

    @staticmethod
    def getSubcommands(cmd: str) -> list[str]:
        subcommands = cmd.split(";")
        if len(subcommands[-1]) <= 1:
            subcommands = subcommands[:-1]
        return [subcommand.strip() for subcommand in subcommands]

class command:
    """
    command: Class representing a command that can be executed.
    
    Instances of command represent a single command that can be executed. This includes getting command components like function name and arguments, formatting arguments, executing built-in functions like set/get/cond, and calling external functions. command instances are created by multicommand and executed.
    """
    def __init__(self, cmd, vals={}):
        self.vals = vals
        cmd = self.formatVariables(cmd)
        self.func = self.getFunc(cmd)
        self.args = self.getArgs(cmd)
        self.command = cmd
        self.createArgCommands()

    internalFuncs = ["set", "get", "cond"]

    def createArgCommands(self) -> None:
        for i, arg in enumerate(self.args):
            if arg[0] == "#":
                self.args[i] = command(arg, self.vals)

    def executeInternalFunc(self):
        if self.func == "set":
            self.vals[self.args[0]] = self.args[1].execute()
            return True
        elif self.func == "get":
            return self.vals[self.args[0]]
        elif self.func == "cond":
            if self.args[0].execute():
                self.args[1].execute()
                return True
            return False

    def executeExternalFunc(self):
        for i, arg in enumerate(self.args):
            if isinstance(arg, command):
                arg.setVals(self.vals)
                self.args[i] = arg.execute()
        return commands.doCommand(self.func, self.args)

    def execute(self):
        if self.func in self.internalFuncs:
            return self.executeInternalFunc()
        else:
            return self.executeExternalFunc()
        
        
    def getVals(self) -> dict:
        return self.vals
    
    def setVals(self, vals) -> None:
        self.vals = vals



    @staticmethod
    def replaceSetter(cmd) -> str:
        equal_idx = cmd.find('=')
        i = cmd.find('(')
        if equal_idx > -1 and (i == -1 or equal_idx < i):
            cmd = f"#set({cmd[:equal_idx].strip()}, {cmd[equal_idx+1:].strip()})"
        return cmd
    
    @staticmethod
    def replaceGetters(cmd) -> str:
        i = cmd.find('$')
        while i > -1:
            j = i
            while cmd[j] != ')' and cmd[j] != ',':
                j += 1
            varName = cmd[i+1:j]
            cmd = cmd[:i] + f"#get({varName})" + cmd[j:]
            i = cmd.find('$')
        
        return cmd

    @staticmethod
    def formatVariables(cmd):
        cmd = command.replaceSetter(cmd)
        cmd = command.replaceGetters(cmd)
        return cmd
        

    @staticmethod
    def getFunc(command):
        i = command.find('(')
        func = command[1:i]
        return func
        

    @staticmethod
    def getArgs(command):
        args = []
        argString = command[command.find('(')+1:-1]
        layer = 0
        i = 0
        while i < len(argString):
            if argString[i] == '(':
                layer += 1
            elif argString[i] == ')':
                layer -= 1
            elif argString[i] == ',' and layer == 0:
                args.append(argString[:i].strip())
                argString = argString[i+1:]
                i = -1
            i += 1
        args.append(argString[:i].strip())
        return args


import cards

'''c = multicommand(cards.cards['chapel'])
c = multicommand("$trash($fromHand(4, T))")

#c = command('$set(x, $fromHand(4, T))')
print(c.execute())'''

c2 = multicommand('x=#fromHand(4, T); #trash(#get(x))')
print(c2.execute())
c3 = multicommand('&chapel')
print(c3.execute())
