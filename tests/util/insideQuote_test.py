from radtrack.util.stringTools import insideQuote

def test_inside_quote():
    s = '"ab"de"hi"kl\\"o\\\\"p'
    test = [insideQuote(s, i) for i in range(len(s))]
    #           "     a     b     "      d      e      "     h     i     "      k      l      \      "      o      \      \      "     p
    expected = [True, True, True, False, False, False, True, True, True, False, False, False, False, False, False, False, False, True, True]
    assert test == expected
