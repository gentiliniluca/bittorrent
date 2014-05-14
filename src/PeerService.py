import Peer

class PeerService:
    
    @staticmethod
    def insertNewPeer(database, ipp2p, pp2p):
        peer = Peer.Peer(None, ipp2p, pp2p)
        peer.insert(database)
        return peer
    
    @staticmethod
    def getPeer(database, sessionid):
        database.execute("""SELECT sessionid, ipp2p, pp2p
                            FROM Peer
                            WHERE sessionid = %s""",
                            sessionid)
        sessionid, ipp2p, pp2p = database.fetchone()
        peer = Peer.Peer(sessionid, ipp2p, pp2p)
        return peer
    
    @staticmethod
    def getPeersfromFile(database, randomid):
        database.execute("""SELECT DISTINCT sessionid,ipp2p, pp2p
                            FROM Peer,Part,File
                            WHERE randomid LIKE %s
                            AND Peer.sessionid=Part.Peer_sessionid 
                            AND File.randomid=Part.File_randomid
                            ORDER BY randomid""",
                            randomid)        
        
        try:            
            peers = []         
            
            while True:            
                sessionid,ipp2p, pp2p = database.fetchone()       
                peers.append(Peer.Peer(sessionid, ipp2p, pp2p))     
                                
        except:
            pass            
            
        return peers
    
    
    @staticmethod
    def getCountFile(database, sessionid):
        
        database.execute("""SELECT count(*)
                            FROM Part
                            WHERE Peer_sessionid = %s""",
                            sessionid)
        
        count, = database.fetchone()
        
        return count