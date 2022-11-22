import tkinter as tk
import numpy.random as random
from collections import deque
import modelMMC
import numpy as np

#Apartir de una matriz de probabilidad se crea una que con su probabilidada acomulada
def getAcumulativeArray(array: list):
    acumulative = array
    for n in range(1, len(array), 1):
        acumulative[n] = array[n-1]+array[n]
    return acumulative

#Se guardan los datos necesarios para identificar al cliente
class Client:
    def __init__(self,id,arrival,system=None,server=None):
        self.id = id
        self.arrival = arrival
        #Determina donde ha estado el cliente
        #El path define el recorrilo del cliente
        self.path = list()
        self.awaiting = list()
        self.system = system
        self.server = server
    def __str__(self) -> str:
        return f"{self.id}->{self.arrival}"
    #Este metodo indica que se termino el servicio para el cliente
    def finish(self):
        origen = systems.index(self.system)
        #Se selecciona a que sistema se movera el cliente o si saldra del sistema
        newSystem = self.selectSystem(origen)
        if not newSystem == None:
            #Al definir el sistema de destino se envia al cliente a dicho sistema
            newSystem.clientArrive(self)
        else:
            #Se actualiza el registro de los clientes que salieron del sistema
            attendedClients.append(self)
            logs.append(Log(f"Cliente:{self.id}",globalclock,f"Terminado servicio en: {self.server.id}"))
    #Se selecciona el sistema nuevo en base a al sistema de precedencia y la matriz de probabilidad de transición
    def selectSystem(self,origen):
        azar = random.random()
        probabilities= [0]+changeProb[origen]
        probabilities = getAcumulativeArray(probabilities)
        #Bloque para elegir el sistema segun el rango en el que se encuentra el numero aleatorio
        for n in range(1, len(probabilities), 1):
            if azar>= probabilities[n-1] and azar<probabilities[n]:
                return systems[n-1]
        return None
           
class Server:
    #Datos de identificacion del servidor
    def __init__(self,id,ratio, client=None):
        self.idle:int = 0
        self.idleLog = list()
        self.timeleft:int  = 0
        self.id = id
        self.serviceRatio = ratio
        self.attending = client
    #Se define que un nuevo cliente ha sido atendido.
    def attend(self,client):
        if self.idle > 0:
            #Se registra el tiempo que habia estado desocupado cada servidor
            self.idleLog.append(self.idle)
            logs.append(Log(f"Servidor:{self.id}",globalclock,f"Saliendo de espera despues de {self.idle}m."))
        self.attending = client
        logs.append(Log(f"Cliente:{client.id}",globalclock,f"Recibiendo servicio en {self.id}"))
        #Cada vez que llega un cliente se calcula el tiempo que le tomaria ser atendido
        self.timeleft = 60/self.serviceRatio
        
        self.idle = 0
    #Determina que esta ocupado o no segun su tiempo restante en la fila para ser atendido
    def isBusy(self):
        return self.timeleft > 0
    #Lleva el control de la prestacion del servicio por parte de los servidores 
    def work(self):
        if self.isBusy():
            self.timeleft -= 1
        elif not self.isBusy():
                #Si pasa de ocupado a desocupado significa que el cliente ha sido atendido
                #Se le indica al cliente que puede seguir con su proceso, ya sea saliendo o 
                self.timeleft=0
                if not self.attending == None:
                    self.attending.finish()
                    self.attending = None
        if not self.isBusy():
            #Si no hay cliente disponible se registra el tiempo que va el servidor esta inactivo
            self.idle+=1
    def showInfo(self):
        #Mostrar la informacion del servidor
        if self.timeleft==0:
            return f"{self.id}  Idle({self.idle}m)..."
        else:
            return f"{self.id}  attending:{self.attending}  timeLeft:{format(self.timeleft, '.1f')}"
    def __str__(self) -> str:
        return f"{self.serviceRatio}"


class ServerSystem:
    #datos para identificar cada sistema de servidores
    def __init__(self,name:str,numServers,serviceRate):
        self.servers = deque()
        self.awaitingClients = deque()
        self.name = name
        #Al construir se crean los servicios de cada sistema
        for n in range(0,numServers):
            self.servers.append(Server(f"{name[0]}{n+1}",serviceRate))
    def isBusy(self) -> bool:
        #Determinar si un sitema esta ocupado en base al estado de los servidores contenidos
        for server in self.servers :
            if not server.isBusy():
                return False
        return True
    def idleServer(self) -> Server:
        #Determinar cual de los servidores contenidos esta desocupado
        for server in self.servers:
            if not server.isBusy():
                return server
    def clientArrive(self,client:Client):
        #Determinar que hacer en caso de que llegue un cliente
        if(self.isBusy()):
            client.path.append(f"{self.name[0]}")
            client.system = self
            #Si el sistema esta ocupado, el cliente esperaria en la zona designada
            self.awaitingClients.append(client)
            logs.append(Log(f"Cliente:{client.id}",globalclock,f"Esperando en sistema: {self.name}"))
        else:
            #Si el sistema esta libre, se ingresa un nuevo cliente 
            idleServer = self.idleServer()
            client.path.append(f"{idleServer.id}")
            client.system = self
            client.server = idleServer
            idleServer.attend(client)
            if self.isBusy():  
                logs.append(Log(f"Sistema:{self.name}",globalclock,f"saturado"))
    def work(self):
            #Simula el trabajo de todos los servidores dentro del sistema
        for server in self.servers :
            server.work()
            if (not server.isBusy()) and len(self.awaitingClients) >= 1:
                #Verifica si hay clientes en espera y el servidor esta disponible
                client = self.awaitingClients.popleft()
                client.path.append(f"{server.id}")
                client.server = server
                #Envia un cliente al servidor 
                server.attend(client)
        return self.showInfo()
    def showInfo(self):
        #Mostrar la informacion de todo el sistema de colas
        log = f"System:{self.name}  isBusy:{self.isBusy()}  clientsAwaiting:{len(self.awaitingClients)}\n"
        for server in self.servers :
            log+="     "+server.showInfo()+"\n"
        return log
    def __str__(self) -> str:
        return f"{self.showInfo()}"

class Log:
    def __init__(self,cliente,clock,descripcion):
        self.cliente = cliente
        self.clock = clock
        self.descripcion = descripcion
    def __str__(self) -> str:
        return f"t:{self.clock}m\t {self.cliente} \t{self.descripcion}"

def ciclo(clock):
    global globalclock
    globalclock = clock
    #Ciclo general de la simulacion

    for sys in systems:
        #Crear un nuevo cliente en recepcion solo si la plantilla indica que han llegado en determinado tiempo
        for n in range(0,arrivalsSample[systems.index(sys)][clock]):
            clientcount=len(generatedClients)+1
            newClient = Client(f"C{clientcount}",clock)
            logs.append(Log(f"Cliente:{newClient.id}",newClient.arrival,"Creacion"))
            sys.clientArrive(newClient)
            generatedClients.append(newClient)
            #print(f"*{newClient}")

    #Especificar el tiempo
    #print(f"t: {clock}")
    for sys in systems:
        #Mostrar el estado de cada sistema
        #print(sys.showInfo())
        #Simular servidores trabajando
        sys.work()

def initialize(): 
    params()
    random.seed(semilla)
    global logs
    logs = list()
    #Lista de clientes atendidos
    global generatedClients
    global attendedClients
    attendedClients = deque()
    generatedClients = deque()



    #Sistemas de colas
    receptionists = ServerSystem("Reception",nServers[0],serviceRate[0])
    parkingValets = ServerSystem("Parking",nServers[1],serviceRate[1])
    elevators = ServerSystem("Elevator",nServers[2],serviceRate[2])
    #Acceso rapido a los sistemas
    global systems
    systems = [receptionists,parkingValets,elevators]
    

    #Crear matrices de tamaño clockEnd que especifiquen cuantos clientes llegaron en cada minuto especifico
    global arrivalsSample
    clientsArrivalsReception = random.poisson(arrivals[0]/60,size=clockEnd) 
    clientsArrivalsParking = random.poisson(arrivals[1]/60,size=clockEnd) 
    clientsArrivalsElevator = random.poisson(arrivals[2]/60,size=clockEnd)
    arrivalsSample=[clientsArrivalsReception,clientsArrivalsParking,clientsArrivalsElevator]

    return systems

def params():
    global semilla
    global clockEnd
    global changeProb
    global arrivals
    global serviceRate
    global nServers
    semilla = 1500
    clockEnd = 60*1*1 #1 dias
    changeProb = [[000,0.6,0.3], [0.1,000,0.3],[0.4,0.4,000]]
    arrivals = [10,20,30]
    serviceRate = [7,10,21]
    nServers = [2,3,2]




    lambd =modelMMC.solve(np.array(changeProb),np.array(arrivals))
    rec =  modelMMC.ModelMMC(lambd[0],serviceRate[0],nServers[0])
    est =  modelMMC.ModelMMC(lambd[1],serviceRate[1],nServers[1])
    ele =  modelMMC.ModelMMC(lambd[2],serviceRate[2],nServers[2])
    colas = [rec,est,ele]
    red =  modelMMC.JacksonNet(colas)
    print(f"\nRecepcion: {rec}")
    print(f"\nEstacionamiento: {est}")
    print(f"\nElevador: {ele}")
    print(f"\n\nSistema: {red}")



    





    
    
    
    
