import CompareEqlist as o



file1 = '../server16_ifiles/results/OUTPUTMLS-SUBSUMP.txt'
file2 = '../server17_ifiles/results/OUTPUTMLS-SUBSUMP.txt'

a = o.subSumptionClass(filename=file1)
a.parseFile()


b = o.subSumptionClass(filename=file2)
b.parseFile()

eqlistPresent = False
OperationPresent = False
OperandPresent = False

applyFilter = True

removedClasses = 0
addedClasses = 0
OperationsAdded = 0
OperationsRemoved = 0
replacedSMA = 0
SMAAdded = 0
SMARemoved = 0
replacedOps =0


allRead = True
allWrite = True
mix = True

def FilterOps(operations):
    writec =0
    readc = 0
    if len(operations) == 0:
        return 0,0,0
    for op in operations:
        opType = op.split('(')[0]
        if opType == 'write':
            writec = writec+1
        else:
            readc =readc+1
    if writec == len(operations):
        return 0,1,0
    elif readc == len(operations):
        return 1,0,0
    else:
        return 0,0,1




#if the first element matches then all other operands and ops should be present...

for aeqlists in a.eqList:
   # print aeqlists
    for beqlists in b.eqList:
        #check if eqlist in a is present in b
        if aeqlists[0].operand == beqlists[0].operand:
            #check if all operations match..
            if aeqlists[0].operations == beqlists[0].operations:
                #eqclass match.. check for others.
                eqlistPresent = True
                # check for new operand in eqlist.. or new operation in some operands..
                for aeq in aeqlists:
                    for beq in beqlists:
                        if aeq.operand == beq.operand:
                            OperandPresent = True
                            if aeq.operations == beq.operations:
                                OperationPresent = True

                    if OperandPresent == True and OperationPresent == False:
                        # operand present but same ops not present..:
                        for beq in beqlists:
                            if aeq.operand == beq.operand:
                                if aeq.operations != beq.operations:
                                    if len(aeq.operations) < len(beq.operations):
                                        if applyFilter:
                                            addedops = list(set(aeq.operations) - set(beq.operations))
                                            if FilterOps(aeqlists[0].operations) != FilterOps(addedops):
                                                print "------------"
                                                print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                                    aeqlists[0].operand, aeqlists[0].operations
                                                print "A : ", aeq.operations
                                                print "B : ", beq.operations
                                                SMAAdded = SMAAdded + 1
                                            elif FilterOps(addedops)[2] == 1:
                                                print "------------"
                                                print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                                    aeqlists[0].operand, aeqlists[0].operations
                                                print "A : ", aeq.operations
                                                print "B : ", beq.operations
                                                SMAAdded = SMAAdded + 1
                                        else:
                                            print "------------"
                                            print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                                aeqlists[0].operand, aeqlists[0].operations
                                            print "A : ", aeq.operations
                                            print "B : ", beq.operations
                                            SMAAdded = SMAAdded + 1
                                    elif len(beq.operations) < len(aeq.operations):
                                        print "------------"
                                        print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                            aeqlists[0].operand, aeqlists[0].operations
                                        print "A : ", aeq.operations
                                        print "B : ", beq.operations
                                        SMARemoved = SMARemoved + 1
                                    elif len(aeq.operations) == len(beq.operations):
                                        print "------------"
                                        print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                            aeqlists[0].operand, aeqlists[0].operations
                                        print "A : ", aeq.operations
                                        print "B : ", beq.operations
                                        replacedSMA = replacedSMA + 1
                                        SMARemoved = SMARemoved + 1
                                        SMAAdded = SMAAdded + 1

                                    # print "B : ", beq.operations
                    OperationPresent = False
                    if OperandPresent == False:
                        if applyFilter:
                            if FilterOps(aeqlists[0].operations) != FilterOps(aeq.operations):
                                OperationsRemoved = OperationsRemoved + 1
                                if len(aeqlists) <= len(beqlists):
                                    replacedOps = replacedOps + 1
                                print "-----------"
                                print "New Operand in A: subsumed by: ", aeqlists[0].operand, aeqlists[0].operations
                                print aeq.operand, "--", aeq.operations
                            elif FilterOps(aeq.operations)[2] == 1:
                                OperationsRemoved = OperationsRemoved + 1
                                if len(aeqlists) <= len(beqlists):
                                    replacedOps = replacedOps + 1
                                print "-----------"
                                print "New Operand in A: subsumed by: ", aeqlists[0].operand, aeqlists[0].operations
                                print aeq.operand, "--", aeq.operations
                        else:
                            OperationsRemoved = OperationsRemoved + 1
                            if len(aeqlists) <= len(beqlists):
                                replacedOps = replacedOps + 1
                            print "-----------"
                            print "New Operand in A: subsumed by: ", aeqlists[0].operand, aeqlists[0].operations
                            print aeq.operand, "--", aeq.operations
                    OperandPresent = False
    if eqlistPresent == False:
        if applyFilter:
            if FilterOps(aeqlists[0].operations) != FilterOps(aeq.operations):
                removedClasses = removedClasses + 1
                print "-----------"
                print "Subsumption only in A : "
                for aeq in aeqlists:
                    print aeq.operand, "--", aeq.operations
            elif FilterOps(aeq.operations)[2] == 1:
                removedClasses = removedClasses + 1
                print "-----------"
                print "Subsumption only in A : "
                for aeq in aeqlists:
                    print aeq.operand, "--", aeq.operations
        else:
            removedClasses = removedClasses + 1
            print "-----------"
            print "Subsumption only in A : "
            for aeq in aeqlists:
                print aeq.operand, "--", aeq.operations
    eqlistPresent = False

for aeqlists in b.eqList:
    # print aeqlists
    for beqlists in a.eqList:
        # check if eqlist in a is present in b
        if aeqlists[0].operand == beqlists[0].operand:
            # check if all operations match..
            if aeqlists[0].operations == beqlists[0].operations:
                # eqclass match.. check for others.
                eqlistPresent = True
                #check for new operand in eqlist.. or new operation in some operands..
                for aeq in aeqlists:
                    for beq in beqlists:
                        if aeq.operand == beq.operand:
                            OperandPresent = True
                            if aeq.operations == beq.operations:
                                OperationPresent = True

                    if OperandPresent == True and OperationPresent == False:
                        #operand present but same ops not present..:

                        for beq in beqlists:
                            if aeq.operand == beq.operand:
                                if aeq.operations != beq.operations:
                                    if len(aeq.operations) > len(beq.operations):
                                        if applyFilter:
                                            addedops = list(set(aeq.operations) - set(beq.operations))
                                            if FilterOps(aeqlists[0].operations) != FilterOps(addedops):
                                                print "------------"
                                                print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                                    aeqlists[0].operand, aeqlists[0].operations
                                                print "B : ", aeq.operations
                                                print "A : ", beq.operations
                                                SMAAdded = SMAAdded + 1
                                            elif FilterOps(addedops)[2] == 1:
                                                print "------------"
                                                print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                                    aeqlists[0].operand, aeqlists[0].operations
                                                print "B : ", aeq.operations
                                                print "A : ", beq.operations
                                                SMAAdded = SMAAdded + 1
                                        else:
                                            print "------------"
                                            print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                                aeqlists[0].operand, aeqlists[0].operations
                                            print "B : ", aeq.operations
                                            print "A : ", beq.operations
                                            SMAAdded = SMAAdded + 1
                                    elif len(beq.operations) > len(aeq.operations):
                                        print "------------"
                                        print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                            aeqlists[0].operand, aeqlists[0].operations
                                        print "B : ", aeq.operations
                                        print "A : ", beq.operations
                                        SMARemoved = SMARemoved + 1
                                    elif len(aeq.operations) == len(beq.operations):
                                        print "------------"
                                        print "Mismatch operations for operand : ", aeq.operand, " in Subsumption of: ", \
                                            aeqlists[0].operand, aeqlists[0].operations
                                        print "B : ", aeq.operations
                                        print "A : ", beq.operations
                                        replacedSMA = replacedSMA + 1
                                        SMARemoved = SMARemoved + 1
                                        SMAAdded = SMAAdded + 1
                        #print "B : ", beq.operations
                    OperationPresent = False
                    if OperandPresent == False:
                        if applyFilter:
                            if FilterOps(aeqlists[0].operations) != FilterOps(aeq.operations):
                                OperationsAdded = OperationsAdded +1
                                if len(aeqlists) <= len(beqlists):
                                    replacedOps = replacedOps + 1
                                print "-----------"
                                print "New Operand in B: subsumed by: ", aeqlists[0].operand, aeqlists[0].operations
                                print aeq.operand, "--", aeq.operations
                            elif FilterOps(aeq.operations)[2] == 1:
                                OperationsAdded = OperationsAdded + 1
                                if len(aeqlists) <= len(beqlists):
                                    replacedOps = replacedOps + 1
                                print "-----------"
                                print "New Operand in B: subsumed by: ", aeqlists[0].operand, aeqlists[0].operations
                                print aeq.operand, "--", aeq.operations
                        else:
                            OperationsAdded = OperationsAdded + 1
                            if len(aeqlists) <= len(beqlists):
                                replacedOps = replacedOps + 1
                            print "-----------"
                            print "New Operand in B: subsumed by: ", aeqlists[0].operand, aeqlists[0].operations
                            print aeq.operand, "--", aeq.operations
                    OperandPresent = False
    if eqlistPresent == False:
        if applyFilter:
            if FilterOps(aeqlists[0].operations) != FilterOps(aeq.operations):
                addedClasses  = addedClasses+1
                print "-----------"
                print "Subsumption only in B : "
                for aeq in aeqlists:
                    print aeq.operand, "--", aeq.operations
            elif FilterOps(aeq.operations)[2] == 1:
                addedClasses = addedClasses + 1
                print "-----------"
                print "Subsumption only in B : "
                for aeq in aeqlists:
                    print aeq.operand, "--", aeq.operations
        else:
            addedClasses = addedClasses + 1
            print "-----------"
            print "Subsumption only in B : "
            for aeq in aeqlists:
                print aeq.operand, "--", aeq.operations
    eqlistPresent = False


print "Filtered :--------- "
print " "
print "----"
print "Removed Subsumptions : ", removedClasses
print "Removed Operations: ", OperationsRemoved
print "Removed SMA       : ",SMARemoved
print "----"
print "Added Subsumptions   : ", addedClasses
print "Added Operations: ", OperationsAdded
print "Added SMA       : ",SMAAdded
print " "
print "SMAs added as well as removed : ",replacedSMA
print "Operations added as well as removed : ", replacedOps

            # for op1 in aeqlists[0].operations:
            #     for op2 in beqlists[0].operations:
            #         if op1 == op2:

     #   print beqlists
     #    for aop in aeqlists:
     #        for bop in beqlists:
     #           if aop.operand == bop.operand:
     #               print "-------------"
     #               print aop.operand
     #               print aop.operations
     #               print bop.operations




#print a.eqList[4][0]