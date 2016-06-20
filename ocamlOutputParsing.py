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

if __name__ == '__main__':
    file1 = 'Xserver_versions/server14_ifiles/resultsnew/OUT-MHOOK-AHOOK-EQUAL.txt'
    o = ocamlOutputFile(filename=file1)
    o.parseFile()
    print "Number of lists :", len(o.eqList)
    for i in range(len(o.eqList)):
        print "List Number ", i
        print "Equations :", len(o.eqList[i])