from radtrack.RbUtility import insideQuote

def test_inside_quote():
    s = '"ab"de"hi"kl\\"o'
    test = [insideQuote(s, i) for i in range(len(s))]
    #           "     a     b     "      d      e      "     h     i     "      k      l      \      "      o
    expected = [True, True, True, False, False, False, True, True, True, False, False, False, False, False, False]
    assert test == expected
