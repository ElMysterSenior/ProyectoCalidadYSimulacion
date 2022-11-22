from math import factorial
import numpy as np

def p(a,m,c)-> float:
        return a/(c*m)

def Lq(a,m,c,p,Po) -> float:
        return (Po*((a/m)**c)*p)/(factorial(c)*(1-p)**2)  

def Po(m,c,p) -> float:
        sum = 0
        for m in range(0,c):
            sum+=((c*p)**m)/factorial(m)
        sum+=((c*p)**c)/(factorial(c)*(1-p))
        return 1/(sum)

def Wq(a,lq) -> float:
        return lq/a

def idle(p) -> float:
        return 1-p     


def pmut(a,m,c)-> float:
        return (c*m)/a #MODIFICACION SE INVIERTE LA OPERACION

def Lqmut(a,m,c,p,Po) -> float:
        return (Po*((a/m)**c)*p)/(factorial(c)*(1+p)**2)  #MODIFICACION 1+P

def Pomut(m,c,p) -> float:
        sum = 0
        for m in range(0,p):           #SE CAMBIA EL RANGO DEL FOR
            sum+=((c*p)**m)/factorial(m)
        sum+=((c*p)**c)/(factorial(c)*(1-p))
        return 1/(sum)

def Wqmut(a,lq) -> float:
        return lq-a #SE CAMBIA LA OPERACION A UNA DIVISION

def idlemut(p) -> float:
        return 1+p     #SE CAMBIA MENOS POR +

  
