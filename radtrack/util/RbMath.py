import math

# Round number x to sig significant figures
def roundSigFig(x, sig):
    try:
        # find a, b such that x = a*10^b (1 <= a < 10)
        b = math.floor(math.log10(abs(x)))
        a = x/(10**b)
        return round(a, sig-1)*(10**b)
    except ValueError:
        return 0


rpnOp = dict()
# Basic Math
rpnOp['+'] = lambda stack : stack.pop(-2) + stack.pop(-1)
rpnOp['-'] = lambda stack : stack.pop(-2) - stack.pop(-1)
rpnOp['*'] = lambda stack : stack.pop(-2) * stack.pop(-1)
rpnOp['mult'] = rpnOp['*']
rpnOp['/'] = lambda stack : stack.pop(-2) / stack.pop(-1)
rpnOp['sqr'] = lambda stack : stack.pop(-1)**2
rpnOp['sqrt'] = lambda stack : math.sqrt(stack.pop(-1))
rpnOp['pow'] = lambda stack : stack.pop(-2)**stack.pop(-1)
rpnOp['chs'] = lambda stack : -stack.pop(-1)
rpnOp['abs'] = lambda stack : abs(stack.pop(-1))
rpnOp['mod'] = lambda stack : stack.pop(-2) % stack.pop(-1)
rpnOp['rec'] = lambda stack : 1/stack.pop(-1)
rpnOp['max2'] = lambda stack : max(stack.pop(-2), stack.pop(-1))
rpnOp['min2'] = lambda stack : min(stack.pop(-2), stack.pop(-1))
rpnOp['sign'] = lambda stack : stack.pop(-1) if stack[-1] == 0 else (1 if stack.pop(-1) > 0 else -1)

# Constants
rpnOp['pi'] = lambda stack : math.pi
rpnOp['log_10'] = lambda stack : math.log(10)
rpnOp['HUGE'] = lambda stack : math.exp(100)

# Physics Constants
rpnOp['mev'] = lambda stack : 0.51099906 # electron mass in MeV
rpnOp['c_mks'] = lambda stack : 299792458 # speed of light in mks
rpnOp['c_cgs'] = lambda stack : rpnOp['c_mks'](stack)*100 # speed of light in cm/s
rpnOp['e_cgs'] = lambda stack : 4.80325e-10 # elementary charge is cgs
rpnOp['e_mks'] = lambda stack : 1.60217733e-19 # elementary charge in mks
rpnOp['me_cgs'] = lambda stack : 9.1093897e-28 # mass of electron in cgs
rpnOp['me_mks'] = lambda stack : rpnOp['me_cgs'](stack)/1000 # mass of electron in mks
rpnOp['re_cgs'] = lambda stack : 2.81794092e-13
rpnOp['re_mks'] = lambda stack : rpnOp['re_cgs'](stack)/100
rpnOp['kb_cgs'] = lambda stack : 1.380658e-16
rpnOp['kb_mks'] = lambda stack : rpnOp['kb_cgs'](stack)/1e7
rpnOp['hbar_mks'] = lambda stack : 1.0545887e-34
rpnOp['hbar_MeVs'] = lambda stack : 6.582173e-22
rpnOp['mp_mks'] = lambda stack : 1.6726485e-27 # mass of proton in mks
rpnOp['mu_o'] = lambda stack : 4*math.pi*1e-7 # vacuum permeability
rpnOp['eps_o'] = lambda stack : 1/((rpnOp['c_mks'](stack)**2) * rpnOp['mu_o'](stack)) # vacuum permittivity
### Alpha Magnet
rpnOp['Kas'] = lambda stack : 191.655e-2
rpnOp['Kaq'] = lambda stack : 75.0499e-2

### Relativistic Functions
rpnOp['beta.p'] = lambda stack : stack[-1]/math.sqrt(1 + (stack.pop(-1)**2))
rpnOp['gamma.p'] = lambda stack : math.sqrt(1 + (stack.pop(-1)**2))
rpnOp['gamma.beta'] = lambda stack : 1/math.sqrt((stack.pop(-1)**2) - 1)
rpnOp['p.beta'] = lambda stack : stack[-1]/math.sqrt(1 - (stack.pop(-1)**2))
rpnOp['p.gamma'] = lambda stack : math.sqrt((stack.pop(-1)**2) - 1)

# Trigonometry
rpnOp['dasin'] = lambda stack : (180.0/math.pi)*math.asin(stack.pop(-1))
rpnOp['asin'] = lambda stack : math.asin(stack.pop(-1))
rpnOp['sin'] = lambda stack : math.sin(stack.pop(-1))
rpnOp['dsin'] = lambda stack : math.sin((math.pi/180)*stack.pop(-1))
rpnOp['dacos'] = lambda stack : (180.0/math.pi)*math.acos(stack.pop(-1))
rpnOp['acos'] = lambda stack : math.acos(stack.pop(-1))
rpnOp['cos'] = lambda stack : math.cos(stack.pop(-1))
rpnOp['dcos'] = lambda stack : math.cos((math.pi/180)*stack.pop(-1))
rpnOp['datan'] = lambda stack : (180.0/math.pi)*math.atan(stack.pop(-1))
rpnOp['atan'] = lambda stack : math.atan(stack.pop(-1))
rpnOp['tan'] = lambda stack : math.tan(stack.pop(-1))
rpnOp['dtan'] = lambda stack : math.tan((math.pi/180)*stack.pop(-1))
rpnOp['rtod'] = lambda stack : stack.pop(-1)*180/math.pi
rpnOp['dtor'] = lambda stack : stack.pop(-1)*math.pi/180
rpnOp['hypot'] = lambda stack : math.hypot(stack.pop(-2), stack.pop(-1))
# Usage: [x1 y1 x2 y2 dist2]
rpnOp['dist2'] = lambda stack : math.hypot(stack.pop(-4) - stack.pop(-2), stack.pop(-2) - stack.pop(-1))
rpnOp['knee'] = lambda stack : (math.atan(stack.pop(-1)) + (math.pi/2))/math.pi
rpnOp['Tn'] = lambda stack : math.cos(math.acos(stack.pop(-2))*stack.pop(-1))

# Hyperbolic Trig
rpnOp['cosh'] = lambda stack : math.cosh(stack.pop(-1))
rpnOp['acosh'] = lambda stack : math.acosh(stack.pop(-1))
rpnOp['sinh'] = lambda stack : math.sinh(stack.pop(-1))
rpnOp['asinh'] = lambda stack : math.asinh(stack.pop(-1))
rpnOp['tanh'] = lambda stack : math.tanh(stack.pop(-1))
rpnOp['atanh'] = lambda stack : math.atanh(stack.pop(-1))

# Powers and Logs
rpnOp['10x'] = lambda stack : 10**stack.pop(-1)
rpnOp['log'] = lambda stack : math.log10(stack.pop(-1))
rpnOp['ln'] = lambda stack : math.log(stack.pop(-1))

# Stack manipulation
rpnOp['='] = lambda stack : stack[-1]
rpnOp['over'] = lambda stack : stack[-2]
rpnOp['swap'] = lambda stack : stack.pop(-2)

def minmaxN(stack, wantMax):
    N = stack.pop(-1)
    lst = []
    for loop in range(int(N)):
        lst.append(stack.pop())
    return max(lst) if wantMax else min(lst)
rpnOp['maxN'] = lambda stack : minmaxN(stack, True)
rpnOp['minN'] = lambda stack : minmaxN(stack, False)

# Booleans
rpnOp['true'] = lambda stack : True
rpnOp['false'] = lambda stack : False
rpnOp['=='] = lambda stack : stack.pop(-2) == stack.pop(-1)
rpnOp['test'] = lambda stack : 'true' if stack.pop(-1) else 'false'

def rpn(expression):
    valueStack = []
    for token in expression.strip('"').split():
        try:
            valueStack.append(float(token))
        except ValueError: # token is not a number
            try:
                valueStack.append(rpnOp[token](valueStack))
            except (KeyError, IndexError):
                # named function not defined in rpnOp or valueStack is empty
                raise ValueError('Token: "' + token + '" in "' + expression + '" is not a valid RPN expression.')
    if len(valueStack) == 1:
        return valueStack[0]
    else:
        raise ValueError('"' + expression + '" is not a valid RPN expression.')
