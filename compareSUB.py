import CompareEqlist as o



file1 = '../server11_ifiles/results/OUTPUTMLS-SUBSUMP.txt'
file2 = '../server12_ifiles/results/OUTPUTMLS-SUBSUMP.txt'

a = o.subSumptionClass(filename=file1)
a.parseFile()


b = o.subSumptionClass(filename=file2)
b.parseFile()

eqlistPresent = False
OperationPresent = False
OperandPresent = False

removedClasses = 0
addedClasses = 0
OperationsAdded = 0
OperationsRemoved = 0
replacedSMA = 0
SMAAdded = 0
SMARemoved = 0
replacedOps =0


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
                        print "------------"
                        print "Mismatch operations for operand : ", aeq.operand, " in eqlist of: ", aeqlists[0].operand
                        print "A : ", aeq.operations
                        for beq in beqlists:
                            if aeq.operand == beq.operand:
                                if aeq.operations != beq.operations:
                                    print "B : ", beq.operations
                                    if len(aeq.operations) > len(beq.operations):
                                        SMARemoved = SMARemoved+1
                                    if len(aeq.operations) == len(beq.operations):
                                        replacedSMA = replacedSMA+1
                                        SMARemoved = SMARemoved + 1
                                        SMAAdded = SMAAdded + 1
                                    if len(aeq.operations) < len(beq.operations):
                                        SMAAdded = SMAAdded+1

                                    # print "B : ", beq.operations
                    OperationPresent = False
                    if OperandPresent == False:
                        OperationsRemoved = OperationsRemoved+1
                        if len(aeqlists) <= len(beqlists):
                            replacedOps = replacedOps+1
                        print "-----------"
                        print "New Operand in A: for eqlist of: ", aeqlists[0].operand
                        print aeq.operand, "--", aeq.operations
                    OperandPresent = False
    if eqlistPresent == False:
        removedClasses = removedClasses + 1
        print "-----------"
        print "EQlist only in A : "
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
                        print "------------"
                        print "Mismatch operations for operand : ", aeq.operand, " in eqlist of: ", aeqlists[0].operand
                        print "B : ", aeq.operations
                        for beq in beqlists:
                            if aeq.operand == beq.operand:
                                if aeq.operations != beq.operations:
                                    print "A : ", beq.operations
                                    if len(beq.operations) > len(aeq.operations):
                                        SMARemoved = SMARemoved + 1
                                    if len(aeq.operations) == len(beq.operations):
                                        replacedSMA = replacedSMA + 1
                                        SMARemoved = SMARemoved + 1
                                        SMAAdded = SMAAdded + 1
                                    if len(aeq.operations) > len(beq.operations):
                                        SMAAdded = SMAAdded + 1

                        #print "B : ", beq.operations
                    OperationPresent = False
                    if OperandPresent == False:
                        OperationsAdded = OperationsAdded +1
                        if len(aeqlists) <= len(beqlists):
                            replacedOps = replacedOps + 1
                        print "-----------"
                        print "New Operand in B: for eqlist of: ", aeqlists[0].operand
                        print aeq.operand, "--", aeq.operations
                    OperandPresent = False
    if eqlistPresent == False:
        addedClasses  = addedClasses+1
        print "-----------"
        print "EQlist only in B : "
        for aeq in aeqlists:
            print aeq.operand, "--", aeq.operations
    eqlistPresent = False



print " "
print "----"
print "Removed Classes : ", removedClasses
print "Removed Operations: ", OperationsRemoved
print "Removed SMA       : ",SMARemoved
print "----"
print "Added Classes   : ", addedClasses
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