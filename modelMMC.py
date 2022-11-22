
from math import factorial
import numpy as np

class ModelMMC:
    def __init__(self,a,miu,servers):
        self.ar = a
        self.miu = miu
        self.ser = servers
    #Utilizacion
    def p(self) -> float:
        a=self.ar
        m=self.miu
        c=self.ser
        return a/(c*m)
    #Clientes en el sistema
    def L(self) -> float:
        a=self.ar
        return a*self.W()
    #Clientes en la cola
    def Lq(self) -> float:
        a=self.ar
        m=self.miu
        c=self.ser
        p = self.p()
        Po = self.Po()
        return (Po*((a/m)**c)*p)/(factorial(c)*(1-p)**2)
    #Probabilidad de 0 clientes en el sistema
    def Po(self) -> float:
        a=self.ar
        m=self.miu
        c=self.ser
        p = self.p()
        sum = 0
        for m in range(0,c):
            sum+=((c*p)**m)/factorial(m)
        sum+=((c*p)**c)/(factorial(c)*(1-p))
        return 1/(sum)
    #Espera en el sistema
    def W(self) -> float:
        m=self.miu
        return self.Wq()+(1/m)
    #Espera en la cola Wq
    def Wq(self) -> float:
        a=self.ar
        return self.Lq()/a
    #Service idle
    def idle(self) -> float:
        return 1-self.p()
    
    def __str__(self) -> str:
        return f"L:{format(self.L(), '.4f')} Lq:{format(self.Lq(), '.4f')} W:{format(self.W(), '.4f')} Wq:{format(self.Wq(), '.4f')} Po:{format(self.Po(), '.4f')} p:{format(self.p(), '.4f')} idle:{format(self.idle(), '.4f')}"

class JacksonNet:
    def __init__(self,colasMMC:list()):
        self.colasMMC = colasMMC
    def L(self):
        sum = 0
        for cola in self.colasMMC:
            sum += cola.L()
        return sum
    def Lq(self):
        sum = 0
        for cola in self.colasMMC:
            sum += cola.Lq()
        return sum
    def W(self):
        sum = 0
        for cola in self.colasMMC:
            sum += cola.W()
        return sum
    def Wq(self):
        sum = 0
        for cola in self.colasMMC:
            sum += cola.Wq()
        return sum
    def __str__(self) -> str:
        return f"L:{format(self.L(), '.4f')} Lq:{format(self.Lq(), '.4f')} W:{format(self.W(), '.4f')} Wq:{format(self.Wq(), '.4f')}"
def solve(a,b):
    '''
    #Tasas de llegada
    #Lambda = arrivals + t(p) * Lambda
    #     -Arrivals =  t(p)*Lambda - Lambda
    # No se puede restar puesto que no es de dimensiones identicas,
    # entonces se usa una matriz auxiliar para relizar la resta
    #     -Arrivals =  t(p)*Lambda - aux
    
    Se obtiene una matriz de resultados y tambien una matriz de coeficientes 
    por lo que se puede obtener una matriz de resultados con las 
    tasas de llegada a cada nodo tomando en cuenta las entradas 
    externas e internas del sistema
    '''
    aux = ([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    x = np.linalg.solve(a.transpose()-aux, -b)
    return x





