import outputFileParsing as o


def getFilenameonly(filename,pattern):
    #print filename
    namesplit = filename.split("/")
    filename = namesplit[len(namesplit) - 1]
    dirname  = namesplit[len(namesplit) - 3]
    if (filename.endswith(pattern)):
        filename = filename[:-len(pattern)]
    if (filename.endswith(".bc")):
        filename = filename[:-3]
    return dirname, filename


if __name__ == '__main__':
    #class for Output (signature based approach)
    ffOutput = o.fileFormat(baseDirectory='Analyzed', outputDirectory='output', verbose=False, pattern='.out1', excludePattern='.opt.out')
    ffOutput.generateStatistics()

    print "---------Output for signature based analysis--------"
    print "Total analyzed :", len(ffOutput.files)
    print "Empty files :", len(ffOutput.emptyFiles)

    indirectCallsCount = 0
    for k in ffOutput.indirectCalls.keys():
        indirectCallsCount += len(ffOutput.indirectCalls[k])

    print "Indirect calls :", indirectCallsCount

    targets = 0
    for k in ffOutput.targets.keys():
        targets += len(ffOutput.targets[k])

    print "Total targets :", targets

    print "Average targets per call :", targets / float(indirectCallsCount)

    targetless = 0
    print "Call sites with no target : ", len(ffOutput.callSitesWithNoTargets)

    #Create class for results..(function pointer based approach)
    ffResults = o.fileFormat(baseDirectory='Analyzed', outputDirectory='Results', verbose=False, pattern='.results', excludePattern='.opt.bc.results')
    ffResults.generateStatistics()

    print " "
    print "---------Output for Function pointer based analysis--------"
    print "Total analyzed :", len(ffResults.files)
    print "Empty files :", len(ffResults.emptyFiles)

    indirectCallsCount = 0
    for k in ffResults.indirectCalls.keys():
        indirectCallsCount += len(ffResults.indirectCalls[k])

    print "Indirect calls :", indirectCallsCount

    targets = 0
    for k in ffResults.targets.keys():
        targets += len(ffResults.targets[k])

    print "Total targets :", targets

    print "Average targets per call :", targets / float(indirectCallsCount)

    targetless = 0
    print "Call sites with no target : ", len(ffResults.callSitesWithNoTargets)
    outEmptyMap = {}
    resultEmptyMap = {}

    for empfile in ffOutput.emptyFiles:
        dirname, empfile = getFilenameonly(empfile,ffOutput.pattern)
        if dirname in outEmptyMap:
            filelist = outEmptyMap[dirname]
            filelist.append(empfile)
            outEmptyMap[dirname] = filelist
        else:
            filelist = []
            filelist.append(empfile)
            outEmptyMap[dirname] = filelist

        #print "empty in: ", dirname," file :",empfile

    for empfile in ffResults.emptyFiles:
        dirname, empfile = getFilenameonly(empfile, ffResults.pattern)
        if dirname in resultEmptyMap:
            filelist = resultEmptyMap[dirname]
            filelist.append(empfile)
            resultEmptyMap[dirname] = filelist
        else:
            filelist = []
            filelist.append(empfile)
            resultEmptyMap[dirname] = filelist

    #compare the directories and empty files.. in each case

    for dir in outEmptyMap:
        if(not dir in resultEmptyMap):
            print "Empty files only in Output : ",dir,outEmptyMap[dir]
        else:
            for file1 in outEmptyMap[dir]:
                if(not file1 in resultEmptyMap[dir]):
                    print "Empty files only in Output : ", dir, file1

    print " "
    print "*******************"
    print " "
    for dir in resultEmptyMap:
        if (not dir in outEmptyMap):
            print "Empty files only in Output : ", dir, resultEmptyMap[dir]

    # print "*******************"
    # for dir in outEmptyMap:
    #     print dir, outEmptyMap[dir]
    #
    # print "########################"
    # for dir in resultEmptyMap:
    #     print dir, resultEmptyMap[dir]

    # print "-----------------"
    # for empfile in ffResults.emptyFiles:
    #     dirname, empfile = getFilenameonly(empfile, ffResults.pattern)
    #     print "empty in: ", dirname, " file :", empfile


    # for dirsOut in ffOutput.dirmap:
    #     if dirsOut in ffResults.dirmap:
    #         filemapResult = ffResults.dirmap[dirsOut]
    #         filemapOut =  ffOutput.dirmap[dirsOut]
    #         print "Directory------ : ", dirsOut
    #         for file1 in filemapOut:
    #             print file1
    #             if (not file1 in filemapResult):
    #                 print "File not in REsults : ",dirsOut, " filename : ", file1
    #
    #         print "file list from results :"
    #         for file1 in filemapResult:
    #             print file1
    #             if (not file1 in filemapOut):
    #                 print "File not in Outputs : ", dirsOut, " filename : ", file1
    #         # for file1 in dirsOut:
    #         #     print "File output: ",file1

    # for dirs1 in ffResults.dirmap:
    #     if (not dirs1 in ffOutput.dirmap):
    #         print "directory absent in output : ", dirs1

