
import Connessione
import Util
import os
import signal
import Server


class GestioneTracker:
    
    @staticmethod
    def SupertrackerManagement():
        print("\nAvvio come Tracker")

        s = Server.Server.initServerSocket()
        print("\n\t\t\t\t\t\tPronto a ricevere richieste...")
        while 1:            
            clientSocket, address = s.accept()
            print("\n\t\t\t\t\t\tConnesso al peer con indirizzo: " + str(address))
            newpid = os.fork()
            if(newpid == 0):
                try:
                    s.close()

                    #Server.Server.expiredPacketHandler()

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

                  

                except Exception as e: 
                    print e
                    print("\t\t\t\t\t\tErrore ricezione lato server")

                finally:
                    clientSocket.close() 
                    stringa_ricevuta_server = ""
                    os._exit(0) 

            else:
                clientSocket.close()

    print("Terminato.")