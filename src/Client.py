import os.path
import Connessione
import random
import socket
import string
import Util
import sys
import os
import SharedPartService
import SharedFileService



from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

class Client:
    
    global SIZE
    SIZE = 1024
    
    @staticmethod
    def visualizza_menu_principale():
        
        while True: 
            print("\n************************\n*  1 - Login           *\n*  2 - Aggiunta File   *\n*  3 - Ricerca         *\n*  4 - Download        *\n*  5 - Logout          *\n*  0 - Fine            *\n************************")
            out=raw_input("\nOperazione scelta: ")
            if(int(out) >= 0 and int(out) <= 5 ):
                break
            print("Valore inserito errato!")
        
        return out
    
    
    @staticmethod
    def login(SessionID):
        stringa_da_trasmettere="LOGI"+Util.HOST+Util.Util.adattaStringa(5,str(Util.PORT) )
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.connect((Util.IPTracker, int(Util.PORTTracker) ))
            sock.send(stringa_da_trasmettere.encode())
            risposta=sock.recv(20)
            print("Session id:"+risposta[4:20])
            nuovosessionid=risposta[4:20]
            sock.close()
        except Exception as e:
            print e
            print "Errore login"
        if(nuovosessionid=="0000000000000000"):
            return SessionID
        else:
            return nuovosessionid
            
    @staticmethod
    def logout(SessionID):
       
        if(SessionID != "" and SessionID != "0000000000000000"):
            stringa_da_trasmettere="LOGO"+SessionID
            
            try:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
                sock.connect((Util.IPTracker, int(Util.PORTTracker) ))
                sock.send(stringa_da_trasmettere.encode())
                risposta=sock.recv(14)
                print(risposta)
                returnString=""
                if(risposta[0:4]=="NLOG"):
                    print("Non si puo fare Logout")
                    returnString = SessionID
                else:
                    print("Logout consentito")
                    #quando faccio il logout elimino tutti i record dalla tabella sharedfile e sharedpart
                    conn_db=Connessione.Connessione()
                    SharedPartService.SharedPartService.delete(conn_db.crea_cursore())
                    SharedFileService.SharedFileService.delete(conn_db.crea_cursore())
                    conn_db.esegui_commit()
                    conn_db.chiudi_connessione()
                    returnString = "" 
                
                sock.close()
                
            except Exception as e:
                print e
                print "Errore logout"
        return returnString
    
    
    @staticmethod
    def addFile(SessionID):
        nomefile=""
        randomid=""
        
        #aggiungo file nella tabella del peer SharedFile
        try:
            conn_db = Connessione.Connessione()
            nomefile = raw_input("Inserire il nome del file: " + Util.LOCAL_PATH)
            lenfile=os.path.getsize(Util.LOCAL_PATH+nomefile)
            
            sharedfile = SharedFileService.SharedFileService.insertNewSharedFile(conn_db.crea_cursore(), nomefile, lenfile, Util.LENPART)
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
                        
            #scrittura delle parti
            i=0
            count=lenfile//Util.LENPART
            if(lenfile % Util.LENPART !=0):
                count=count+1
                
            file_object = open(Util.LOCAL_PATH+nomefile)
            while True:
                data = file_object.read(Util.LENPART)
                if not data:
                    break
                else:
                    conn_db = Connessione.Connessione()
                    part=SharedPartService.SharedPartService.insertNewSharedPart(conn_db.crea_cursore(), i, data, sharedfile.randomid)
                    conn_db.esegui_commit()
                    conn_db.chiudi_connessione()
                i= i + 1
                
        except Exception as e:
            print e
            print("Errore aggiunta file")
        
        
        #formatto e invio stringa di aggiunta file al tracker    
        try:
            nomefile = Util.Util.aggiungi_spazi_finali(nomefile,100)
            stringa_da_inviare="ADDR"+SessionID+sharedfile.randomid+Util.Util.adattaStringa(10,str(lenfile))+Util.Util.adattaStringa(6,str(Util.LENPART))+nomefile
            print(stringa_da_inviare)
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.connect((Util.IPTracker, int(Util.PORTTracker) ))
            sock.send(stringa_da_inviare)
            risposta=sock.recv(14)
            print("Ricevuto: "+risposta+", Numero parti condivise: "+risposta[4:12])
            sock.close()
        except Exception as e:
            print e
            print("Errore per contattare il superpeer in add file")
    
    @staticmethod 
    def searchFile(SessionID):
        
        try:
            conn_db = Connessione.Connessione()
            SearchResultService.SearchResultService.delete(conn_db.crea_cursore())
        finally:
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
        
        while True:
            query_ricerca = raw_input("\n\tInserire la stringa di ricerca (massimo 20 caratteri): ")
            if(len(query_ricerca) <= 20):
                break
            print("\n\tErrore lunghezza query maggiore di 20!")
        query_ricerca = Util.Util.riempi_stringa(query_ricerca, 20)
        stringa_da_trasmettere = "LOOK" + SessionID + query_ricerca
        print "Invio supernodo: " + stringa_da_trasmettere
        
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.connect((Util.IPTracker, int(Util.PORTTracker)))
            sock.send(stringa_da_trasmettere.encode())
            
            #lettura e scrittura su db dei risultati della ricerca di un file 
            stringa_ricevuta = sock.recv(4)
            if(stringa_ricevuta!="AFIN"):
                print "Errore non ricevuto AFIN"
            else:
                stringa_ricevuta=sock.recv(3)
                print(stringa_ricevuta)
                occorenze_md5=int(stringa_ricevuta)
                print("occorenze md5: "+str(occorenze_md5))

                for i in range(0,occorenze_md5):
                        #print("ciao contatore: "+str(i))
                        filemd5=sock.recv(16)
                        print("md5: "+filemd5)
                        filename=sock.recv(100)
                        #elimino eventuali asterischi e spazi finali
                        filename=Util.Util.elimina_spazi_iniziali_finali(filename)
                        filename=Util.Util.elimina_asterischi_iniziali_finali(filename)
                        
                        print("file name: "+filename)
                        occorenze_peer=int(sock.recv(3))
                        print("occorenze peer: "+str(occorenze_peer))
                        #print("Contatore: "+str(i)+"filemd5: "+filemd5+"filename: "+filename+" Occorenze Perr: "+str(occorenze_peer))
                        for j in range(0,occorenze_peer):
                                ipp2p=sock.recv(39)
                                pp2p=sock.recv(5)
                                print("IPP2P"+ipp2p+"PP2P: "+pp2p )
                                try:
                                    conn_db=Connessione.Connessione()
                                    SearchResultService.SearchResultService.insertNewSearchResult(conn_db.crea_cursore(), ipp2p, pp2p, filemd5, filename, "0000000000000000", 'T')
                                finally:
                                    conn_db.esegui_commit()
                                    conn_db.chiudi_connessione   
            sock.close()
            
        except Exception as e:
            print e
            print"Errore nel contattare il supernodo per ricerca file"
            
            
    @staticmethod
    def initServerSocket():
        
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((Util.HOST, Util.PORT))
        s.listen(10)
        return s
        
    
