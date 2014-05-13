class Part:
    def __init__(self, Peer_sessionid, File_randomid, partid):
        self.Peer_sessionid = Peer_sessionid
        self.File_randomid = File_randomid
        self.partid = partid    
    
    def insert(self, database):
        try:
            database.execute("""INSERT INTO Part
                                (Peer_sessionid, File_randomid, partid)
                                VALUES (%s, %s, %s)""",
                                (self.Peer_sessionid, self.File_randomid, self.partid))
        except:
            pass
        
#    def update(self, database):
#        
#        database.execute("""UPDATE file
#                            SET filename = %s
#                           WHERE filemd5 = %s""",
#                            (self.filename, self.filemd5))
    
    def delete(self, database):
        
        try:
            database.execute("""DELETE FROM Part
                                WHERE Peer_sessionid = %s AND File_randomid = %s AND partid = %s""",
                                (self.Peer_sessionid, self.File_randomid, self.partid))
        except:            
            pass   