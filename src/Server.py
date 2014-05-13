import Connessione

import os
import socket
import Util
import string
import sys
import random
import time

from signal import signal, SIGPIPE, SIG_DFL
from os.path import stat
signal(SIGPIPE, SIG_DFL)

class Server:
    
    global SIZE
    SIZE = 1024
    
    stringa_ricevuta_server = ""
    
    @staticmethod
    def initServerSocket():
        
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((Util.HOST, Util.PORT))
        s.listen(10)
        return s
    
    @staticmethod
    def expiredPacketHandler():
        
        conn_db = Connessione.Connessione()
        PacketService.PacketService.deleteExpiredPacket(conn_db.crea_cursore())
        conn_db.esegui_commit()
        conn_db.chiudi_connessione()
        
    @staticmethod
    def readSocket(clientSocket):
        
        stringa_ricevuta_server = clientSocket.recv(SIZE)        
        if stringa_ricevuta_server == "":
            print("\t\t\t\t\t\tSocket vuota")
        else:      
            print("\t\t\t\t\t\tPacchetto ricevuto: " + stringa_ricevuta_server)
        return stringa_ricevuta_server
    
    @staticmethod
    def loginHandler(receivedString, clientSocket):
        
        ipp2p = receivedString[4:43]
        pp2p = receivedString[43:48]
        print("\t\t\t\t\t\t\tOperazione Login. Ip: " + ipp2p + ", Porta: " + pp2p)

        #operazione di inserimento nel db del nuovo peer registrato attenzione all'istruzione che è commentata
        conn_db = Connessione.Connessione()
        #peer = PeerService.PeerService.insertNewPeer(conn_db.crea_cursore(), ipp2p, pp2p)
        conn_db.esegui_commit()
        conn_db.chiudi_connessione()
        sessionID = peer.sessionid

        sendingString = "ALGI" + sessionID
        print("\t\t\t\t\t\t\t->Restituisco: " + sendingString)
        clientSocket.send(sendingString)
        print("\t\t\t\t\t\t\t->OK")
    
    @staticmethod
    def logoutHandler(receivedString, clientSocket):
        