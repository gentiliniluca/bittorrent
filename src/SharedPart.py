class SharedPart:
    def __init__(self, partid, data, SharedFile_randomid):
        self.partid = partid
        self.data = data
        self.SharedFile_randomid = SharedFile_randomid
    
    def insert(self, database):
        try:
            database.execute("""INSERT INTO SharedPart
                                (partid, data, SharedFile_randomid)
                                VALUES (%s, %s, %s)""",
                                (self.partid, self.data, self.SharedFile_randomid))
        except:
            pass        
    
    def update(self, database):
        
        database.execute("""UPDATE SharedPart
                            SET data = %s
                            WHERE partid = %s AND SharedFile_randomid = %s """,
                            (self.data, self.partid, self.SharedFile_randomid))
    
    def delete(self, database):        
        
        database.execute("""DELETE FROM SharedPart
                            WHERE partid = %s AND SharedFile_randomid = %s""",
                            (self.partid, self.SharedFile_randomid))