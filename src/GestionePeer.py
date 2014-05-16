import Client 
import Util
import os
import signal
import time

class GestionePeer:
    
    @staticmethod
    def PeerManagement():
        print("\nAvvio come peer")
#        
        pid = os.fork()
        if(pid == 0): #figlio per gestire operazioni menu
            operazione_utente = 1
            SessionID=" "
            while(int(operazione_utente) != 0):
                operazione_utente = Client.Client.visualizza_menu_principale()                        
                                    
                #login
                if(int(operazione_utente) == 1):            
                    SessionID=Client.Client.login(SessionID)
                    out_file = open("sessionID.txt","w")
                    out_file.write(SessionID)
                    out_file.close()
                
                #carica file
                if(int(operazione_utente) == 2):            
                    Client.Client.addFile(SessionID)
                
                #ricerca file
                if(int(operazione_utente) == 3):            
                    Client.Client.searchFile(SessionID)
                    
                #download file
                if(int(operazione_utente) == 4):            
                    Client.Client.downloadFile(SessionID)
                    
                #logout
                if(int(operazione_utente) == 5):            
                    SessionID=Client.Client.logout(SessionID)
                    out_file = open("sessionID.txt","w")
                    out_file.write(SessionID)
                    out_file.close()
       

            print("Fine operazioni utente")
            #pulisco DB quando esco
            os.kill(os.getppid(), signal.SIGKILL)
        
        
        else: #gestisco funzionalita server 
            pid2=os.fork()
            if(pid2==0): #processino FCHU
                while 1:
                    sessionID=""
                    time.sleep(Util.SLEEPTIME)
                    try:
                        in_file = open("sessionID.txt","r")
                        sessionID = in_file.read()
                        in_file.close()
                    except Exception as e:
                        print("non eseguito ancora il login")
                        
                    if(sessionID!= " " and sessionID!="" and sessionID!="0000000000000000"):
                        Client.Client.notificaTracker(sessionID)
            else:
                #ancora padre server
                s = Client.Client.initServerSocket()
                while 1:
                    print("\t\t\t\t\t\t\t\t\tAttesa richiesta peer")
                    client, address = s.accept()
                    newpid = os.fork()
                    if(newpid == 0):
                        try:
                            s.close()

                            receivedString = Client.Client.readSocket(client)
                            operazione = receivedString[0:4]

                            if operazione == "":
                                break

                            #operazione RETR
                            if operazione.upper() == "RETR":
                                Client.Client.uploadHandler(client,receivedString) 


                        except Exception as e: 
                            print e
                            print("\t\t\t\t\t\t\t\t\tErrore ricezione lato server")

                        finally:
                            client.close() 
                            stringa_ricevuta_server = ""
                            os._exit(0) 

                    else:
                        client.close()

            print("Terminato parte server del peer")
    
