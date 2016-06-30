# open terminal, browse to the directory that contains this script and enter the following commands
#==========================
# python
# import outputFileParsing as o
# ff = o.fileFormat(baseDirectory='Analyzed', outputDirectory='output', verbose=False, pattern='.out', excludePattern='.opt.out')
# ff.generateStatistics()
#==========================
# Now you can access all the properties of ff given below
# ff.files                      # list of files in output/results folder
# ff.emptyFiles                 # list of empty files
# ff.directories                # list of directories in Analyzed folder
# ff.indirectCalls              # map of indirect calls key = filename, value = list of indirectCalls
# ff.targets                    # map of targets key = filename_callName, value = list of targets
# ff.callSitesWithNoTargets     # list of callsites with no targets. Each value = [filename, callName]
# ff.dirmap                     # map of directories dirmap={dirname,filemap}, filemap={filename, indirectcallmap}, indirectcallmap={call,list oftargets}

import os
import datetime
import argparse

class fileFormat():

    def __init__(self, baseDirectory='Analyzed', outputDirectory='output', verbose=False, pattern='.out', excludePattern='.opt.out'):
        # Parameters
        self.baseDirectory = baseDirectory
        self.outputDirectory = outputDirectory
        self.verbose = verbose
        self.pattern = pattern
        self.excludePattern = excludePattern

        #Properties
        self.files = []     # list of files in output/results folder
        self.emptyFiles = [] # list of empty files
        self.directories = []   # list of directories in Analyzed folder
        self.indirectCalls={}    # map of indirect calls key = filename, value = list of indirectCalls
        self.targets={}         # map of targets key = filename_callName, value = list of targets
        self.callSitesWithNoTargets = [[]] # list of callsites with no targets. Each value = [filename, callName]
        self.dirmap = {}     # map of directories dirmap={dirname,filemap}, filemap={filename, indirectcallmap}, indirectcallmap={call,list oftargets}
        self.errCalls = []   # list of all the calls with error
        self.indirectErrorCalls={}  # map of error indirect calls key = filename, value = list of error indirectCalls
        #self.errorDirmap = {}


    def getCallInst(self,callName):
        if len(callName) > 0 and callName[0] == '[':
            callName = callName[callName.index(']') + 1:]
            callName = callName.strip(' ')
        return callName

    def getFilenameonly(self,filename):
        # print "Full filename :--- "
        # print filename
        namesplit = filename.split("/")
        filename = namesplit[len(namesplit)-1]
        if(filename.endswith(self.pattern)):
            filename = filename[:-len(self.pattern)]
        if(filename.endswith(".bc")):
            filename = filename[:-3]
        # print filename
        return filename

    def getIndirectErrorCalls(self, filename):
        verbose = self.verbose
        callName = ''
        if verbose:
            print "getindirectCalls :: Reading file :", filename
        f = open(filename, 'r')
        contents = f.read()
        f.close()
        indirectCalls = contents.count('[ERROR]')
        contents = contents.split('\n')
        indirectErrorCalls = []
        for line in contents:
            if line.startswith("[ERROR]"):
                #collect all indirect calls with errors.
                line = line.split(']')
                #print len(line)
                if(len(line)>=2):
                    callName = line[1]
                    indirectErrorCalls.append(callName)
                    self.errCalls.append(callName)
        self.indirectErrorCalls[filename] = indirectErrorCalls
        return  indirectErrorCalls



    def getIndirectCalls(self, filename):
        verbose = self.verbose
        callName = ''
        if verbose:
            print "getindirectCalls :: Reading file :", filename
        f = open(filename, 'r')
        contents = f.read()
        f.close()
        indirectCalls = contents.count('========')
        contents = contents.split('\n')
        count = 0
        countCalls = False
        localTargetCount = 0
        prevLine = None
        targets = []
        temp_calls = []
        filemap = {}
        indirectcallmap = {}
        for line in contents:
            if line == '':
                countCalls = False
                if prevLine == '========' and localTargetCount == 0:
                    self.callSitesWithNoTargets.append([filename, callName])
                else:
                    self.targets[filename + '_' + callName] = targets
                    #create indcall to targets list map here.
                    if len(callName) >0:
                        callInst = self.getCallInst(callName)
                        indirectcallmap[callInst] = targets
            elif countCalls:
                count += 1
                targets.append(line)
                localTargetCount +=1
            elif line == '========':
                callName = prevLine
                targets = []
                temp_calls.append(callName)
                countCalls = True
                localTargetCount = 0
            prevLine = line
        filenameonly = self.getFilenameonly(filename)
        if(len(indirectcallmap)>0):
            filemap[filenameonly] = indirectcallmap
        self.indirectCalls[filename] = temp_calls
        return count, indirectCalls,filemap

    def getFileCounts(self, directory):
        verbose = self.verbose
        pattern = self.pattern
        excludePattern = self.excludePattern
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        emptyFiles=[]
        emptyCount = 0
        count = 0
        for f in files:
            f = os.path.join(directory, f)
            if f.endswith(excludePattern) or (not f.endswith(pattern)):
                continue
            self.files.append(f)
            count += 1
            statinfo = os.stat(f)
            if verbose:
                print "getEmptyFileCounts :: ", f, ' : ' ,statinfo.st_size
            if statinfo.st_size == 0:
                self.emptyFiles.append(f)
                emptyCount += 1
                emptyFiles.append(f)
        return count, emptyCount, emptyFiles

    def generateStatistics(self):
        verbose = self.verbose
        directory = self.baseDirectory
        outputDirectory = self.outputDirectory
        pattern = self.pattern
        excludePattern = self.excludePattern
        totalAnalyzed = []
        emptyFilesCount = []
        emptyFiles = []
        targets = []
        calls = []
        directoryStats = {}
        ErrorCalls = []
        for dir in next(os.walk(directory))[1]:
            # print "directpry :", dir
            path = os.path.join(os.path.abspath(directory), dir)
            self.directories.append(path)
            output = os.path.join(path,outputDirectory)
            # print output
            total, empties, zeroKBFiles = self.getFileCounts(output)
            totalAnalyzed.append(total)
            emptyFilesCount.append(empties)
            emptyFiles.extend(zeroKBFiles)
            if verbose:
                print "generateStatistics :: current directory :", output

            currentDirTargets = 0
            currentDirCalls = 0
            currentDirErrors = 0

            for _, _, outputFiles in os.walk(output):
                for eachFile in outputFiles:
                    if eachFile.endswith(pattern) and (not eachFile.endswith(excludePattern)):
                        filemap = {}
                        if verbose:
                            print "generateStatistics :: current file :", os.path.join(output, eachFile)
                        count, indirectCalls, filemap = self.getIndirectCalls(filename=os.path.join(output, eachFile))
                        self.getIndirectErrorCalls(filename=os.path.join(output, eachFile))
                        targets.append(count)
                        calls.append(indirectCalls)
                        currentDirTargets += count
                        currentDirCalls += indirectCalls
                        #print "file map ~~~~~~~~~~~~~~~~~~~~~~~~  : ", filemap
                        self.dirmap[dir] = filemap

            directoryStats[output] = [totalAnalyzed[-1], emptyFilesCount[-1], currentDirTargets, currentDirCalls]

        # print emptyFiles
        return totalAnalyzed, emptyFilesCount, targets, calls, directoryStats

def rreplace(s, old, new, occurrence=1):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def compareOutputFiles(file1, file2, verbose = False, outputFile='output.csv'):
    if verbose:
        print "Comparing file", file1, " with ", file2
    if os.path.isfile(file1) and os.path.isfile(file2):

        f = open(file1, 'r')
        contents1 = f.read()
        f.close()

        f = open(file2, 'r')
        contents2 = f.read()
        f.close()

        contents1 = contents1.split('\n')
        contents2 = contents2.split('\n')

        callBegin = False
        cursor = []
        cursorStartInContents2 = 0
        cursorEndInContents2 = 0
        call = ''
        for line in contents1:
            if len(line) > 0 and line[0] == '[' and (not callBegin):
                line = line[line.index(']')+1:]
                line = line.strip(' ')
                call = line
                callBegin = True
                cursor = [k for k in range(len(contents2)) if line in contents2[k]]

                if len(cursor) > 0:
                    cursorStartInContents2 = cursor[0]
                    cursorStartInContents2 = cursorStartInContents2 + 2  # ignore current line and next line
                    for k in range(len(contents2) - cursorStartInContents2):
                        if contents2[cursorStartInContents2+k] == '':
                            cursorEndInContents2 = cursorStartInContents2 + k
                            break
                    continue
                else:
                    out = 'File:,"' + file1 + '", No Match for Call:,' + call + '", Line:,"' + line + '"\n'
                    outputFile.write(out)
                    continue
            if line == '':
                callBegin = False
                cursorStartInContents2 = 0
                cursorEndInContents2 = 0
                continue
            if callBegin:
                if line in contents2[cursorStartInContents2 : cursorEndInContents2]:
                    if verbose:
                        print "Call : ", call, "->", line , " matches in both files"
                else:
                    if line.strip(' ')[0:2] != '==':
                        out = 'File:,"'+ file1 + '", Call:,"' + call + '", Line:,"' + line + '"\n'
                        outputFile.write(out)

def generateComparison(directory='Analyzed', comparisonDirectory1='output', comparisonDirectory2='Results', verbose=False):
    outputFile = open('comparison' + str(datetime.datetime.now()) + '.csv', 'a')
    for dir in next(os.walk(directory))[1]:
        # print path to all subdirectories first.
        compare1 = os.path.abspath(directory) + '/' + os.path.join(dir, comparisonDirectory1)
        compare2 = os.path.abspath(directory) + '/' + os.path.join(dir, comparisonDirectory2)

        fileList1 = next(os.walk(compare1))[2]
        fileList1 = [k for k in fileList1 if k.endswith('.out') and (not k.endswith('.opt.out'))]
        fileList2 = next(os.walk(compare2))[2]
        fileList2 = [k for k in fileList2 if k.endswith('.bc.results') and (not k.endswith('.opt.bc.results'))]

        if len(fileList1) == len(fileList2):
            if verbose:
                print compare1, "  Matches with ", compare2
            for eachFile in fileList1:
                compareOutputFiles(
                    os.path.join(compare1, eachFile),
                    os.path.join(compare2, rreplace(eachFile, '.out', '.bc.results')),
                    outputFile=outputFile
                )
        else:
            print compare1, ":: ", fileList1
            print compare2, ":: ", fileList2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", '--directory', help="base directory of analysis", default='Analyzed',
                        type=str)
    parser.add_argument('-o','--output', help='output directory name in the subdirectories', default='output', type=str)
    parser.add_argument('-e', '--extension', help='Extension of files to be used', default = '.sigout', type=str)
    parser.add_argument('-x', '--exclude', help='Extension of files to be excluded', default=' ', type=str)
    parser.add_argument('-v','--verbose', help='Print verbose output',
                        action="store_true", default=False)
    parser.add_argument('-c', '--compare', help='Print compare results of the individual files one on one', default=0,
                        type=bool)

    args = parser.parse_args()
    directory = args.directory
    outDir = args.output
    fileExtension = args.extension
    excludePattern = args.exclude
    verbose=args.verbose
    compare=args.compare

    ff = fileFormat(baseDirectory=directory, outputDirectory=outDir, verbose=verbose, pattern=fileExtension, excludePattern=excludePattern)
    ff.generateStatistics()

    print "Total analyzed :", len(ff.files)
    print "Empty files :", len(ff.emptyFiles)

    indirectCallsCount = 0
    for k in ff.indirectCalls.keys():
        indirectCallsCount += len(ff.indirectCalls[k])

    print "Indirect calls :", indirectCallsCount

    targets = 0
    for k in ff.targets.keys():
        targets += len(ff.targets[k])

    print "Total targets :", targets

    print "Average targets per call :", targets/ float(indirectCallsCount)

    targetless = 0
    print "Call sites with no target : ", len(ff.callSitesWithNoTargets)



    print " Error Calls : ", len(ff.errCalls)

    #print "directory map ----------------------  ", ff.dirmap
    # print '\n'.join(ff.callSitesWithNoTargets)
    # for c in ff.callSitesWithNoTargets:
    #     print c
    # for t in ff.targets:
    #     print t, ff.targets[t]

    #generateComparison()



