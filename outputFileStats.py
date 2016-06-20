import os


def getIndirectCalls(filename='beanstalkd.out', verbose=False):
    if verbose:
        print "getindirectCalls :: Reading file :", filename
    f = open(filename, 'r')
    contents = f.read()
    f.close()
    indirectCalls = contents.count('========')
    contents = contents.split('\n')
    count = 0
    countCalls = False
    for line in contents:
        if line == '':
            countCalls = False
        elif countCalls:
            count += 1
        elif line == '========':
            countCalls = True
    print count

    return count, indirectCalls

def getFileCounts(directory, verbose=False, pattern = 'out'):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    emptyCount = 0
    count = 0
    for f in files:
        if not f.endswith(pattern):
            continue
        count += 1
        statinfo = os.stat(os.path.join(directory,f))
        if verbose:
            print "getEmptyFileCounts :: ", f, ' : ' ,statinfo.st_size
        if statinfo.st_size == 0:
            emptyCount += 1
    return count, emptyCount

def generateStatistics(baseDirectory='Analyzed',resultsDirectory='output', verbose=False, pattern ='out'):
    totalAnalyzed = []
    emptyFiles = []
    targets = []
    calls = []
    directoryStats = {}
    for dirname, dirnames, filenames in os.walk(baseDirectory):
        # print path to all subdirectories first.

        for subdirname in dirnames:
            if subdirname != resultsDirectory:
                continue
            output = os.path.abspath('.') + '/' + os.path.join(dirname, subdirname)
            #output = path + '/' + directory
            if (('Transformed' not in output) and ('Bitcode' not in output) and ('Results' not in output) and (resultsDirectory in output)):
                total, empties = getFileCounts(output, verbose=verbose, pattern=pattern)

                totalAnalyzed.append(total)
                emptyFiles.append(empties)

                dirCalls = 0
                dirTargets = 0
                if verbose:
                    print "generateStatistics :: current directory :", output
                for _, _, outputFiles in os.walk(output):
                    for eachFile in outputFiles:
                        if eachFile.endswith(pattern):
                            if verbose:
                                print "generateStatistics :: current file :", os.path.join(output, eachFile)
                            count, indirectCalls = getIndirectCalls(filename=os.path.join(output, eachFile), verbose=verbose)
                            targets.append(count)
                            calls.append(indirectCalls)
                            dirCalls += indirectCalls
                            dirTargets += count
                if(resultsDirectory in dirname):
                    if("output/output" not in dirname):
                        directoryStats[dirname] = [total,empties,dirTargets,dirCalls]

    return totalAnalyzed, emptyFiles, targets, calls, directoryStats

if __name__ == '__main__':
    totalAnalyzed, emptyFiles, targets, calls, dirStats = generateStatistics(resultsDirectory='output', verbose=True, pattern='.out')
    print "--- Results per dir ----"
    printStat = sorted(dirStats.items(), key=lambda x: x[1][3], reverse=True)

    for stat in printStat:
        print stat  # ' : \t\t\t',printStat[stat]
    print "Total analyzed :", sum(totalAnalyzed)
    print "Empty files :", sum(emptyFiles)
    print "Indirect calls :", sum(calls)
    print "Total targets :", sum(targets)
    print "Average targets per call :", sum(targets)/ float(sum(calls))

