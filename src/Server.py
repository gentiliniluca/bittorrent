
import os
import socket
import Util
import string
import sys
import random
import time
import bitarray
import Connessione
import PartService
import Part
import PeerService
import Peer
import File
import FileService

from signal import signal, SIGPIPE, SIG_DFL
from os.path import stat
from debian.debfile import PART_EXTS
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
        logout=True
        
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
                count = int(PartService.PartService.getPartCount(conn_db.crea_cursore(), parts[i].File_randomid, parts[i].partid))
                conn_db.esegui_commit()
                conn_db.chiudi_connessione()

                if(count<=1):
                    logout=False
                    break
                i=i+1    


            if logout==True:
                sendingString = "ALOG"+Util.Util.adattaStringa(10,str(len(parts)))

                #eliminazione delle parti e del peer dal db, viene fatta una volta che siamo sicuri che sia possibile il logout 
                conn_db = Connessione.Connessione()
                PartService.PartService.deleteParts(conn_db.crea_cursore(),sessionID)#elimino parti
                peer = PeerService.PeerService.getPeer(conn_db.crea_cursore(), sessionID)#elimino il peer
                peer.delete(conn_db.crea_cursore())
                conn_db.esegui_commit()
                conn_db.chiudi_connessione()    

            else:
                conn_db = Connessione.Connessione()
                partdown = len(PartService.PartService.getPartsDown(conn_db.crea_cursore(), sessionID))
                conn_db.esegui_commit()
                conn_db.chiudi_connessione() 
                
                sendingString="NLOG"+Util.Util.adattaStringa(10,str(partdown))                

            print("\t\t\t\t\t\t\t->Restituisco: " + sendingString)
            clientSocket.send(sendingString)
            print("\t\t\t\t\t\t\t->OK")
            
        except Exception as e:
           print (e)
        
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
            FileService.FileService.insertNewFile(conn_db.crea_cursore(),sessionID,randomID,int(lenFile),int(lenPart),fileNamePulito)
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

        print(sessionID+" "+searchStringClear)

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
                sendingString=sendingString+files[i].randomid+Util.Util.aggiungi_spazi_finali(files[i].filename,100)
                sendingString=sendingString+Util.Util.adattaStringa(10,files[i].lenfile)+files[i].lenpart
                i=i+1

            print("\t\t\t\t\t\t\t->Restituisco: " + sendingString)
            clientSocket.send(sendingString)
            print("\t\t\t\t\t\t\t->OK")

        except Exception as e:
            print(e)
                
    @staticmethod
    def fileSearchHandlerPartList(receivedString, clientSocket):
        sessionID=receivedString[4:20]
        randomID=receivedString[20:36]

        try:

            conn_db=Connessione.Connessione()
            #vettore dei file ottenuti dalla ricerca facendo match con la stringa
            peers=[]
            peers=PeerService.PeerService.getPeersfromFile(conn_db.crea_cursore(),randomID)
            file=FileService.FileService.getFile(conn_db.crea_cursore(),randomID)
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()

            numPart=int(file.lenfile) // int(file.lenpart)

            if(int(file.lenfile)%int(file.lenpart)!=0):
                numPart=numPart+1

            sendingString="AFCH"+Util.Util.adattaStringa(3,str(len(peers)))
            partPresence=""

            i=0
            #per ogni peer
            while(i<len(peers)):
                partPresence=""
                j=0
                while(j<numPart):

                    try:
                        conn_db=Connessione.Connessione()
                        part=PartService.PartService.getPart(conn_db.crea_cursore(),peers[i].sessionid,randomID,j+1)
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione()
                        #attenzione la stringa e' ribaltata
                        partPresence=partPresence+"1"

                    except Exception as e:
                        partPresence=partPresence+"0"
                    j=j+1
                #partPresence=partPresence[::-1]
                
                partPresenceBit=bitarray.bitarray(partPresence,endian='big')
                
                partPresenceByte=partPresenceBit.tobytes()
                
                
                sendingString=sendingString+peers[i].ipp2p+Util.Util.adattaStringa(5,peers[i].pp2p)+partPresenceByte

                i=i+1

            print("\t\t\t\t\t\t\t->Restituisco: " + sendingString)
            clientSocket.send(sendingString)
            print("\t\t\t\t\t\t\t->OK")

        except Exception as e:
            #print(e)
            print("")
                
    @staticmethod
    def downloadNotification(receivedString, clientSocket):
        sessionID=receivedString[4:20]
        randomID=receivedString[20:36]
        partID=receivedString[36:44]

        try:
            conn_db=Connessione.Connessione()
            part=PartService.PartService.insertNewPart(conn_db.crea_cursore(),sessionID,randomID,partID)
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()

            conn_db=Connessione.Connessione()
            count=PartService.PartService.getPartCountfromSessionidRandomid(conn_db.crea_cursore(),sessionID,randomID)
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()

            sendingString="APAD"+Util.Util.adattaStringa(8,str(count))
            print("\t\t\t\t\t\t\t->Restituisco: " + sendingString)
            clientSocket.send(sendingString)
            print("\t\t\t\t\t\t\t->OK")

        except Exception as e:
            print(e)
