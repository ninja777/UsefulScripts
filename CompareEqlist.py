import copy

class equation():
    def __init__(self, operand, operations = None):
        self.operand = operand
        self.operations = operations

    def __str__(self):
        out =  "Operand : " + self.operand +'\n'
        out += "Operations :" + ','.join(self.operations)
        return out

class ocamlOutputFile():
    def __init__(self, filename, verbose=False):
        self.filename = filename
        self.verbose = verbose
        self.eqList = []

    def parseFile(self):
        f = open(self.filename, 'r')
        contents = f.read()
        f.close()
        contents = contents.split('\n')

        for line in contents:

            if line.startswith('[EQLIST]'):
                self.eqList.append([])
                line = line.split()
                line = ' '.join(line[1:])

            if line.strip().startswith('EQL->'):
                line = line.split()
                if line[0] == 'EQL->':
                    temp = line[1].split(':')
                    operand = temp[0][1:]
                    operations = temp[1].split(',')
                    operations[-1] = operations[-1][:-1]
                    eq = equation(operand=operand, operations=operations)
                    self.eqList[-1].append(eq)


class subSumptionClass():
    def __init__(self, filename, verbose=False):
        self.filename = filename
        self.verbose = verbose
        self.eqList = []

    def parseFile(self):
        f = open(self.filename, 'r')
        contents = f.read()
        f.close()
        contents = contents.split('\n')

        for line in contents:

            if line.startswith('**[SSO]'):
                self.eqList.append([])
                line = line.split()
                line = ' '.join(line[1:])
                #print "SSO line: ", line
                temp = line.split(':')
                operand = temp[0][1:]
                operations = temp[1].split(',')
                operations[-1] = operations[-1][:-1]
                eq = equation(operand=operand, operations=operations)
                self.eqList[-1].append(eq)

            if line.strip().startswith('-> [Subsumes]'):
                line = line.split()
                line = ' '.join(line[1:])
                line = line.split()
                if line[0] == '[Subsumes]':
                    temp = line[1].split(':')
                    operand = temp[0][1:]
                    operations = temp[1].split(',')
                    operations[-1] = operations[-1][:-1]
                    eq = equation(operand=operand, operations=operations)
                    self.eqList[-1].append(eq)



class hook():
    def __init__(self, hookName, secSensitiveOper=[]):
        self.hookName = hookName
        self.secSensitiveOper = secSensitiveOper

class function():
    def __init__(self, functionName, hook=[]):
        self.functionName = functionName
        self.hook = hook

class ocamlFunctionFile():
    def __init__(self, filename, verbose = False):
        self.filename = filename
        self.verbose = verbose
        self.functions = []

    def parseFile(self):
        f = open(self.filename, 'r')
        contents = f.read()
        f.close()
        contents = contents.split('\n')

        for line in contents:
            if line.strip().startswith('Function'):
                name = line.split()
                name = line[0].split(':')[1][1:-1]
                self.functions.append(function(functionName=name))

            if line.split()[1] == 'Hook':
                line = line.split()
                if line[0] == 'EQL->':
                    temp = line[1].split(':')
                    operand = temp[0]
                    operations = temp[1].split(',')
                    eq = equation(operand=operand, operations=operations)
                    self.eqList[-1].append(eq)

class AutoHook():
    def __init__(self, hook, fileName, line,stmt=None):
        self.hook = hook
        self.fileName = fileName
        self.line = line
        self.ifStmt = False
        self.stmt = stmt
        self.SSOs = []
        self.domHooks = []

class ManualHook():
    def __init__(self, hook, fileName, line):
        self.hook = hook
        self.fileName = fileName
        self.line = line
        self.Autohooks = []


class ocamlMaualHooks():
    def __init__(self, filename, verbose=False):
        self.filename = filename
        self.verbose = verbose
        self.ManHooks = []

    def parseFile(self):
        f = open(self.filename, 'r')
        contents = f.read()
        f.close()
        contents = contents.split('\n')
        isDom = False
        Autohooklist = []
        for line in contents:

            #print len(Autohooklist)
            if line.startswith('[ManualHook]'):
                if len(self.ManHooks) > 0:
                    print " In manhook present.."
                    #self.ManHooks[len(self.ManHooks) - 1].Autohooks = Autohooklist
                    # for autohook in Autohooklist:
                    #     aHook = copy.deepcopy(autohook)
                    #     self.ManHooks[len(self.ManHooks)-1].Autohooks.append(aHook)
                    # # del Autohooklist
                    # Autohooklist = []
                    print "length of auto for man hook ", len(self.ManHooks[len(self.ManHooks)-1].Autohooks),self.ManHooks[len(self.ManHooks)-1].hook
                Autohooklist = []
                #self.ManHooks.append([])
                line = line.split()
                hookCall = line[2].split('@')[0]
                filename = line[4].split('@')[0]
                lineNumber = line[4].split('@')[1]
                ManHook = ManualHook(hook=hookCall,fileName=filename,line=lineNumber)
                self.ManHooks.append(ManHook)
                print line
                line = ' '.join(line[1:])
                print "Manual Hook: ", line

            if line.strip().startswith('[AutoHook]'):
                isDom = False
                line = line.split()
                hookCall = line[1]
                filename = line[3].split('@')[0]
                lineNumber = line[3].split('@')[1]
                if hookCall.startswith('stm'):
                    stmt = line[5]
                    ahook = AutoHook(hookCall,filename,lineNumber,stmt)
                else:
                    ahook = AutoHook(hookCall, filename, lineNumber)
                self.ManHooks[len(self.ManHooks) - 1].Autohooks.append(ahook)
                #Autohooklist.append(ahook)
                if line[0] == '[AutoHook]':
                    print "Auto hook: ", line
                line = ' '.join(line[1:])

            if line.strip().startswith('[SSO]'):
                line = line.split()
                temp = line[1].split(':')
                operand = temp[0]
                operations = temp[1].split(',')
                eq = equation(operand=operand, operations=operations)
                line = ' '.join(line[1:])
                manHooklength = len(self.ManHooks)
                hooklength = len(self.ManHooks[manHooklength - 1].Autohooks)
                domLength = len(self.ManHooks[manHooklength - 1].Autohooks[hooklength-1].domHooks)
                if(isDom):
                    self.ManHooks[manHooklength - 1].Autohooks[hooklength - 1].domHooks[domLength-1].SSOs.append(eq)
                else:
                    self.ManHooks[manHooklength - 1].Autohooks[hooklength-1].SSOs.append(eq)

            if line.strip().startswith('- [Dom]'):
                isDom = True
                line = line.split()
                manHooklength = len(self.ManHooks)
                hooklength = len(self.ManHooks[manHooklength - 1].Autohooks)
                hookCall = line[2]
                filename = line[4].split('@')[0]
                lineNumber = line[4].split('@')[1]
                if hookCall.startswith('stm'):
                    stmt = line[5]
                    ahook = AutoHook(hookCall, filename, lineNumber, stmt)
                else:
                    ahook = AutoHook(hookCall, filename, lineNumber)
                self.ManHooks[len(self.ManHooks) - 1].Autohooks[hooklength-1].domHooks.append(ahook)
                line = ' '.join(line[1:])

            if line.strip().startswith('[Unmediated Hook]'):
                line = line.split()
                if line[0] == '[Unmediated':
                    print "Unmediated : ", line
                line = ' '.join(line[2:])

class ocamlAutoHooks():
    def __init__(self, filename, verbose=False):
        self.filename = filename
        self.verbose = verbose
        self.eqList = []

    def parseFile(self):
        f = open(self.filename, 'r')
        contents = f.read()
        f.close()
        contents = contents.split('\n')

        for line in contents:

            if line.startswith('[EQLIST]'):
                self.eqList.append([])
                line = line.split()
                line = ' '.join(line[1:])

            if line.strip().startswith('EQL->'):
                line = line.split()
                if line[0] == 'EQL->':
                    temp = line[1].split(':')
                    operand = temp[0][1:]
                    operations = temp[1].split(',')
                    operations[-1] = operations[-1][:-1]
                    eq = equation(operand=operand, operations=operations)
                    self.eqList[-1].append(eq)



if __name__ == '__main__':
    file1 = '../server13_ifiles/results/OUT-MHOOK-AHOOK1.txt'
    o = ocamlMaualHooks(filename=file1)
    o.parseFile()

    print "Man Hooks : ", len(o.ManHooks)
    for manHook in o.ManHooks:
        #print manHook
        print manHook.hook, manHook.fileName, manHook.line
        print len(manHook.Autohooks)
        for hook in manHook.Autohooks:
            print hook.hook, hook.fileName, hook.line
            print "SSO :",len(hook.SSOs)

        #print manHook.hook, manHook.fileName, manHook.line
        #print "Dominated Autohooks :",len(manHook.Autohooks)
        #print manHook.Autohooks


    # print "Number of lists :", len(o.eqList)
    # for i in range(len(o.eqList)):
    #     print "List Number ", i
    #     print "Equations :", len(o.eqList[i])