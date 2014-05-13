class File:
    def __init__(self, randomid, lenfile, lenpart, filename):
        self.randomid = randomid
        self.lenfile = lenfile
        self.lenpart = lenpart
        self.filename = filename
        #self.peers = []
    
    def insert(self, database, sessionid):
        try:
            database.execute("""INSERT INTO File
                                (randomid, lenfile, lenpart, filename)
                                VALUES (%s, %s, %s, %s)""",
                                (self.randomid, self.lenfile, self.lenpart, self.filename))
        except:
            pass
        
#    def update(self, database):
#        
#        database.execute("""UPDATE file
#                            SET filename = %s
#                           WHERE filemd5 = %s""",
#                            (self.filename, self.filemd5))
    
#    def delete(self, database, sessionid):
#        
#        try:
#            database.execute("""DELETE FROM peer_has_file
#                                WHERE peer_sessionid = %s AND file_filemd5 = %s""",
#                                (sessionid, self.filemd5))
#        except:
#            print("File non condiviso da questo peer. Nessuna cancellazione effettuata.")
#            pass
#        
#        try:
#            database.execute("""DELETE FROM file
#                                WHERE filemd5 = %s""",
#                                (self.filemd5))
#        except:
#            pass