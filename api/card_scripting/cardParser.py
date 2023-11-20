from card_scripting import commands
from card_scripting import cards
# This module provides classes for parsing and executing Dominion card commands.
# multicommand parses a command string into multiple command instances.
# command represents a single command that can be executed, handling built-in
# functions such as set/get/cond as well as calling external functions. 
# command instances are created by multicommand and executed.


class multicommand:
    '''
    A class representing and giving functionality to the text of a card
    See the README in the card_scripting folder for more information on the syntax of the scripting language
    
    '''
    def __init__(self, multicommand, player):
        self.multicommand = multicommand
        self.player = player
        self.vals = {}
        self.nextVar = 0
        self.playerInput = None
        self.setupCommands()

    def setPlayerInput(self, playerInput):
        # used to set player input when execution is paused partway through
        self.playerInput = playerInput

    def execute(self):
        # executes each subcommand one by one and removes it, stopping if player input is required
        res = None
        while self.commands:
            if self.shouldReplaceYield():
                self.replaceYield()
                continue
            else:
                res = self.executeSubcommand()
                if res == "yield":
                    return "yield"
        return res
    
    def setupCommands(self):
        verboseCommand = self.replaceMacros(self.multicommand)
        cleaned = self.replaceRawStrings(verboseCommand)
        subcommands = self.getSubcommands(cleaned)
        reformattedSubcommands = self.seperateYields(subcommands)
        self.commands = [command(cmd, self.player, self.vals) for cmd in reformattedSubcommands]

    def replaceRawStrings(self, raw):
        # sometimes strings need characters that have reserved meanings. This function extracts them to variables where they will be left alone
        # raw strings are enclosed in backticks and cannot be nested
        while '`' in raw:
            i = raw.index("`")
            end = raw.index("`", i+1)
            varName = f"_internalYieldVar{self.nextVar}"
            self.nextVar += 1
            self.vals[varName] = raw[i+1:end]
            raw = f"{raw[:i]}${varName}{raw[end+1:]}"
        return raw

    def shouldReplaceYield(self) -> bool:
        # if the first command is a set and we have received player input, the variable will be replaced with the player input
        return self.playerInput != None and self.commands[0].func == "set"
    
    def replaceYield(self):
        # replace variable in set command with player input
        self.vals[self.commands[0].args[0]] = self.playerInput
        self.commands = self.commands[1:]
        self.playerInput = None

    def executeSubcommand(self):
        # executes the first command in the list and removes it from the list
        self.commands[0].setVals(self.vals)
        res = self.commands[0].execute()
        if res == "yield":
            return "yield"
        if len(self.commands) > 0:
            self.vals = self.commands[0].getVals()
            self.commands = self.commands[1:]
        return res


    def replaceYieldCommand(self, cmd: str, yieldFunc: str) -> str:
        # commands requiring player input have to be extracted (i.e. cannot be nested) and so are extracted and stored in variables as early as possible
        endpoints = self.findYieldCommand(cmd, yieldFunc)
        if endpoints == None:
            return None
        cmdStart = endpoints[0] - 1
        cmdEnd = endpoints[1] + 1
        newCommands = self.getNewCommands(cmd, cmdStart, cmdEnd)
        return newCommands
        
    def findYieldCommand(self, cmd: str, yieldFunc: str) -> tuple[int, int]:
        # finds a specific function call in a command string, if it exists
        i = cmd.find(yieldFunc)
        if i == -1:
            return
        j = i + len(yieldFunc)
        layer = 0
        while j < len(cmd):
            if cmd[j] == '(':
                layer += 1
            elif cmd[j] == ')':
                layer -= 1
                if layer == 0:
                    break
            j += 1
        return i, j

    def getNewCommands(self, cmd: str, cmdStart: int, cmdEnd: int) -> list[str]:
        # helper function for removing player input commands
        yieldCmd = cmd[cmdStart:cmdEnd]
        varName = f"_internalYieldVar{self.nextVar}"
        self.nextVar += 1
        setCmd = f"#set({varName}, {yieldCmd})"
        getCmd = cmd[:cmdStart] + f"#get({varName})" + cmd[cmdEnd:]
        return [setCmd, getCmd]

    def seperateYields(self, cmdStrs: list[str]) -> list[str]:
        # iterates through each subcommand and player input functions and replaces them
        yieldFuncs = commands.yieldFuncs
        cmdIdx = 0
        while cmdIdx < len(cmdStrs):
            cmd = cmdStrs[cmdIdx]
            for yieldFunc in yieldFuncs:
                newLines = self.replaceYieldCommand(cmd, yieldFunc)
                if newLines != None:
                    cmdStrs[cmdIdx:cmdIdx + 1] = newLines
                    break
           
            cmdIdx += 1
        return cmdStrs

    @staticmethod
    def replaceMacros(cmd: str) -> str:
        # replaces macros with their verbose versions
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
        #splits a multicommand strubg into subcommand strings
        subcommands = cmd.split(";")
        if len(subcommands[-1]) <= 1:
            subcommands = subcommands[:-1]
        return [subcommand.strip() for subcommand in subcommands]

class command:
    """
    command: Class representing a command that can be executed.
    
    Instances of command represent a single command that can be executed.
    They can be nested--a commands arguments can be other commands, which will be executed first
    command instances are created by multicommand and executed and should not be created externally
    """
    def __init__(self, cmd, player, vals={}):
        self.vals = vals
        self.player = player
        cmd = self.formatVariables(cmd)
        self.func = self.getFunc(cmd)
        self.args = self.getArgs(cmd)
        self.command = cmd
        self.createArgCommands()

    internalFuncs = ["set", "get", "cond"]

    def createArgCommands(self) -> None:
        # for each argument which is a function, replaces it with a command instance
        for i, arg in enumerate(self.args):
            if arg[0] == "#":
                self.args[i] = command(arg, self.player, self.vals)

    def executeInternalFunc(self):
        # handles internal functions: set, get, and cond (if)
        if self.func == "set":
            self.args[1].vals = self.vals
            res = self.args[1].execute()
            if res == "yield":
                return "yield"
            self.vals[self.args[0]] = res
            return True
        elif self.func == "get":
            return self.vals[self.args[0]]
        elif self.func == "cond":
            self.args[0].setVals(self.vals)
            res = self.args[0].execute()
            self.vals = self.args[0].getVals()
            if res:
                self.args[1].setVals(self.vals)
                self.args[1].execute()
                self.vals = self.args[1].getVals()
                return True
            return False

    def executeExternalFunc(self):
        # handles external functions, defined in commands.py
        # all functions take the same two arguments, args and player, though the content of well formatted args varies by function
        for i, arg in enumerate(self.args):
            if isinstance(arg, command):
                arg.setVals(self.vals)
                self.args[i] = arg.execute()
                self.vals = arg.getVals()
        return commands.doCommand(self.func, self.args, self.player)

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
        # replaces variable assignment syntax varName=#funcName() with internally used #set(varName, #funcName())
        equal_idx = cmd.find('=')
        i = cmd.find('(')
        if equal_idx > -1 and (i == -1 or equal_idx < i):
            cmd = f"#set({cmd[:equal_idx].strip()}, {cmd[equal_idx+1:].strip()})"
        return cmd
    
    @staticmethod
    def replaceGetters(cmd) -> str:
        # replaces variable getter syntax $varName with internally used #get(varName)
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
        # gets the name of the function in a function string
        i = command.find('(')
        func = command[1:i]
        return func
        

    @staticmethod
    def getArgs(command):
        # gets a list of each arg in a function string
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
        nonEmptyArgs = [arg for arg in args if arg != '']
        return nonEmptyArgs