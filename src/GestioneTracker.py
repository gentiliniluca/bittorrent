
import Connessione
import Util
import os
import signal
import Server
import Client
import time


class GestioneTracker:
    
    @staticmethod
    def SupertrackerManagement():
        print("\nAvvio come Tracker")
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
                s = Server.Server.initServerSocket()
                print("\n\t\t\t\t\t\tPronto a ricevere richieste...")
                while 1:            
                    clientSocket, address = s.accept()
                    print("\n\t\t\t\t\t\tConnesso al peer con indirizzo: " + str(address))
                    newpid = os.fork()
                    if(newpid == 0):
                        try:
                            s.close()
                            try:
                                while 1:  #mi controllo la persistenza del peer

                                    receivedString = Server.Server.readSocket(clientSocket)
                                    operazione = receivedString[0:4]

                                    if operazione == "":
                                        break

                                    #login
                                    if operazione.upper() == "LOGI":
                                        Server.Server.loginHandler(receivedString, clientSocket)

                                    #logout         
                                    if operazione.upper() == "LOGO":
                                        Server.Server.logoutHandler(receivedString, clientSocket)                   

                                    #addfile         
                                    if operazione.upper() == "ADDR":
                                        Server.Server.addFileHandler(receivedString, clientSocket) 

                                    #ricerca parte 1 LOOK
                                    if operazione.upper() == "LOOK":
                                        Server.Server.fileSearchHandler(receivedString, clientSocket) 

                                    #ricerca parte 2 FCHU
                                    if operazione.upper() == "FCHU":
                                        Server.Server.fileSearchHandlerPartList(receivedString, clientSocket)

                                    #notifica download
                                    if operazione.upper() == "RPAD":
                                        Server.Server.downloadNotification(receivedString, clientSocket)

                            except Exception as nonpersistente:
                                print nonpersistente
                                print("Connessione non persistente")

                        except Exception as e: 
                            print e
                            print("\t\t\t\t\t\tErrore ricezione lato server")

                        finally:
                            clientSocket.close() 
                            stringa_ricevuta_server = ""
                            os._exit(0) 

                    else:
                        clientSocket.close()

        print("Terminato tracker.")
