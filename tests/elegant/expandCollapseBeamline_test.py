from radtrack.beamlines.RbElegantElements import expandBeamline, collapseBeamline

print "Elegant Expand/Collapse Beamline Test ..."
testCases = [
             (["A"], "A"),
             (["A", "A"], "2*A"),
             (["A", "B", "A", "A", "B", "A"], "2*(A, B, A)"),
             (["A", "B", "A", "B", "A", "B", "A", "B", "A", "B", "A"], "5*(A, B), A"),
             (84*["A"], "84*A"),
             (["a", "b", "a", "a", "b", "a", "c", "c", "c", "c", "c"], "2*(a, b, a), 5*c"),
             (4*(["E"] + 6*["A", "B", "C"] + 2*["D"]), "4*(E, 6*(A, B, C), 2*D)"),
             (6*(["E"] + 6*["A", "B", "C"] + 2*["D"]), "6*(E, 6*(A, B, C), 2*D)"),
             (5*(["E"] + 6*["A", "B", "C"] + 2*["D"]), "5*(E, 6*(A, B, C), 2*D)")
             ]

fail = False
for case in testCases:
    if collapseBeamline(case[0][:]) != case[1]: 
        print "Not ideal collapse:\n", case[0], "-->", collapseBeamline(case[0][:]), "instead of", case[1]
        fail = True

    if expandBeamline(collapseBeamline(case[0][:])) != case[0]:
        print "Expand(Collapse()) not an identity."
        print expandBeamline(collapseBeamline(case[0][:])), '-->', case[0]
        fail = True

    if case[0] != expandBeamline(case[1]):
        print "Incorrect expansion:\n", case[1], "-->", expandBeamline(case[1]), "instead of", case[0]
        fail = True

    if collapseBeamline(expandBeamline(case[1])) != case[1]:
        print "Collapse(Expand()) not an identity."
        print collapseBeamline(expandBeamline(case[1])), "-->", case[1]
        fail = True

if fail:
    raise Exception

print "Passed"
