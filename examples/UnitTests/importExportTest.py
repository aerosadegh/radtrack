print 'Import/Export test ...'

import os, glob, rbcbt, sys

currentDirectory = os.getcwd()
os.chdir('external\\elegant')

exportEnd = '_export.lte'

if len(sys.argv) > 1:
    fileList = sys.argv[1:]
else:
    ignoreList = ['beamlines\\case_line.lte', 'beamlines\\name_test.lte']
    particleFileList = [fileName for fileName in glob.glob('beamlines\\*.lte') \
        if fileName not in ignoreList \
        and not fileName.endswith(exportEnd)]

    opticalFileList = glob.glob('optics\\*.rad')

    fileLists = [particleFileList, opticalFileList]
    styles = ['particle', 'laser']

# Test that importing an .lte file and an exported version of that file
# result in the same elements being created
try:
    for fileList, style in zip(fileLists, styles):
        for fileName in fileList:
            loader = rbcbt.RbCbt(style, None)
            loader.importFile(fileName)
            exportFileName = os.path.splitext(fileName)[0] + exportEnd
            loader.exportToFile(exportFileName)

            loader2 = rbcbt.RbCbt(style, None)
            loader2.importFile(exportFileName)

            if len(loader.elementDictionary) != len(loader2.elementDictionary):
                print fileName
                print "Reimporting created different number of elements."
                raise Exception

            for (element1, element2) in \
                    zip(loader.elementDictionary.values(), \
                        loader2.elementDictionary.values()):
                if element1 != element2:
                    print fileName
                    print element1.componentLine()
                    print element2.componentLine()
                    raise Exception

            os.remove(exportFileName)

    print "Passed."
finally:
    os.chdir(currentDirectory)

