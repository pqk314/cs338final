from card_scripting import commands
# This module provides classes for parsing and executing Dominion card commands.
# multicommand parses a command string into multiple command instances.
# command represents a single command that can be executed, handling built-in
# functions lcike set/get/cond as well as calling external functions. 
# command instances are created by multicommand and executed.



class multicommand:
    def __init__(self, multicommand, gameID):
        self.multicommand = multicommand
        self.gameID = gameID
        self.vals = {}
        self.nextVar = 0
        self.playerInput = None
        self.setupCommands()

    def setPlayerInput(self, playerInput):
        self.playerInput = playerInput

    def execute(self):
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
        subcommands = self.getSubcommands(self.replaceMacros(self.multicommand))
        reformattedSubcommands = self.seperateYields(subcommands)
        self.commands = [command(cmd, self.gameID) for cmd in reformattedSubcommands]

    def shouldReplaceYield(self) -> bool:
        return self.playerInput != None and self.commands[0].func == "set"
    
    def replaceYield(self):
        self.vals[self.commands[0].args[0]] = self.playerInput
        self.commands = self.commands[1:]
        self.playerInput = None

    def executeSubcommand(self):
        self.commands[0].setVals(self.vals)
        res = self.commands[0].execute()
        if res == "yield":
            return "yield"
        self.vals = self.commands[0].getVals()
        self.commands = self.commands[1:]
        return res


    def replaceYieldCommand(self, cmd: str, yieldFunc: str) -> str:
        endpoints = self.findYieldCommand(cmd, yieldFunc)
        if endpoints == None:
            return None
        cmdStart = endpoints[0] - 1
        cmdEnd = endpoints[1] + 1
        newCommands = self.getNewCommands(cmd, cmdStart, cmdEnd)
        return newCommands
        
    def findYieldCommand(self, cmd: str, yieldFunc: str) -> tuple[int, int]:
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
        yieldCmd = cmd[cmdStart:cmdEnd]
        varName = f"_internalYieldVar{self.nextVar}"
        self.nextVar += 1
        setCmd = f"#set({varName}, {yieldCmd})"
        getCmd = cmd[:cmdStart] + f"#get({varName})" + cmd[cmdEnd:]
        return [setCmd, getCmd]

    def seperateYields(self, cmdStrs: list[str]) -> list[str]:
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
    def __init__(self, cmd, gameID, vals={}):
        self.vals = vals
        self.gameID = gameID
        cmd = self.formatVariables(cmd)
        self.func = self.getFunc(cmd)
        self.args = self.getArgs(cmd)
        self.command = cmd
        self.createArgCommands()

    internalFuncs = ["set", "get", "cond"]

    def createArgCommands(self) -> None:
        if self.func == 'attack':
            return
        for i, arg in enumerate(self.args):
            if arg[0] == "#":
                self.args[i] = command(arg, self.gameID, self.vals)

    def executeInternalFunc(self):
        if self.func == "set":
                try:
                    self.args[1].vals = self.vals
                
                except:
                    raise ValueError(self.command, self.args)
                res = self.args[1].execute()
                if res == "yield":
                    return "yield"
                self.vals = self.args[1].vals
                self.vals[self.args[0]] = res
                return True
        elif self.func == "get":
            return self.vals[self.args[0]]
        elif self.func == "cond":
            self.args[0].vals = self.vals
            res = self.args[0].execute()
            self.vals = self.args[0].getVals()
            
            #raise ValueError(self.args)
            if res:
                self.args[1].vals = self.vals
                self.args[1].execute()
                self.vals = self.args[1].getVals()
                return True
            return False

    def executeExternalFunc(self):
        for i, arg in enumerate(self.args):
            if isinstance(arg, command):
                arg.setVals(self.vals)
                self.args[i] = arg.execute()
                self.vals = arg.getVals()
        return commands.doCommand(self.func, self.args, self.gameID)

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
        if equal_idx > -1 and cmd[equal_idx-1] not in ' <>!':
            i = cmd.find('(', equal_idx)
            if (i == -1 or equal_idx < i):
                s = equal_idx
                while s > 0 and cmd[s]!= ' ':
                    s -= 1
                if s > 0: s += 1
                e = i
                layer = 1
                while layer > 0:
                    e += 1
                    if cmd[e] == '(':
                        layer += 1
                    elif cmd[e] == ')':
                        layer -= 1
                cmd = f"{cmd[:s]}#set({cmd[s:equal_idx].strip()}, {cmd[equal_idx+1:e+1].strip()}){cmd[e+1:]}"
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
        nonEmptyArgs = [arg for arg in args if arg != '']
        return nonEmptyArgs



if __name__ == "__main__":
    import cards
    #txt = '#trash(#chooseSubset(#getHand(), 4, T))'
    #txt = 'x=#fromHand(4, T); #trash($x)'
    txt = cards.getCardText('harbinger')
    cmd = multicommand(txt)
    print(cmd.execute())
    cmd.setPlayerInput([1, 2, 3, 4])
    print(cmd.execute())