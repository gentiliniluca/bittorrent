import string
import random

class Peer:
    def __init__(self, sessionid, ipp2p, pp2p):
        self.sessionid = sessionid
        self.ipp2p = ipp2p
        self.pp2p = pp2p
    
    def insert(self, database):
        
        #check di unicita' peer
        database.execute("""SELECT *
                            FROM peer
                            WHERE ipp2p = %s AND pp2p = %s""",
                            (self.ipp2p, self.pp2p))
        
        if database.fetchone() != None:
        
            self.sessionid = "0000000000000000"
        
        else:
        
            #generazione sessionid
            self.sessionid = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        
            #check di unicita' sessionid
            database.execute("""SELECT sessionid
                                FROM Peer
                                WHERE sessionid = %s""",
                                (self.sessionid))
            while database.fetchone() != None:
                self.sessionid = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
                database.execute("""SELECT sessionid
                                    FROM Peer
                                    WHERE sessionid = %s""",
                                    (self.sessionid))
            
            #inserimento nuovo peer
            database.execute("""INSERT INTO Peer
                                (sessionid, ipp2p, pp2p)
                                VALUES
                                (%s, %s, %s)""",
                                (self.sessionid, self.ipp2p, self.pp2p))
        
    #def update(self, database): 
        #pass
    
    def delete(self, database):
        
        database.execute("""DELETE FROM Peer
                            WHERE sessionid = %s""",
                            self.sessionid)