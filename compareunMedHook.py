import CompareEqlist as o



file1 = '../server16_ifiles/results/OUT-MHOOK-AHOOK.txt'
file2 = '../server17_ifiles/results/OUT-MHOOK-AHOOK.txt'

a = o.ocamlMaualHooks(filename=file1)
a.parseFile()


b = o.ocamlMaualHooks(filename=file2)
b.parseFile()

hooksAdded = 0
hooksRemoved = 0
hookPresent = False

print "------------"
for unmed in a.unmediatedHooks:
    for bunmed in b.unmediatedHooks:
        if unmed.hook == bunmed.hook and unmed.fileName == bunmed.fileName:
            if unmed.ifStmt and bunmed.ifStmt:
                if unmed.stmt == unmed.stmt:
                    #print "Hook matched...", unmed
                    hookPresent = True
            else:
                #print "Hook Matched  ",unmed
                hookPresent =  True

    if hookPresent == False:
        if unmed.ifStmt:
            print " Hook removed from B :", unmed.hook, unmed.fileName, unmed.stmt
        else:
            print " Hook removed from B :", unmed.hook, unmed.fileName
        hooksRemoved = hooksRemoved+1
    hookPresent = False

hookPresent = False
for unmed in b.unmediatedHooks:
    for bunmed in a.unmediatedHooks:
        if unmed.hook == bunmed.hook and unmed.fileName == bunmed.fileName:
            if unmed.ifStmt and bunmed.ifStmt:
                if unmed.stmt == unmed.stmt:
                    #print "Hook matched...", unmed
                    hookPresent = True
            else:
                #print "Hook Matched  ",unmed
                hookPresent =  True
    if hookPresent == False:
        if unmed.ifStmt:
            print " Hook added in B :",unmed.hook, unmed.fileName, unmed.stmt
        else:
            print " Hook added in B :", unmed.hook, unmed.fileName
        hooksAdded = hooksAdded +1
    hookPresent = False

print " "
print "Unmediated Hook Added : ", hooksAdded
print "Unmediated Hook Removed : ", hooksRemoved