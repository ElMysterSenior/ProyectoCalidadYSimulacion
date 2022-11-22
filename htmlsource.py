from Exec import Server
from Exec import ServerSystem
from Exec import Client

def header():
    return '''
    <html>
    <head>
    <style>
    *{font-family: 'Roboto', sans-serif;}
    body {
        width:900px; height:600px;
        background-color:#dde1ee;
    }
    .container{
        width:900px; height:600px;
        font-weight:300;}
    div.system{
        position: fixed;
        background-color:#dde1ee;
        width:300px;
        height:70%;
        padding: 10px;
    }
    div.system *{
        position:relative;
    }
    div.servers{
        background-color:#f0f0f0;
        padding: 10px;
        margin:auto;
        width:215px;
        height:180px;
        overflow-y: scroll;
        overflow-x: hidden;
    }
    div.queue{
        background-color:#f0f0f0;
        padding: 10px;
        margin:auto;
        width:215px;
        height:180px;
        overflow-y: scroll;
        overflow-x: hidden;
    }
    .system .title{
        font-weight:500;
        font-size:25px;
        text-align: center;
    }
    .system .subtitle{
        font-weight:300;
        font-size:23px;
    }
    .icon{
        font-size:50px;
        margin: auto;
        width: 100%;
        text-align: center;
    }
    .client{
        padding-top:2px;
        height:30px;
        width:100%;
        margin:2px;
        border-bottom: 1px solid #5faffa;
    }
    .clock{
        background-color:#f0f0f0;
        height:24px;
        margin: auto;
        font-size:24px;
        text-align: center;
        padding-top:5px;
        padding-bottom:5px;
    }
    .server{
        padding-top:2px;
        height:40px;
        width:100%;
        margin:2px;
        border-bottom: 1px solid #5faffa;
    }
    </style>
    </head>'''
def body(i,systems):
    return '''
    <body>'''+'''
        <div class="clock">'''+str(i)+'''
        </div>
        <div class="container">
        <div class="system" style="left:0%">
        <div class="title">'''+ (systems[0].name if not systems == None else "" )+'''</div>
        <div class="subtitle">Servidores</div>
        <div class="servers">
            '''+(getServers(systems[0].servers) if not systems == None  else "" )+'''
        </div>
        <span class="subtitle">Cola:</span>
        <div class="queue">
            '''+(getClient(systems[0].awaitingClients) if not systems == None  else "" )+'''
        </div>
        </div>
        <div class="system" style="left:33.33%">
        <div class="title">'''+(systems[1].name if not systems == None  else "" )+'''</div>
        <div class="subtitle">Servidores</div>
        <div class="servers">
            '''+(getServers(systems[1].servers) if not systems == None  else "" )+'''
        </div>
        <span class="subtitle">Cola:</span>
        <div class="queue">
            '''+(getClient(systems[1].awaitingClients) if not systems == None  else "" )+'''
        </div>
        </div>
        <div class="system" style="left:66.66%">
        <div class="title">'''+(systems[2].name if not systems == None  else "" )+'''</div>
        <div class="subtitle">Servidores</div>
        <div class="servers">
            '''+(getServers(systems[2].servers) if not systems == None  else "" )+'''
        </div>
        <span class="subtitle">Cola:</span>
        <div class="queue">
            '''+(getClient(systems[2].awaitingClients) if not systems == None  else "" )+'''
        </div>
        </div>
        </div>
        </body>
    '''
def end():
    return '''
    </html>
    '''
def getServers(servers):
    serversDiv = ""
    for server in servers:
        serversDiv += f'''<div class="server">{server.showInfo()}</div>'''
    return serversDiv
def getClient(clients):
    clientsDiv = ""
    for client in clients:
        clientsDiv += f'''<div class="client">{client}</div>'''
    return clientsDiv
