import unittest
import Exec
import modelMMCadap

#Prueba 1
a=30 #a
miu=40 #m
servers=3 #c

#Prueba 2

a2=15 #a
miu2=20 #m
servers2=5 #c



class test_excec(unittest.TestCase):
    #Suma numeros de posiciones pasadas
    def test_AcumulativeArray(self):
        cases = [
            ([4, 16,5], [4,20,25]),
            ([1, 2,3], [1,3,6]),
        ]

        for inp, expected in cases:
            
            with self.subTest(inp=inp, expected=expected):
                obtained = Exec.getAcumulativeArray(inp)
                self.assertEqual(obtained, expected, "Array(%s) should be %s" % (inp, expected))

class test_modelMMC_adap(unittest.TestCase):
    def test_p(self):
        #Se encarga de sacar la p con la operacion a/(c*m)
        cases = [
            (a,miu,servers,.25),
            (a2,miu2,servers2,.15)
           
        ]

        for inp1, inp2,inp3, expected in cases:
            
            with self.subTest(inp1=inp1, inp2=inp2,inp3=inp3, expected=expected):
                obtained = modelMMCadap.p(inp1,inp2,inp3)
                self.assertEqual(obtained, expected, "p(%s) should be %s" % (inp1,expected))

    def test_Po(self):
        #Se encarga de sacar Po con la operacion ...
        cases = [
            (a,miu,servers,-6.174119866483886e-34),
            (a2,miu2,servers2,-6.438358212912472e-20)
        ]

        for inp1, inp2,inp3, expected in cases:
            
            with self.subTest(inp1=inp1,inp2=inp2,inp3=inp3, expected=expected):
                obtained = modelMMCadap.Po(inp1, inp2,inp3)
                self.assertEqual(obtained, expected, "Po(%s) should be %s" % (inp1,expected))

    def test_Lq(self):
        #Se encarga de sacar Lq con la operacion (Po*((a/m)**c)*p)/(factorial(c)*(1-p)**2
        cases = [
            (a,miu,servers,.25,-6.174119866483886e-34,.014705882), #0.014705882
            (a2,miu2,servers2,.15,-6.438358212912472e-20,0.000193929), #.000193929
            
        ]

        for inp1, inp2,inp3,inp4,inp5, expected in cases:
            
            with self.subTest(inp1=inp1,inp2=inp2,inp3=inp3,inp4=inp4,inp5=inp5, expected=expected):
                obtained = modelMMCadap.Lq(inp1, inp2,inp3,inp4,inp5)
                self.assertEqual(obtained, expected, "Lq(%s) should be %s" % (inp1,expected))
                
    def test_Wq(self):
        #Se encarga de sacar Wq con la operacion lq/a
        cases = [
            (a,0.014705882,0.0004901960666666667), #0.000490196
            (a2,.000193929,1.29286e-05), #0.000012929
            
        ]

        for inp1, inp2, expected in cases:
            
            with self.subTest(inp1=inp1,inp2=inp2, expected=expected):
                obtained = modelMMCadap.Wq(inp1, inp2)
                self.assertEqual(obtained, expected, "Wq(%s) should be %s" % (inp1,expected))

    def test_idle(self):
        #Se encarga de sacar idle con la operacion 1-p
        cases = [
            (.25,.75), 
            (.15,.85),
            
        ]

        for inp1, expected in cases:
            
            with self.subTest(inp1=inp1, expected=expected):
                obtained = modelMMCadap.idle(inp1)
                self.assertEqual(obtained, expected, "idle(%s) should be %s" % (inp1,expected))   

    def test_pmut(self):
        #Se encarga de sacar la p con la operacion a/(c*m)
        cases = [
            (a,miu,servers,.25),  # error por mutacion
            (a2,miu2,servers2,.15) # error por mutacion
           
        ]

        for inp1, inp2,inp3, expected in cases:
            
            with self.subTest(inp1=inp1, inp2=inp2,inp3=inp3, expected=expected):
                obtained = modelMMCadap.pmut(inp1,inp2,inp3)
                self.assertEqual(obtained, expected, "p(%s) should be %s" % (inp1,expected))

    def test_Pomut(self):
        #Se encarga de sacar Po con la operacion ...
        cases = [
            (a,miu,servers,-6.174119866483886e-34), # error por mutacion
            (a2,miu2,servers2,-6.438358212912472e-20)# error por mutacion
        ]

        for inp1, inp2,inp3, expected in cases:
            
            with self.subTest(inp1=inp1,inp2=inp2,inp3=inp3, expected=expected):
                obtained = modelMMCadap.Pomut(inp1, inp2,inp3)
                self.assertEqual(obtained, expected, "Po(%s) should be %s" % (inp1,expected))

    def test_Lqmut(self):
        #Se encarga de sacar Lq con la operacion (Po*((a/m)**c)*p)/(factorial(c)*(1-p)**2
        cases = [
            (a,miu,servers,.25,-6.174119866483886e-34,.014705882), #0.014705882  # error por mutacion
            (a2,miu2,servers2,.15,-6.438358212912472e-20,0.000193929), #.000193929 # error por mutacion
            
        ]

        for inp1, inp2,inp3,inp4,inp5, expected in cases:
            
            with self.subTest(inp1=inp1,inp2=inp2,inp3=inp3,inp4=inp4,inp5=inp5, expected=expected):
                obtained = modelMMCadap.Lqmut(inp1, inp2,inp3,inp4,inp5)
                self.assertEqual(obtained, expected, "Lq(%s) should be %s" % (inp1,expected))
                
    def test_Wqmut(self):
        #Se encarga de sacar Wq con la operacion lq/a
        cases = [
            (a,0.014705882,0.0004901960666666667), #0.000490196# error por mutacion
            (a2,.000193929,1.29286e-05), #0.000012929# error por mutacion
            
        ]

        for inp1, inp2, expected in cases:
            
            with self.subTest(inp1=inp1,inp2=inp2, expected=expected):
                obtained = modelMMCadap.Wqmut(inp1, inp2)
                self.assertEqual(obtained, expected, "Wq(%s) should be %s" % (inp1,expected))

    def test_idle(self):
        #Se encarga de sacar idle con la operacion 1-p
        cases = [
            (.25,.75), # error por mutacion
            (.15,.85),# error por mutacion
            
        ]

        for inp1, expected in cases:
            
            with self.subTest(inp1=inp1, expected=expected):
                obtained = modelMMCadap.idlemut(inp1)
                self.assertEqual(obtained, expected, "idle(%s) should be %s" % (inp1,expected))   


if __name__ == '__main__':
    unittest.main()


    ####Coverage: coverage run -m unittest discover
    #coverage report