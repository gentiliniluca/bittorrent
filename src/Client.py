
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
import SearchResultService



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
        #pulisco tabella search result x fare nuova ricerca
        try:
            conn_db = Connessione.Connessione()
            SearchResultService.SearchResultService.delete(conn_db.crea_cursore())
        finally:
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
        
        #input stringa di ricerca
        while True:
            query_ricerca = raw_input("\n\tInserire la stringa di ricerca (massimo 20 caratteri): ")
            if(len(query_ricerca) <= 20):
                break
            print("\n\tErrore lunghezza query maggiore di 20!")
        query_ricerca = Util.Util.riempi_stringa(query_ricerca, 20)
        stringa_da_trasmettere = "LOOK" + SessionID + query_ricerca
        print "Query da trasmettere: " + stringa_da_trasmettere
        
        try:
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.connect((Util.IPTracker, int(Util.PORTTracker)))
            sock.send(stringa_da_trasmettere.encode())
            
            #lettura e scrittura su db dei risultati della ricerca di un file 
            stringa_ricevuta = sock.recv(4)
            if(stringa_ricevuta!="ALOO"):
                print "Errore, non ricevuto ALOO"
            else:
                stringa_ricevuta=sock.recv(3)
                print(stringa_ricevuta)
                occorenze_randomid=int(stringa_ricevuta)
                print("occorenze randomid: "+str(occorenze_randomid))

                for i in range(0,occorenze_randomid):
                        #print("ciao contatore: "+str(i))
                        randomid=sock.recv(16)
                        print("randomID: "+randomid)
                        filename=sock.recv(100)
                        lenfile=sock.recv(10)
                        print("lunghezza file : "+lenfile)
                        lenpart=sock.recv(6)
                        print("len part : "+lenpart)
                        #elimino eventuali asterischi e spazi finali
                        filename=Util.Util.elimina_spazi_iniziali_finali(filename)
                        filename=Util.Util.elimina_asterischi_iniziali_finali(filename)
                        print("file name: #"+filename+"#")
 
                        try:
                            conn_db=Connessione.Connessione()
                            SearchResultService.SearchResultService.insertNewSearchResult(conn_db.crea_cursore(), randomid, filename, lenfile, lenpart)
                        finally:
                            conn_db.esegui_commit()
                            conn_db.chiudi_connessione   
            sock.close()
            
        except Exception as e:
            print e
            print"Errore nella ricerca file, searchFile Client"
            
    @staticmethod
    def downloadFile():
        
        conn_db = Connessione.Connessione()
        searchResults = SearchResultService.SearchResultService.getSearchResults(conn_db.crea_cursore())
        conn_db.esegui_commit()
        conn_db.chiudi_connessione()
        
        i = 0
        while i < len(searchResults):
            print("\t" + str(i + 1) + ".\t" + searchResults[i].filename + "\t" + searchResults[i].lenfile)
            i = i + 1
        
        #il valore di choice e' incrementato di uno
        choice = int(raw_input("\t  Scegliere il numero del peer da cui scaricare (0 annulla): ")) 
        
        if(choice > 0):
            
            conn_db = Connessione.Connessione()
            searchResults[choice - 1].setDownloadSearchResult(conn_db.crea_cursore())
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
            conn_db = Connessione.Connessione()
            counts = DownloadPartService.DownloadPartService.getPartCount(conn_db.crea_cursore())
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
            i = 0
            while i < len(counts):
                j = 0
                while j < len(counts[i]):
                    conn_db = Connessione.Connessione()
                    parallelDownload = ParallelDownloadService.ParallelDownloadService.getParallelDownload(conn_db.crea_cursore())
                    conn_db.esegui_commit()
                    conn_db.chiudi_connessione()
                    
                    if parallelDownload.number < Util.PARALLELDOWNLOADS:
                        newpid = os.fork()
                    
                        if newpid == 0:
                            conn_db = Connessione.Connessione()
                            cursor = conn_db.crea_cursore()
                            try:
                                
                                sharedPart = SharedPartService.SharedPartService.getSharedPart(cursor, searchResults[choice - 1].randomid, counts[i][j])
                                
                            except:
                                
                                downloadPeer = DownloadPeerService.DownloadPeerService.getDownloadPeer(cursor, counts[i][j])
                                
                                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 
                                sock.connect((downloadPeer.ipp2p, int(downloadPeer.pp2p)))
                                sendingString = "RETP" + searchResults[choice - 1].randomid + Util.adattaStringa(8, counts[i][j])
                                #sock.send(sendingString.encode())
                                sock.send(sendingString)
                                
                            finally:
                                
                                conn_db.esegui_commit()
                                conn_db.chiudi_connessione()
            
            conn_db = Connessione.Connessione()
            downloadPeer = DownloadPeerService.DownloadPeerService.getDownloadPeer(conn_db.crea_cursore())
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 
            sock.connect((searchResults[choice - 1].ipp2p, int(searchResults[choice - 1].pp2p)))
            sendingString = "RETR" + searchResults[choice - 1].filemd5
            #sock.send(sendingString.encode())
            sock.send(sendingString)

            receivedString = sock.recv(10)        
            if receivedString[0:4].decode() == "ARET":
                nChunk = int(receivedString[4:10].decode())            
                chunk = bytes()
                chunkCounter = 0

                file = open(Util.LOCAL_PATH + searchResults[choice - 1].filename, "wb")
                
                #inizializzo la variabile temporanea per stampre la percentuale
                tmp = -1
                print "\nDownloading...\t",
                
                while chunkCounter < nChunk:
                    receivedString = sock.recv(1024)
                    chunk = chunk + receivedString                

                    while True:
                        
                        #Un po' di piacere per gli occhi...
                        perCent = chunkCounter*100//nChunk
                        if(perCent % 10 == 0 and tmp != perCent):
                            if(tmp != -1):
                                print " - ",
                            print str(perCent) + "%",
                            tmp = perCent
                        
                        if len(chunk[:5]) >=  5:
                            chunkLength = int(chunk[:5])
                        else:
                            break

                        if len(chunk[5:]) >= chunkLength:
                            data = chunk[5:5 + chunkLength]
                            file.write(data)
                            chunkCounter = chunkCounter + 1
                            chunk = chunk[5 + chunkLength:]
                        else:
                            break

                file.close()
                print ""

            sock.close() 

            #controllo correttezza del download
            myMd5 = Util.Util.md5(Util.LOCAL_PATH + searchResults[choice - 1].filename)        
            if myMd5 != searchResults[choice - 1].filemd5:
                print("Errore nel download del file, gli md5 sono diversi!")  
        else:
            print("Annullato")
            
    @staticmethod
    def initServerSocket():
        
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((Util.HOST, Util.PORT))
        s.listen(10)
        return s
        
    
    @staticmethod
    def notificaTracker(sessionid):
        try:
            conn_db=Connessione.Connessione()
            serachResultTrue=SearchResultService.SearchResultService.getSearchResultTrue(conn_db.crea_cursore())
            stringa_da_trasmettere="FCHU"+sessionid+serachResultTrue.randomid
            sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            sock.connect((Util.IPTracker, int(Util.PORTTracker)))
            sock.send(stringa_da_trasmettere.encode())
            
            stringa_ricevuta = sock.recv(4)
            hitpeer = sock.recv(3)
            i=0
            while(i<int(hitpeer)):
                ipp2p=sock.recv(39)
                pp2p=sock.recv(5)
                #parte elaborazione partlist
                
                i=i+1
            print(stringa_ricevuta)
            sock.close()
            
        except Exception as e:
            print(e)
            print("non ci sono download in corso")
        finally:
            conn_db.esegui_commit()
            conn_db.chiudi_connessione
