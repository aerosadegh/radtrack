#stupid genesis file check
import os, sys #, h5py

def main():
    lcls = open('lcls.in','r')
    test = open('test.in','r')
    
    
    def striplist(x):
        for i,f in enumerate(x):
            x[i]=f.strip().strip(',').strip('.')
        return x
        
    def poplist(x):
        for i,f in enumerate(x):
            if f[0] == '$' or not f:
                x.pop(i)
                
    def dblist(x):
        d=[]
        p=[]
        for i in x:
            d1,p1 = i.split('=')
            d.append(d1)
            p.append(p1)
        return d,p
        

        
    def check(x,y):
        for i in x:
            if i not in y:
                print(i)
         
            
        
    beta = striplist(test.readlines())
    alpha = striplist(lcls.readlines())

    poplist(beta)
    poplist(alpha)
    
    bd,bp=dblist(beta)
    ad,ap=dblist(alpha)
    
    #check for diff names
    check(ad,bd)
    #check for diff values
    check(ap,bp)

    #output test file
    #'''
    f = open('newtest.in', 'w+')
    f.write(' $newrun \n')
    for n,i in enumerate(bd):
        if i in ad:
            f.write(' '+i+'='+bp[n]+'\n')
    f.write(' $end \n')
    f.close()
    #'''
    
    lcls.close()
    test.close()
    
main()