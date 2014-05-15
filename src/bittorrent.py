import os
import signal
import Util
import Connessione
import DBException
import GestionePeer
import GestioneTracker

class Bittorrent:
    
    print("Avvio bittorrent")
    while True:
        print ("Si vuole avviare il programma in:")
        print("\t 1. Modalita PEER")
        print("\t 2. Modalita TRACKER")
        out=raw_input("\nOperazione scelta: ")
        if(int(out) >= 1 and int(out) <= 2):
                break
        print("Valore inserito errato! (valore compreso tra 1 e 2)")
        
    
    if(int(out)==1):
        Util.USEMODE="PEER"
        GestionePeer.GestionePeer.PeerManagement()
    else:
        Util.USEMODE="TRACKER"
        GestioneTracker.GestioneTracker.SupertrackerManagement()      

