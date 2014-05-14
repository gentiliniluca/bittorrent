class SharedFile:
    def __init__(self, randomid, filename, lenfile, lenpart):
        self.randomid = randomid
        self.filename = filename
        self.lenfile = lenfile
        self.lenpart = lenpart
    
    def insert(self, database):
        
        database.execute("""INSERT INTO SharedFile
                            (randomid, filename, lenfile, lenpart)
                            VALUES (%s, %s, %s, %s)""",
                            (self.randomid, self.filename, self.lenfile, self.lenpart))
    
    def update(self, database):
        
        database.execute("""UPDATE SharedFile
                            SET filename = %s, lenfile = %s, lenpart = %s
                            WHERE randomid = %s""",
                            (self.filename, self.lenfile, self.lenpart))
    
    def delete(self, database):
        
        database.execute("""DELETE FROM SharedFile
                            WHERE randomid = %s""",
                            (self.randomid))