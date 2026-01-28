import numpy as np
import sympy as sp
import pandas as pd
from sympy.parsing.sympy_parser import parse_expr

def getExpRoot(x, exp, err, xLow, xHigh):
    f = spExp(exp)
    iter = 0
    table = {"Iteration" : [],
             "xLow" : [],
             "xUp" : [],
             "xMid" : [],
             "f(xMid)" :[],
             "Ea" : [f"{np.nan}"]}
    Ea = 100
    while(Ea > err):
        iter += 1
        if(iter != 1):
            oldXMid = newXMid
        table['Iteration'].append(iter)
        table['xLow'].append(xLow)
        table['xUp'].append(xHigh)
        newXMid = (xLow + xHigh)/2
        table['xMid'].append(newXMid)
        fXMid = f.subs(x, newXMid)
        table['f(xMid)'].append(fXMid)
        if(iter != 1):
            Ea = (abs(newXMid - oldXMid)/newXMid) * 100
            table['Ea'].append(f"{Ea} %")
        if(float(fXMid) < 0):
            xLow = newXMid
        elif(float(fXMid) > 0):
              xHigh = newXMid
        else:
            break
    
    df = pd.DataFrame(table)
    return {"Root" : newXMid, "Table" : df}
    


def isInBound(xLow, xUp, x, f):
    if (f.subs(x, xLow) * f.subs(x, xUp) <= 0):
        return True
    else:
        return False
    
def spExp(exp):
    return parse_expr(exp, transformations='all')



print("--------------------------\n  Bisection Root Finding\n--------------------------")

x = sp.symbols('x')

exp = input("Enter a function in terms of x:\t")

minError = float(input("\nEnter the minimum error percentage permissible:\t"))

while True:
    xLow = sp.sympify(input("\nEnter the lower bound to start with:\t"), locals = {"pi"  : sp.pi, "e" : sp.E})
    xUp = sp.sympify(input("\nEnter the upper bound to start with:\t"), locals = {"pi"  : sp.pi, "e" : sp.E})
    if(isInBound(xLow, xUp, x, spExp(exp))):
        break
    print(f"\nThe root isn't within the given bounds, please give another interval:\n")

res = getExpRoot(x, exp, minError, xLow, xUp)

print(f"\n{res['Table']}\n\nThe closest approximation for the root with the given minimum error = {minError} is x = {res['Root']}")
