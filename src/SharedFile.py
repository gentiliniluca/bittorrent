class SharedFile:
    def __init__(self, randomid, filename, lenfile, partnum, lenpart):
        self.randomid = randomid
        self.filename = filename
        self.lenfile = lenfile
        self.partnum = partnum
        self.lenpart = lenpart
    
    def insert(self, database):
        
        database.execute("""INSERT INTO SharedFile
                            (randomid, filename, lenfile, partnum, lenpart)
                            VALUES (%s, %s, %s, %s, %s)""",
                            (self.randomid, self.filename, self.lenfile, self.partnum, self.lenpart))
    
    def update(self, database):
        
        database.execute("""UPDATE SharedFile
                            SET filename = %s, lenfile = %s, partnum = %s, lenpart = %s
                            WHERE randomid = %s""",
                            (self.filename, self.lenfile, self.partnum, self.lenpart))
    
    def delete(self, database):
        
        database.execute("""DELETE FROM SharedFile
                            WHERE randomid = %s""",
                            (self.randomid))