import outputFileParsing as o


printErrorCases = False
printUnresolved = False
printMismatched = False



def getCallInst(callName):
    if len(callName) > 0 and callName[0] == '[':
        callName = callName[callName.index(']') + 1:]
        callName = callName.strip(' ')
    return callName

def getFileandDirnameonly(filename,pattern):
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
    ffOutput = o.fileFormat(baseDirectory='Analyzed', outputDirectory='output', verbose=False, pattern='.out2', excludePattern='.opt.out')
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

    # print " Error Calls : ", len(ffOutput.errCalls)
    # print ffOutput.errCalls

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

    print " Error Calls : ", len(ffResults.errCalls)
    if printErrorCases:
        for files in  ffResults.indirectErrorCalls:
            if len(ffResults.indirectErrorCalls[files]) > 0:
                print ffResults.indirectErrorCalls[files]

    outEmptyMap = {}
    resultEmptyMap = {}

    # Set up for comparison of empty files.
    for empfile in ffOutput.emptyFiles:
        dirname, empfile = getFileandDirnameonly(empfile,ffOutput.pattern)
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
        dirname, empfile = getFileandDirnameonly(empfile, ffResults.pattern)
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
            print "Empty files only in Result : ", dir, resultEmptyMap[dir]


    #set up for comparing the empty targets in each set of results.

    outDirmaps = {}
    resultDirmaps = {}
    CallSites = []

    if printUnresolved:
        for dirs in ffOutput.callSitesWithNoTargets:
            if len(dirs) > 0:
                dirname, fileName = getFileandDirnameonly(dirs[0],ffOutput.pattern)
                callInst = getCallInst(dirs[1])
                if(dirname in outDirmaps):
                    CallSites = outDirmaps[dirname]
                    CallSites.append([fileName,callInst])
                    outDirmaps[dirname] = CallSites
                else:
                    CallSites = []
                    CallSites.append([fileName, callInst])
                    outDirmaps[dirname] = CallSites



        for dirs in ffResults.callSitesWithNoTargets:
            if len(dirs) > 0:
                dirname, fileName = getFileandDirnameonly(dirs[0], ffResults.pattern)
                callInst = getCallInst(dirs[1])
                if (dirname in resultDirmaps):
                    CallSites = resultDirmaps[dirname]
                    CallSites.append([fileName, callInst])
                    resultDirmaps[dirname] = CallSites
                else:
                    CallSites = []
                    CallSites.append([fileName, callInst])
                    resultDirmaps[dirname] = CallSites

        #Compare differences in the unresolved indirect calls
        for outdir in outDirmaps:
            if outdir in resultDirmaps:
                #case when directory is result map also.
                for call1 in outDirmaps[outdir]:
                    if not call1 in resultDirmaps[outdir]:
                        print "call site not resolved in Signature :", outdir, call1
                for call2 in resultDirmaps[outdir]:
                    if not call2 in outDirmaps[outdir]:
                        print "Call site not resolved in Func Pointer :",outdir, call2
            else:
                for call1 in outDirmaps[outdir]:
                    print "Call site not resolved in Func Pointer :", outdir, call1

        for resdir in resultDirmaps:
            if not resdir in outDirmaps:
                for call1 in resultDirmaps[resdir]:
                    print "call site not resolved in Signature :", resdir,call1


    # Find differences in call sites.. all !!!
    # Again for the same dir, same files, check if all the callsites match..
    # else print the recognized ones in one vs the other.


    # for call1 in ffOutput.indirectCalls:
    #     print call1, len(ffOutput.indirectCalls[call1]), ffOutput.indirectCalls[call1]

    print " "
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print  " "
    print  " "


    for outdir in ffOutput.dirmap:
        if outdir in ffResults.dirmap:
            # case when directory is result map also.
         #   print "Dir    : ",outdir
            for filemap in ffOutput.dirmap[outdir]:
                if filemap in ffResults.dirmap[outdir]:
           #         print filemap
                    for indcall in ffOutput.dirmap[outdir][filemap]:
                        if not indcall in ffResults.dirmap[outdir][filemap]:
                            print "Indirect call not recognized in Func Pointer : ",outdir, filemap, indcall
                    for indcall in ffResults.dirmap[outdir][filemap]:
                        if not indcall in ffOutput.dirmap[outdir][filemap]:
                            print "Indirect call not recognized in Signature : ",outdir, filemap, indcall
                else:
                    print "--------File not found in Results", filemap
        else:
            print "=========Dir not found in Results", outdir

                    #check all call sites in each files..



    #     print dirs

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

