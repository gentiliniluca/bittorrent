
import os
import socket
import Util
import string
import sys
import random
import time
import Connessione
import PartService
import Part
import PeerService
import Peer
import File
import FileService

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

#       operazione di inserimento nel db del nuovo peer registrato attenzione all'istruzione che e' commentata
        conn_db=Connessione.Connessione()
        peer=PeerService.PeerService.insertNewPeer(conn_db.crea_cursore(), ipp2p, pp2p)
        conn_db.esegui_commit()
        conn_db.chiudi_connessione()
        sessionID = peer.sessionid

        sendingString = "ALGI" + sessionID
        print("\t\t\t\t\t\t\t->Restituisco: " + sendingString)
        clientSocket.send(sendingString)
        print("\t\t\t\t\t\t\t->OK")
    
    @staticmethod
    def logoutHandler(receivedString, clientSocket):
        sessionID = receivedString[4:20]
        logout=TRUE
        
        print("\t\t\t\t\t\t\tOperazione LogOut. SessionID: " + sessionID)
        
        try:
            conn_db = Connessione.Connessione()
            parts=[]
            parts = PartService.PartService.getParts(conn_db.crea_cursore(), sessionID)
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()    

            #ciclo per controllare se tutte le parti sono condivise
            i=0
            while(i<len(parts)):
                conn_db = Connessione.Connessione()
                count = int(PartService.PartService.getPartCount(conn_db.crea_cursore(), parts[i].File_randomid,parts[i].partid))
                conn_db.esegui_commit()
                conn_db.chiudi_connessione()

                if(conut<=1):
                    logout=FALSE
                    break
                i=i+1    


            if logout==TRUE:
                sendingString = "ALOG"+Util.Util.adattaStringa(10,str(len(parts)))

                #eliminazione delle parti e del peer dal db, viene fatta una volta che siamo sicuri che sia possibile il logout 
                conn_db = Connessione.Connessione()
                PartService.PartService.deleteParts(conn_db.crea_cursore(),sessionID)#elimino parti
                peer = PeerService.PeerService.getPeer(conn_db.crea_cursore(), sessionID)#elimino il peer
                peer.delete(conn_db.crea_cursore())
                conn_db.esegui_commit()
                conn_db.chiudi_connessione()    

            else:
                sendingString="NLOG"+Util.Util.adattaStringa(10,str(len(parts)))

            print("\t\t\t\t\t\t\t->Restituisco: " + sendingString)
            clientSocket.send(sendingString)
            print("\t\t\t\t\t\t\t->OK")
            
        except Exception as e:
            print(e)
        
    @staticmethod
    def addFileHandler(receivedString, clientSocket):
        sessionID=receivedString[4:20]
        randomID=receivedString[20:36]
        lenFile=receivedString[36:46]
        lenPart=receivedString[46:52]
        fileName=receivedString[52:152]
        
        fileNamePulito=Util.Util.elimina_spazi_iniziali_finali(fileName)
        fileNamePulito=Util.Util.elimina_asterischi_iniziali_finali(fileNamePulito)
        
        try:
            numeroParti=int(lenFile) // int(lenPart)
            #controllo se la divisione non e' intera
            if(int(lenFile)%int(lenPart)!=0):
                numeroParti=numeroParti+1
                
            #salvo il file e le parti sul db
            conn_db=Connessione.Connessione()
            Fileservice.FileService.insertNewFile(conn_db.crea_cursore(),sessionID,randomID,lenFile,lenPart,fileNamePulito)
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
            sendingString="AADR"+Util.Util.adattaStringa(8,str(numeroParti))
            print("\t\t\t\t\t\t\t->Restituisco: " + sendingString)
            clientSocket.send(sendingString)
            print("\t\t\t\t\t\t\t->OK")
        
        except Exception as e:
            print(e)
            
        @staticmethod
        def fileSearchHandler(receivedString, clientSocket):
            sessionID=receivedString[4:20]
            searchString=receivedString[20:40]
            
            searchStringClear=Util.Util.elimina_spazi_iniziali_finali(searchString)
            searchStringClear=Util.Util.elimina_asterischi_iniziali_finali(searchStringClear)
            
            try:
                conn_db=Connessione.Connessione()
                #vettore dei file ottenuti dalla ricerca facendo match con la stringa
                files=[]
                files=FileService.FileService.getFiles(conn_db.crea_cursore(),searchStringClear)
                conn_db.esegui_commit()
                conn_db.chiudi_connessione()
                
                sendingString="ALOO"+Util.Util.adattaStringa(3,str(len(files)))
                
                i=0
                while(i<len(files)):
                    sendingString=sendingString+file[i].randomid+Util.Util.aggiungi_spazi_finali(file[i].filename,100)
                    sendingString=sendingString+files[i].lenfile+files[i].lenpart
                    i=i+1
                print("\t\t\t\t\t\t\t->Restituisco: " + sendingString)
                clientSocket.send(sendingString)
                print("\t\t\t\t\t\t\t->OK")
            
            except Exception as e:
                print(e)
                
            