import os
import datetime
import numpy as np

def getIndirectCalls(filename='beanstalkd.out', verbose=False):
    callSitesWithNoTargets = 0
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
    for line in contents:
        if line == '':
            countCalls = False
            if prevLine == '========' and localTargetCount == 0:
                callSitesWithNoTargets += 1
                print callSitesWithNoTargets
        elif countCalls:
            count += 1
            localTargetCount +=1
        elif line == '========':
            countCalls = True
            localTargetCount = 0
        prevLine = line
    return count, indirectCalls, callSitesWithNoTargets

def getFileCounts(directory, verbose=False, pattern = 'out'):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    emptyCount = 0
    count = 0
    for f in files:
        f = os.path.join(directory, f)
        if not f.endswith(pattern):
            continue
        count += 1
        statinfo = os.stat(f)
        if verbose:
            print "getEmptyFileCounts :: ", f, ' : ' ,statinfo.st_size
        if statinfo.st_size == 0:
            emptyCount += 1
    return count, emptyCount

def generateStatistics(directory='Analyzed', outputDirectory='output', verbose=False, pattern = 'out'):
    totalAnalyzed = []
    emptyFiles = []
    targets = []
    calls = []
    directoryStats = {}
    for dir in next(os.walk(directory))[1]:
        # print dir
        path = os.path.join(os.path.abspath(directory), dir)
        output = os.path.join(path,outputDirectory)
        # print output
        total, empties = getFileCounts(output, verbose=verbose, pattern=pattern)
        totalAnalyzed.append(total)
        emptyFiles.append(empties)

        if verbose:
            print "generateStatistics :: current directory :", output

        currentDirTargets = 0
        currentDirCalls = 0

        for _, _, outputFiles in os.walk(output):
            for eachFile in outputFiles:
                if eachFile.endswith(pattern):
                    if verbose:
                        print "generateStatistics :: current file :", os.path.join(output, eachFile)
                    count, indirectCalls, callwithNoTargets = getIndirectCalls(filename=os.path.join(output, eachFile), verbose=verbose)
                    targets.append(count)
                    calls.append(indirectCalls)
                    currentDirTargets += count
                    currentDirCalls += indirectCalls

        directoryStats[output] = [totalAnalyzed[-1], emptyFiles[-1], currentDirTargets, currentDirCalls]


    return totalAnalyzed, emptyFiles, targets, calls, directoryStats

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




def generateComparison(directory='Analyzed', comparisonDirectory1='output', comparisonDirectory2='results', verbose=False):
    outputFile = open('comparison' + str(datetime.datetime.now()) + '.csv', 'a')
    for dir in next(os.walk(directory))[1]:
        # print path to all subdirectories first.
        compare1 = os.path.abspath(directory) + '/' + os.path.join(dir, comparisonDirectory1)
        compare2 = os.path.abspath(directory) + '/' + os.path.join(dir, comparisonDirectory2)

        fileList1 = next(os.walk(compare1))[2]
        fileList1 = [k for k in fileList1 if k.endswith('.out')]
        fileList2 = next(os.walk(compare2))[2]
        fileList2 = [k for k in fileList2 if k.endswith('.bc.results')]

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
            print compare1, " Does Not Match with ", compare2

if __name__ == '__main__':
    totalAnalyzed, emptyFiles, targets, calls, directoryStats = generateStatistics(outputDirectory='output',verbose=False, pattern='.out')

    printStat = sorted(directoryStats.items(), key=lambda x: x[1][3], reverse=True)
    for stat in printStat:
        print stat

    print "Total analyzed :", sum(totalAnalyzed)
    print "Empty files :", sum(emptyFiles)
    print "Indirect calls :", sum(calls)
    print "Total targets :", sum(targets)
    print "Average targets per call :", sum(targets)/ float(sum(calls))
    # for stat in directoryStats:
    #     print stat, ":", directoryStats[stat]
    # generateComparison()



