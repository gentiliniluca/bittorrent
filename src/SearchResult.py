class SearchResult:
    
    def __init__(self, idsearchresult, randomid, filename, lenfile, lenpart, choose):
        self.idsearchresult = idsearchresult
        self.randomid = randomid
        self.filename = filename 
        self.lenfile = lenfile
        self.lenpart = lenpart
        self.choose = choose         
        
    def insert(self, database):
        self.choose = 'F'
        database.execute("""INSERT INTO SearchResult
                            (randomid, filename, lenfile, lenpart, choose)
                            VALUES (%s, %s, %s, %s, %s)""",
                            (self.randomid, self.filename, self.lenfile, self.lenpart, self.choose))
    
    def update(self, database):
        database.execute("""UPDATE SearchResult
                            SET randomid = %s, filename = %s, lenfile = %s, lenpart = %s, choose = %s
                            WHERE idsearchresult = %s""",
                            (self.randomid, self.filename, self.lenfile, self.lenpart, self.choose, self.idsearchresult))
        
    def setDownloadSearchResult(self, database):
        self.choose = 'T'
        self.update(database)
