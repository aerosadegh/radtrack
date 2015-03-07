print 'Strip comments test ...'
from RbUtility import stripComments

inputString  = 'This is a test that "#" is treated as a comment. # This should not appear.'
outputString = 'This is a test that "#" is treated as a comment.'

stripString = stripComments(inputString, '#')

if stripString != outputString:
    print inputString
    print stripString
    print outputString
    raise Exception
print 'Passed.'
