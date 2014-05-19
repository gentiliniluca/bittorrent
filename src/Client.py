import os.path
import Connessione
import random
import socket
import string
import Util
import sys
import os
import bitarray
import SharedPart
import SharedPartService
import SharedFileService
import SearchResult
import SearchResultService
import DownloadPeerService
import DownloadPartService
import ParallelDownloadService



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
            
            sharedfile = SharedFileService.SharedFileService.insertNewSharedFile(conn_db.crea_cursore(), None, nomefile, lenfile, Util.LENPART)
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
            sharedFile = SharedFileService.SharedFileService.insertNewSharedFile(conn_db.crea_cursore(), searchResults[choice - 1].randomid, searchResults[choice - 1].filename, searchResults[choice - 1].lenfile, searchResults[choice - 1].lenpart)
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
                            ParallelDownloadService.ParallelDownloadService.increase(conn_db.crea_cursore())
                            conn_db.esegui_commit()
                            conn_db.chiudi_connessione()
                            
                            try:
                                conn_db = Connessione.Connessione()
                                sharedPart = SharedPartService.SharedPartService.getSharedPart(conn_db.crea_cursore(), searchResults[choice - 1].randomid, counts[i][j])
                                conn_db.esegui_commit()
                                conn_db.chiudi_connessione()
                                
                            except:
                                
                                conn_db = Connessione.Connessione()
                                downloadPeer = DownloadPeerService.DownloadPeerService.getDownloadPeer(conn_db.crea_cursore(), counts[i][j])
                                conn_db.esegui_commit()
                                conn_db.chiudi_connessione()
                                
                                sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 
                                sock.connect((downloadPeer.ipp2p, int(downloadPeer.pp2p)))
                                sendingString = "RETP" + searchResults[choice - 1].randomid + Util.adattaStringa(8, counts[i][j])
                                #sock.send(sendingString.encode())
                                sock.send(sendingString)
                                
                                receivedString = sock.recv(10)       
                                if receivedString[0:4].decode() == "AREP":
                                    nChunk = int(receivedString[4:10].decode())            
                                    chunk = bytes()
                                    chunkCounter = 0
                    
                                    #file = open(Util.LOCAL_PATH + searchResults[choice - 1].filename, "wb")
                                    sharedPart = SharedPart.SharedPart(counts[i][j], "", sharedFile.randomid)
                                    
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
                                                #file.write(data)
                                                sharedPart.data = sharedPart.data + data
                                                chunkCounter = chunkCounter + 1
                                                chunk = chunk[5 + chunkLength:]
                                            else:
                                                break
                    
                                    #file.close()
                                    conn_db = Connessione.Connessione()
                                    sharedPart.insert(conn_db.crea_cursore())
                                    conn_db.esegui_commit()
                                    conn_db.chiudi_connessione()
                                    print ""
                            
                            finally:
                                conn_db = Connessione.Connessione()
                                ParallelDownloadService.ParallelDownloadService.decrease(conn_db.crea_cursore())
                                conn_db.esegui_commit()
                                conn_db.chiudi_connessione()
                                
                                os._exit(0)
                        
                        else:
                            j = j + 1
                    
                    # Ipotizzare presenza wait
                
                i = i + 1
            
            conn_db = Connessione.Connessione()
            sharedParts = SharedPartService.SharedPartService.getSharedParts(conn_db.crea_cursore(), sharedFile.randomid)
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
            file = open(Util.LOCAL_PATH + sharedFile.filename, "wb")
            
            i = 0
            while i < len(sharedParts):
                file.write(sharedParts[i].data)
                i = i + 1
            
            file.close()
            
            conn_db = Connessione.Connessione()
            SearchResultService.SearchResultService.unsetDownloadSearchResult(conn_db.crea_cursore())
            conn_db.esegui_commit()
            conn_db.chiudi_connessione()
            
            #controllo correttezza del download
            lenfile = os.path.getsize(Util.LOCAL_PATH + sharedFile.filename)      
            if lenfile != sharedFile.lenfile:
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
            conn_db.esegui_commit()
            conn_db.chiudi_connessione
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
                print("\t\t"+ipp2p+"  "+pp2p)
                conn_db=Connessione.Connessione()
                #salva nella tabella DownloadPeer le info appena prese
                downloadpeer=DownloadPeerService.DownloadPeerService.insertNewDownloadPeer(conn_db.crea_cursore(),ipp2p,pp2p)
                conn_db.esegui_commit()
                conn_db.chiudi_connessione
                print("\t\tinserito download peer")
                #parte elaborazione partlist e calcolo numero di parti
                numparti=int(serachResultTrue.lenfile)//int(serachResultTrue.lenpart)
                if(int(serachResultTrue.lenfile) % int(serachResultTrue.lenpart)!=0):
                    numparti= numparti+1
                
                numparti_byte=numparti//8
                if(numparti % 8!=0):
                    numparti_byte= numparti_byte+1
                
                part_list=sock.recv(numparti_byte)
               
                part_list_bit=bitarray.bitarray(endian='big')
                part_list_bit.frombytes(part_list)
               

                print("\t\tnum part binario:"+str(numparti_byte)+"   part list:"+str(part_list))
                
                j=0
                while(j<numparti):
                    if(part_list_bit[j]==1):
                        conn_db=Connessione.Connessione()
                        downloadpart=DownloadPartService.DownloadPartService.insertNewDownloadPart(conn_db.crea_cursore(), j, downloadpeer.downloadpeerid )
                        conn_db.esegui_commit()
                        conn_db.chiudi_connessione
                        print("\t\t inserito parte db")
                    j=j+1
                
                i=i+1
            sock.close()
            
        except Exception as e:
            print(e)
            print("non ci sono download in corso")
            
