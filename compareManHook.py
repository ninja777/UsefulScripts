import CompareEqlist as o



file1 = 'server11_ifiles/results/OUT-MHOOK-AHOOK.txt'
file2 = 'server12_ifiles/results/OUT-MHOOK-AHOOK.txt'

a = o.ocamlMaualHooks(filename=file1)
a.parseFile()


b = o.ocamlMaualHooks(filename=file2)
b.parseFile()

hooksAdded = 0
hooksRemoved = 0
hookPresent = False

# for manhook in a.ManHooks:
#     for bmanhook in b.ManHooks:
#         if manhook.fileName == bmanhook.fileName:
#             print "hooks in file"

AddedmHooks = 0
RemovedmHooks = 0
ChangedmHooks = 0
mhookConsAdded = 0
mhookConsRemoved = 0

filePresent = False

def isSameAutoHook(ahook,bhook):
    if ahook.hook == bhook.hook and ahook.fileName == bhook.fileName:
        if ahook.fileName.startswith('Stm'):
            if ahook.stmt == bhook.stmt:
                return True
        else:
            return True
    return False


def compareAutohooks(aHooks,bHooks):
    for ahook in aHooks:
        for bhook in bHooks:
            if isSameAutoHook(ahook,bhook):
                # compare ssos in matched hooks.
                ahook == bhook
                # print " compare SSOs here"
                #compare number of doms.. is same can recursively call
                #compareAutoHooks(aDoms, bDoms)
                break


#use fileMap
#for every manual hook
#   compare anything here? number of automated hooks, print if changed
#   for every autohook
#      compare anything here? number of ssos and doms
#       for every SSO
#             compare every operand and operation
#       for every dom
#           compare anything here? number of ssos
#           for every SSO
#               compare every operand and operation



for afile in a.fileMap:
    for bfile in b.fileMap:
        if afile == bfile:
            filePresent = True
            print "-----------------"
            print "Hooks in File : ",afile
            ahooknum = len(a.fileMap[afile])
            bhooknum = len(b.fileMap[bfile])
            ahooks = a.fileMap[afile]
            bhooks = b.fileMap[bfile]
            print "Hooks in A : ", len(ahooks)
            # for hook in ahooks:
            #     print hook.hook, hook.fileName, hook.line, len(hook.Autohooks)
            print "Hooks in B : ", len(bhooks)
            # for bhook in bhooks:
            #     print bhook.hook, bhook.fileName, bhook.line, len(bhook.Autohooks)
            if ahooknum != bhooknum:
                print "Hooks different in File  : ", afile
                for hook in ahooks:
                    print ' '* 4,
                    print hook.hook, hook.fileName, hook.line, len(hook.Autohooks)
                print "------- Hooks in B"
                for bhook in bhooks:
                    print ' ' * 4,
                    print bhook.hook, bhook.fileName, bhook.line, len(bhook.Autohooks)
            else:
                for amanHook in ahooks:
                    for bmanHook in bhooks:
                        autoHookCounta = len(amanHook.Autohooks)
                        autoHookCountb = len(bmanHook.Autohooks)
                        if autoHookCounta == autoHookCountb:
                            #Same number of autohooks.
                            compareAutohooks(amanHook.Autohooks,bmanHook.Autohooks)

            break
                #Compare the contained autohooks.. if diff or new constrains
                #check if only
    if filePresent == False:
        print "No hooks in file : ", afile
    filePresent = False


