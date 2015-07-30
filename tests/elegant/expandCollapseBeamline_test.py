from __future__ import print_function, division, unicode_literals, absolute_import
from radtrack.beamlines.RbElegantElements import expandBeamline, collapseBeamline

# In each test case, the first element in the tuple should collapse to the second.
testCases = [
             (["A"], "A"),
             (["A", "A"], "2*A"),
             (["A", "B", "A", "A", "B", "A"], "2*(A, B, A)"),
             (["A", "B", "A", "B", "A", "B", "A", "B", "A", "B", "A"], "5*(A, B), A"),
             (84*["A"], "84*A"),
             (["a", "b", "a", "a", "b", "a", "c", "c", "c", "c", "c"], "2*(a, b, a), 5*c"),
             (4*(["E"] + 6*["A", "B", "C"] + 2*["D"]), "4*(E, 6*(A, B, C), 2*D)"),
             (6*(["E"] + 6*["A", "B", "C"] + 2*["D"]), "6*(E, 6*(A, B, C), 2*D)"),
             (5*(["E"] + 6*["A", "B", "C"] + 2*["D"]), "5*(E, 6*(A, B, C), 2*D)"),
             (["-B", "-B", "-B"], "-3*B"),
             (["-B", "-B", "-B", "-B"], "-4*B"),
             (["-B", "-B", "-B", "-B", "-B", "-B", "-B", "-B", "-B", "-B"], "-10*B"),
             ]

def test_beamline_expand_collapse():
    for case in testCases:
        assert collapseBeamline(case[0][:]) == case[1]
        assert expandBeamline(case[1][:]) == case[0] 
