import CompareEqlist as o
file1 = 'server11_ifiles/results/OUT-MHOOK-AHOOK.txt'
file2 = 'server12_ifiles/results/OUT-MHOOK-AHOOK.txt'

a = o.ocamlMaualHooks(filename=file1)
a.parseFile()


b = o.ocamlMaualHooks(filename=file2)
b.parseFile()

hooksAdded = 0
hooksRemoved = 0

AddedmHooks = 0
RemovedmHooks = 0
ChangedmHooks = 0
mhookConsAdded = 0
mhookConsRemoved = 0
autoHookMismatch = 0

def isSameAutoHook(ahook,bhook):
    if ahook.hook == bhook.hook and ahook.fileName == bhook.fileName:
        if ahook.fileName.startswith('Stm'):
            if ahook.stmt == bhook.stmt:
                return True
        else:
            return True
    return False

#use fileMap
for afile in a.fileMap:
    aManHooks = a.fileMap[afile]
    try:
        b.fileMap[afile]
    except KeyError:
        print "File does not exist in B"
        continue
    bManHooks = b.fileMap[afile]
#for every manual hook
    print "-"*20
    print "Filename :" , afile
    print "Hooks in A :",len(aManHooks)
    print "Hooks in B :", len(bManHooks)
    #   compare anything here? number of automated hooks, print if changed

    for i in range(len(aManHooks)):
        if not aManHooks[i] != bManHooks:
            hooksRemoved += 1
            print "Manual hook removed :", aManHooks[i].hook, ' ', aManHooks[i].fileName, ' ', aManHooks[i].line
        else:
            #   for every autohook
            temp = bManHooks.index(aManHooks[i])
            if len(aManHooks[i].Autohooks) == len(bManHooks[temp].Autohooks):
                for aAutoHook in aManHooks[i].Autohooks:
                    for bAutoHook in bManHooks[temp].Autohooks:
                        if isSameAutoHook(aAutoHook, bAutoHook):

                            aOperands = [s.operand for s in aAutoHook.SSOs]
                            bOperands = [s.operand for s in bAutoHook.SSOs]

                            for operand in aOperands:
                                if operand not in bOperands:
                                    print " "*8,
                                    print "Operand Removed:", operand
                            for operand in bOperands:
                                if operand not in aOperands:
                                    print " "*8,
                                    print "Operand Added:", operand

                            aAutoHook.SSOs == bAutoHook.SSOs


            else:
                autoHookMismatch += abs(len(aManHooks[i].Autohooks) - len(bManHooks[temp].Autohooks))
    print "AutoHook mismatch :", autoHookMismatch
    autoHookMismatch = 0
    for i in range(len(bManHooks)):
        if not bManHooks[i] in aManHooks:
            hooksAdded += 1
            print "Manual hook added :", bManHooks[i].hook, ' ', bManHooks[i].fileName, ' ', bManHooks[i].line



#      compare anything here? number of ssos and doms
#       for every SSO
#             compare every operand and operation
#       for every dom
#           compare anything here? number of ssos
#           for every SSO
#               compare every operand and operation
