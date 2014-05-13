import Part
#import Peer
#import sys

class PartService:
        
    @staticmethod
    def insertNewPart(database, sessionid, randomid, partid):     
        part = Part.Part(sessionid, randomid, partid)            
        part.insert(database) 
        return part       
    
    @staticmethod
    def getParts(database, sessionid):
        database.execute("""SELECT Peer_sessionid, File_randomid, partid
                            FROM Part
                            WHERE Peer_sessionid = %s
                            ORDER BY File_randomid, partid""",
                            sessionid)
        
        parts = []        
        try:            
            while True:        
                sessionid, randomid, partid = database.fetchone()        
                part = Part.Part(sessionid, randomid, partid)
                parts.append(part)
        except:
            pass
        
        return parts
    
    @staticmethod
    def getPartCount(database, randomid, partid):
        database.execute("""SELECT count(*)
                            FROM Part
                            WHERE File_randomid = %s AND partid = %s""",
                            randomid, partid)
        count, = database.fetchone()
        return count
    
    @staticmethod
    def deleteParts(database, sessionid):
        database.execute("""DELETE FROM Part
                            WHERE Peer_sessionid = %s""",
                            (self.Peer_sessionid))  